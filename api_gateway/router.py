import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict, Any
from .version_manager import VersionManager
from .rate_limiter import RateLimiter
from security.authentication import Authentication
from security.access_control import AccessControl, Permission

class APIRouter:
    def __init__(self, kernel, auth: Authentication, access_control: AccessControl):
        self.app = FastAPI()
        self.kernel = kernel
        self.auth = auth
        self.access_control = access_control
        self.version_manager = VersionManager()
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self.logger = logging.getLogger(__name__)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/token")
        async def login(username: str, password: str):
            token = self.auth.login(username, password)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return {"access_token": token, "token_type": "bearer"}

        @self.app.post("/execute_task")
        async def execute_task(task: Dict[str, Any], token: str = Depends(self.oauth2_scheme)):
            if not self.rate_limiter.allow_request():
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            user_id = self.auth.get_user_id_from_token(token)
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")

            if not self.access_control.check_permission(user_id, Permission.EXECUTE):
                raise HTTPException(status_code=403, detail="Permission denied")

            try:
                result = self.kernel.process_command(task)
                return {"result": result}
            except Exception as e:
                self.logger.error(f"Error executing task: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.get("/system_status")
        async def system_status(token: str = Depends(self.oauth2_scheme)):
            if not self.rate_limiter.allow_request():
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            user_id = self.auth.get_user_id_from_token(token)
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")

            if not self.access_control.check_permission(user_id, Permission.READ):
                raise HTTPException(status_code=403, detail="Permission denied")

            try:
                status = self.kernel.resource_manager.check_resources()
                return status
            except Exception as e:
                self.logger.error(f"Error getting system status: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.post("/update_config")
        async def update_config(config: Dict[str, Any], token: str = Depends(self.oauth2_scheme)):
            if not self.rate_limiter.allow_request():
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            user_id = self.auth.get_user_id_from_token(token)
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")

            if not self.access_control.check_permission(user_id, Permission.ADMIN):
                raise HTTPException(status_code=403, detail="Permission denied")

            try:
                self.kernel.update_config(config)
                return {"status": "Configuration updated successfully"}
            except Exception as e:
                self.logger.error(f"Error updating configuration: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")

    def run(self, host="0.0.0.0", port=8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)