const fs = require('fs');
const path = require('path');

module.exports = async function handler(req, res) {
  try {
    const targetPath = path.join(process.cwd(), 'frontend', 'zipzy-unified', 'supabase-setup.sql');
    const content = fs.readFileSync(targetPath, 'utf8');
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(200).send(content);
  } catch (err) {
    console.error('Failed to read supabase-setup.sql', err);
    return res.status(500).json({ error: 'Failed to load file' });
  }
};


