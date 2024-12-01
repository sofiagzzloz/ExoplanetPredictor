const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// MySQL connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'exoplanet_user',
  password: 'Sofimessi13!',
  database: 'exoplanet_explorer'
});

connection.connect(error => {
  if (error) throw error;
  console.log("Successfully connected to the database.");
});

// Routes
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

app.post('/articles', (req, res) => {
    const { title, content, author } = req.body;
    const sql = 'INSERT INTO articles (title, content, author) VALUES (?, ?, ?)';
    connection.query(sql, [title, content, author], (error, results) => {
      if (error) throw error;
      res.status(201).send(`Article added with ID: ${results.insertId}`);
    });
  });

  app.get('/articles', (req, res) => {
    const sql = 'SELECT * FROM articles';
    connection.query(sql, (error, results) => {
      if (error) throw error;
      res.status(200).json(results);
    });
  });

  app.put('/articles/:id', (req, res) => {
    const { id } = req.params;  // Get article ID from URL
    const { title, content, author } = req.body;  // Get updated values from request body
  
    const sql = 'UPDATE articles SET title = ?, content = ?, author = ? WHERE id = ?';
    connection.query(sql, [title, content, author, id], (error, results) => {
      if (error) {
        return res.status(500).send('Error updating the article: ' + error.message);
      }
      if (results.affectedRows === 0) {
        return res.status(404).send('Article not found');
      }
      res.send('Article updated successfully.');
    });
  });

  app.delete('/articles/:id', (req, res) => {
    const { id } = req.params;  // Get article ID from URL
  
    const sql = 'DELETE FROM articles WHERE id = ?';
    connection.query(sql, [id], (error, results) => {
      if (error) {
        return res.status(500).send('Error deleting the article: ' + error.message);
      }
      if (results.affectedRows === 0) {
        return res.status(404).send('Article not found');
      }
      res.send('Article deleted successfully.');
    });
  });

  app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  });

  function validateArticle(req, res, next) {
    const { title, content, author } = req.body;
    if (!title || !content || !author) {
      return res.status(400).send('Missing required fields');
    }
    next();
  }
  
  app.post('/articles', validateArticle, (req, res) => {
    // Your existing code
  });
  
  app.put('/articles/:id', validateArticle, (req, res) => {
    // Your existing code
  });

  require('dotenv').config();  // npm install dotenv



  