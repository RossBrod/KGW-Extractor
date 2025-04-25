import express from 'express';
import cors from 'cors';
import { Pool } from 'pg';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

console.log('Database URL:', process.env.DATABASE_URL);

const app = express();
app.use(cors());
app.use(express.json());

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

// Test database connection
pool.connect((err, client, release) => {
  if (err) {
    console.error('Error connecting to the database:', err);
    return;
  }
  console.log('Successfully connected to the database');
  
  // Test query
  client.query('SELECT COUNT(*) FROM prompts', (err, result) => {
    release();
    if (err) {
      console.error('Error executing test query:', err);
      return;
    }
    console.log('Total prompts in database:', result.rows[0].count);
  });
});

// Get all prompts
app.get('/api/prompts', async (req, res) => {
  try {
    console.log('Executing query: SELECT functional_area, is_on FROM prompts ORDER BY functional_area');
    const result = await pool.query('SELECT functional_area, is_on FROM prompts ORDER BY functional_area');
    console.log('Query result:', result.rows);
    console.log('Number of rows returned:', result.rows.length);
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update prompt status
app.put('/api/prompts/:functional_area', async (req, res) => {
  const { functional_area } = req.params;
  const { is_on } = req.body;
  
  try {
    await pool.query('UPDATE prompts SET is_on = $1 WHERE functional_area = $2', [is_on, functional_area]);
    res.json({ success: true });
  } catch (err) {
    console.error('Error executing query:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 