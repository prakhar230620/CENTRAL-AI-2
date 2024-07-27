import logging
from datetime import datetime
import traceback

class ErrorLogger:
    def __init__(self, log_file='error_log.txt'):
        self.logger = logging.getLogger(__name__)
        self.log_file = log_file

    def log_error(self, error, context=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"[{timestamp}] {type(error).__name__}: {str(error)}"
        if context:
            error_message += f"\nContext: {context}"
        error_message += f"\nTraceback:\n{traceback.format_exc()}"

        self.logger.error(error_message)

        with open(self.log_file, 'a') as f:
            f.write(error_message + "\n\n")

    def get_recent_errors(self, n=10):
        with open(self.log_file, 'r') as f:
            errors = f.read().split('\n\n')
        return errors[-n:]

    def clear_log(self):
        open(self.log_file, 'w').close()
        self.logger.info(f"Error log cleared: {self.log_file}")