const mysql = require('mysql');

const connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'exoplanet_user',
  password : 'your_password',
  database : 'exoplanet_explorer'
});

connection.connect(err => {
  if (err) {
    return console.error('error connecting: ' + err.stack);
  }
  console.log('connected as id ' + connection.threadId);
});

// Use `connection` to interact with the database
