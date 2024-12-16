import { Server } from 'socket.io';
const { connect, getConnection, r } = require('../../lib/rethinkdb');

const ioHandler = async (req, res) => {
  if (!res.socket.server.io) {
    const io = new Server(res.socket.server);
    res.socket.server.io = io;

    await connect();
    const conn = getConnection();

    // Watch for changes in the transactions table
    r.table('transactions')
      .changes()
      .run(conn)
      .then((cursor) => {
        cursor.each((err, change) => {
          if (err) throw err;
          io.emit('transactionUpdate', change);
        });
      });

    io.on('connection', (socket) => {
      console.log('Client connected');
      socket.on('disconnect', () => {
        console.log('Client disconnected');
      });
    });
  }
  res.end();
};

export default ioHandler;
