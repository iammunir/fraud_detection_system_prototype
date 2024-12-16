const r = require('rethinkdb');

let connection = null;

async function connect() {
  try {
    connection = await r.connect({
      host: process.env.RETHINK_HOST,
      port: process.env.RETHINK_PORT,
      db: process.env.RETHINK_DB,
    });
    console.log('Connected to RethinkDB');
    return connection;
  } catch (error) {
    console.error('Error connecting to RethinkDB:', error);
    throw error;
  }
}

function getConnection() {
    return connection;
}

module.exports = {
  connect,
  getConnection,
  r
};
