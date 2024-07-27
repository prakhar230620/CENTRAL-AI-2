from flask import Flask, render_template, jsonify, request
from core.kernel import Kernel

app = Flask(__name__)
kernel = Kernel()

@app.route('/')
def index():
    return render_template('core.html')

@app.route('/api/core/status')
def get_status():
    return kernel.get_status()

@app.route('/api/core/start', methods=['POST'])
def start_kernel():
    kernel.start()
    return jsonify({"message": "Kernel started"})

@app.route('/api/core/stop', methods=['POST'])
def stop_kernel():
    kernel.stop()
    return jsonify({"message": "Kernel stopped"})

@app.route('/api/core/update-config', methods=['POST'])
def update_config():
    new_config = request.json
    kernel.update_config(new_config)
    return jsonify({"message": "Configuration updated"})

if __name__ == '__main__':
    app.run(debug=True)