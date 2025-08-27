import { createProxyMiddleware } from 'http-proxy-middleware';

const proxy = createProxyMiddleware({
  target: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  changeOrigin: true,
  pathRewrite: {
    '^/api/restaurants': '/api/restaurants',
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

export default proxy;

export const config = {
  api: {
    externalResolver: true,
  },
};
