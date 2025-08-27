const { createProxyMiddleware } = require('http-proxy-middleware');

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

module.exports = async function handler(req, res) {
  const { path } = req.query;
  const targetPath = path ? path.join('/') : '';
  
  // Set up proxy
  const proxy = createProxyMiddleware({
    target: API_BASE_URL,
    changeOrigin: true,
    pathRewrite: {
      '^/api/partners': '/api/partners',
    },
    onProxyReq: (proxyReq, req, res) => {
      // Forward the original path
      proxyReq.path = `/api/partners/${targetPath}`;
      
      // Forward headers
      if (req.headers.authorization) {
        proxyReq.setHeader('Authorization', req.headers.authorization);
      }
      if (req.headers['content-type']) {
        proxyReq.setHeader('Content-Type', req.headers['content-type']);
      }
    },
    onError: (err, req, res) => {
      console.error('Proxy error:', err);
      res.status(500).json({ error: 'Proxy error' });
    }
  });

  // Handle the request
  return new Promise((resolve, reject) => {
    proxy(req, res, (result) => {
      if (result instanceof Error) {
        return reject(result);
      }
      return resolve(result);
    });
  });
};
