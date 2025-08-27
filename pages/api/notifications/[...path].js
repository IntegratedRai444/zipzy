import { createProxyMiddleware } from 'http-proxy-middleware';

const proxy = createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  pathRewrite: {
    '^/api/notifications': '/api/notifications',
  },
  onProxyReq: (proxyReq, req, res) => {
    // Forward authorization header
    if (req.headers.authorization) {
      proxyReq.setHeader('Authorization', req.headers.authorization);
    }
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(500).json({ error: 'Proxy error' });
  },
});

export default function handler(req, res) {
  proxy(req, res, (result) => {
    if (result instanceof Error) {
      return res.status(500).json({ error: result.message });
    }
    throw new Error(`Request '${req.url}' is not proxied!`);
  });
}

export const config = {
  api: {
    bodyParser: false,
  },
};
