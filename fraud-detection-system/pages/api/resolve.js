const { connect, getConnection, r } = require('../../lib/rethinkdb');

export default async function handler(req, res) {
  const { transNum } = req.body;
  console.log('resolving ', transNum);
  try {
    await connect()
    const conn = getConnection();
    const result = await r.table('transactions')
        .filter(r.row("trans_num").eq(transNum))
        .update({ status: 'resolved' })
        .run(conn);
    res.status(200).json({'status': true, 'data': result});
  } catch (error) {
    console.error('Error resolving transaction:', error);
    res.status(500).json({ error: 'Error resolving transaction' });
  }
}
