const express = require('express');
const os = require('os');

const app = express();
const PORT = 5000;

app.get('/', (req, res) => {
    const hostname = os.hostname();
    const ip = Object.values(os.networkInterfaces())
        .flat()
        .find(addr => addr.family === 'IPv4' && !addr.internal)?.address || 'N/A';
    
    res.json({
        hostname: hostname,
        ip_address: ip
    });
});

app.get('/greet', (req, res) => {
    res.json({
        message: 'Hello, welcome to the Node.js app!'
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
});
