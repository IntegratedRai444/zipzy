const axios = require('axios');

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

module.exports = async function handler(req, res) {
  const { path } = req.query;
  const apiPath = Array.isArray(path) ? path.join('/') : path;

  try {
    if (req.headers.upgrade === 'websocket') {
      res.status(400).json({ error: 'WebSocket connections should be made directly to the backend' });
      return;
    }

    const response = await axios({
      method: req.method,
      url: `${BACKEND_URL}/api/geolocation/${apiPath}`,
      data: req.method !== 'GET' ? req.body : undefined,
      params: req.method === 'GET' ? req.query : undefined,
      headers: {
        'Content-Type': 'application/json',
        ...req.headers
      },
      timeout: 30000
    });

    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Geolocation API proxy error:', error);
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({
        error: 'Internal server error',
        message: error.message
      });
    }
  }
};
