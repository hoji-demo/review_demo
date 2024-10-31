import express from 'express';
import sqlite3 from 'sqlite3';
import { exec } from 'child_process';

const app = express();
app.use(express.json());

const db = new sqlite3.Database(':memory:');
db.serialize(() => {
  db.run(`CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    notes TEXT
  )`);
  db.run("INSERT INTO users VALUES (1, 'admin', 'password123', 'super secret notes')");
});

app.get('/api/user', (req, res) => {
  const { username } = req.query;
  db.get(`SELECT * FROM users WHERE username = '${username}'`, (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(row);
  });
});

app.post('/api/ping', (req, res) => {
  const { host } = req.body;
  exec(`ping -c 1 ${host}`, (error, stdout) => {
    if (error) {
      res.status(500).json({ error: error.message });
      return;
    }
    res.json({ output: stdout });
  });
});

app.get('/api/profile', (req, res) => {
  const { name } = req.query;
  res.send(`
    <html>
      <body>
        <h1>Welcome back, ${name}!</h1>
        <div id="profile"></div>
      </body>
    </html>
  `);
});

app.get('/api/notes/:id', (req, res) => {
  const { id } = req.params;
  db.get('SELECT notes FROM users WHERE id = ?', id, (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(row);
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
