module.exports = async function handler(req, res) {
  const { path = [] } = req.query;
  const targetPath = Array.isArray(path) ? path.join('/') : path;
  const backendBase = process.env.BACKEND_URL || 'http://localhost:8000';

  const url = `${backendBase}/api/external-ai/${targetPath}`;

  try {
    const headers = new Headers();
    for (const [key, value] of Object.entries(req.headers)) {
      if (typeof value === 'string') headers.set(key, value);
    }
    if (req.body && !headers.has('content-type')) {
      headers.set('content-type', 'application/json');
    }

    const init = {
      method: req.method,
      headers,
      body: req.method === 'GET' || req.method === 'HEAD' ? undefined : JSON.stringify(req.body ?? {}),
    };

    const response = await fetch(url, init);
    const contentType = response.headers.get('content-type') || '';
    const status = response.status;

    if (contentType.includes('application/json')) {
      const data = await response.json();
      return res.status(status).json(data);
    }

    const text = await response.text();
    res.status(status).send(text);
  } catch (err) {
    res.status(502).json({ error: 'Bad gateway', detail: String(err) });
  }
};


