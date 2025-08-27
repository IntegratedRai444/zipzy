import { createProxyMiddleware } from 'http-proxy-middleware';

// Simple in-memory rate limit per IP
const hits = new Map();
const WINDOW_MS = 60_000; // 1 minute
const MAX_HITS = 60; // 60 req/min/IP

function allowed(req) {
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown';
  const now = Date.now();
  const entry = hits.get(ip) || { t: now, c: 0 };
  if (now - entry.t > WINDOW_MS) {
    hits.set(ip, { t: now, c: 1 });
    return true;
  }
  if (entry.c >= MAX_HITS) return false;
  entry.c += 1;
  hits.set(ip, entry);
  return true;
}

const target = process.env.LEGACY_SERVER_URL || 'http://localhost:4001';

const proxy = createProxyMiddleware({
  target,
  changeOrigin: true,
  pathRewrite: {
    '^/api/legacy/server': '/',
  },
  onProxyReq: (proxyReq, req) => {
    if (req.headers.authorization) {
      proxyReq.setHeader('Authorization', req.headers.authorization);
    }
  },
});

export default function handler(req, res) {
  const expected = process.env.PROXY_INTERNAL_TOKEN;
  const provided = req.headers['x-internal-proxy-token'];
  if (!expected || provided !== expected) {
    return res.status(401).json({ error: 'Unauthorized proxy access' });
  }
  if (!allowed(req)) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  proxy(req, res, (result) => {
    if (result instanceof Error) {
      return res.status(500).json({ error: result.message });
    }
    res.status(404).json({ error: 'Not proxied' });
  });
}

export const config = { api: { bodyParser: false } };


