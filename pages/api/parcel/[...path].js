module.exports = async function handler(req, res) {
  const { path } = req.query;
  const pathString = Array.isArray(path) ? path.join('/') : path || '';
  try {
    const backendUrl = `http://localhost:8000/api/parcel/${pathString}`;
    const response = await fetch(backendUrl, {
      method: req.method,
      headers: { 'Content-Type': 'application/json', ...req.headers },
      body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
    });
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error('API proxy error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};


