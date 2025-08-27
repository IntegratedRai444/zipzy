module.exports = async function handler(req, res) {
  const { path } = req.query;
  const pathString = Array.isArray(path) ? path.join('/') : path || '';

  try {
    const backendUrl = `http://localhost:8000/api/auth/${pathString}`;

    // Pass only safe headers to backend
    const { host, connection, 'content-length': _cl, ...rest } = req.headers || {};

    const response = await fetch(backendUrl, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        ...rest,
      },
      body: req.method && req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body || {}) : undefined,
    });

    const text = await response.text();
    let data;
    try { data = JSON.parse(text); } catch { data = text; }

    res.status(response.status).json(data);
  } catch (error) {
    console.error('API proxy error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
