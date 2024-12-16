const { connect, getConnection, r } = require('../../lib/rethinkdb');

export default async function handler(req, res) {
  try {
    await connect();
    const conn = getConnection();
    const transactions = await r.table('transactions').run(conn);
    const result = await transactions.toArray();
    res.status(200).json(result);
  } catch (error) {
    console.error('Error fetching transactions:', error);
    res.status(500).json({ error: 'Error fetching transactions' });
  }
}
