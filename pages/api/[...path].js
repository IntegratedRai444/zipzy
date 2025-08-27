// Generic proxy for FastAPI backend. Catches any /api/* calls not otherwise handled.
// Forward to FastAPI at localhost:8000 preserving method, body and safe headers.
module.exports = async function handler(req, res) {
  try {
    const { path } = req.query;
    const pathString = Array.isArray(path) ? path.join('/') : (path || '');
    const backendUrl = `http://localhost:8000/api/${pathString}`;

    const { host, connection, 'content-length': _cl, 'accept-encoding': _ae, ...rest } = req.headers || {};

    const response = await fetch(backendUrl, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        ...rest,
      },
      body: req.method && req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body || {}) : undefined,
    });

    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      const data = await response.json();
      res.status(response.status).json(data);
    } else {
      const text = await response.text();
      res.status(response.status).send(text);
    }
  } catch (error) {
    console.error('Generic API proxy error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}


