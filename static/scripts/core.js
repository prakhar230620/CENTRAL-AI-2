document.addEventListener('DOMContentLoaded', () => {
    const statusText = document.getElementById('statusText');
    const cpuUsage = document.getElementById('cpuUsage').querySelector('span');
    const memoryUsage = document.getElementById('memoryUsage').querySelector('span');
    const configList = document.getElementById('configList');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const updateConfigBtn = document.getElementById('updateConfigBtn');

    function updateStatus() {
        fetch('/api/core/status')
            .then(response => response.json())
            .then(data => {
                statusText.textContent = data.status;
                cpuUsage.textContent = `${data.resources.cpu}%`;
                memoryUsage.textContent = `${data.resources.memory}%`;

                configList.innerHTML = '';
                for (const [key, value] of Object.entries(data.config)) {
                    const li = document.createElement('li');
                    li.textContent = `${key}: ${value}`;
                    configList.appendChild(li);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    startBtn.addEventListener('click', () => {
        fetch('/api/core/start', { method: 'POST' })
            .then(() => updateStatus())
            .catch(error => console.error('Error:', error));
    });

    stopBtn.addEventListener('click', () => {
        fetch('/api/core/stop', { method: 'POST' })
            .then(() => updateStatus())
            .catch(error => console.error('Error:', error));
    });

    updateConfigBtn.addEventListener('click', () => {
        const newConfig = prompt('Enter new configuration as JSON:');
        if (newConfig) {
            fetch('/api/core/update-config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: newConfig,
            })
            .then(() => updateStatus())
            .catch(error => console.error('Error:', error));
        }
    });

    updateStatus();
    setInterval(updateStatus, 5000);  // Update every 5 seconds
});