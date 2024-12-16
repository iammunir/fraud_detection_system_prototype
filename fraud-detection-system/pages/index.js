import { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Tabs, 
  Tab, 
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle
} from '@mui/material';
import io from 'socket.io-client';
import { connect, getConnection, r } from '../lib/rethinkdb';

let socket;

export default function Home({ initialFraudTransactions, initialNonFraudTransactions,  initialResolvedFraudTransactions}) {
  const [activeTab, setActiveTab] = useState(0);
  const [fraudTransactions, setFraudTransactions] = useState(initialFraudTransactions);
  const [nonFraudTransactions, setNonFraudTransactions] = useState(initialNonFraudTransactions);
  const [resolvedTransactions, setResolvedTransactions] = useState(initialResolvedFraudTransactions);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [currentTransNum, setCurrentTransNum] = useState(null);

  useEffect(() => {
    socketInitializer();
    return () => {
      if (socket) socket.disconnect();
    };
  }, []);

  const socketInitializer = async () => {
    await fetch('/api/socket');
    socket = io();

    socket.on('transactionUpdate', (change) => {
      const transaction = change.new_val;

      if (!transaction) {
        setFraudTransactions([])
        setNonFraudTransactions([])
        setResolvedTransactions([])
      }
      
      if (transaction.is_fraud && !transaction.status) {
        setFraudTransactions(prev => [...prev, transaction]);
      } else if (!transaction.is_fraud) {
        setNonFraudTransactions(prev => [...prev, transaction]);
      } else if (transaction.status === 'resolved') {
        setFraudTransactions(prev => 
          prev.filter(t => t.trans_num !== transaction.trans_num)
        );
        setResolvedTransactions(prev => [...prev, transaction]);
      }
    });
  };

  const handleResolveClick = (transNum) => {
    setCurrentTransNum(transNum);
    setDialogOpen(true);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setCurrentTransNum(null);
  };

  const handleConfirmResolve = async () => {
    console.log('resolve ', currentTransNum);
    if (currentTransNum) {
      if (currentTransNum) {
        try {
          const response = await fetch('/api/resolve', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ transNum: currentTransNum }),
          });
          const res = await response.json();
          console.log(res);
        } catch (error) {
          console.error('Error resolving transaction:', error);
        }
      }
    }
    handleDialogClose();
  };

  const TransactionTable = ({ transactions, showResolve }) => (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Transaction Number</TableCell>
            <TableCell>Date</TableCell>
            <TableCell>Time</TableCell>
            <TableCell>Amount</TableCell>
            <TableCell>Merchant</TableCell>
            <TableCell>Customer</TableCell>
            <TableCell>Category</TableCell>
            {showResolve && <TableCell>Action</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions.map((transaction) => (
            <TableRow key={transaction.trans_num}>
              <TableCell>{transaction.trans_num}</TableCell>
              <TableCell>{transaction.trans_date}</TableCell>
              <TableCell>{transaction.trans_time}</TableCell>
              <TableCell>${transaction.amt.toFixed(2)}</TableCell>
              <TableCell>{transaction.merchant}</TableCell>
              <TableCell>{`${transaction.first} ${transaction.last}`}</TableCell>
              <TableCell>{transaction.category}</TableCell>
              {showResolve && (
                <TableCell>
                  <Button 
                    variant="contained" 
                    color="primary"
                    onClick={() => handleResolveClick(transaction.trans_num)}
                  >
                    Resolve
                  </Button>
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );

  return (
    <Container maxWidth="lg">
      <Typography variant="h3" component="h1" gutterBottom>
        Fraud Detection System
      </Typography>
      <Typography variant="h6" component="h2" gutterBottom>
        Real-time Transaction Monitoring and Resolution
      </Typography>

      <Paper sx={{ marginTop: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Fraud Transactions" />
          <Tab label="Non-Fraud Transactions" />
          <Tab label="Resolved Transactions" />
        </Tabs>
      </Paper>

      {activeTab === 0 && (
        <TransactionTable 
          transactions={fraudTransactions} 
          showResolve={true}
        />
      )}
      {activeTab === 1 && (
        <TransactionTable 
          transactions={nonFraudTransactions} 
          showResolve={false}
        />
      )}
      {activeTab === 2 && (
        <TransactionTable 
          transactions={resolvedTransactions} 
          showResolve={false}
        />
      )}

      <Dialog
        open={dialogOpen}
        onClose={handleDialogClose}
      >
        <DialogTitle>Confirm Resolve</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to resolve this transaction?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleConfirmResolve} color="primary">
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export async function getServerSideProps() {
  try {
    await connect();
    const conn = getConnection();
    const transactions = await r.table('transactions').run(conn);
    const data = await transactions.toArray();

    const initialFraudTransactions = data.filter(t => t.is_fraud && !t.status);
    const initialNonFraudTransactions = data.filter(t => !t.is_fraud);
    const initialResolvedFraudTransactions = data.filter(t => t.is_fraud && t.status);

    return {
      props: {
        initialFraudTransactions,
        initialNonFraudTransactions,
        initialResolvedFraudTransactions
      },
    };
  } catch (error) {
    console.error('Error fetching initial transactions:', error);
    return {
      props: {
        initialFraudTransactions: [],
        initialNonFraudTransactions: [],
        initialResolvedFraudTransactions: [],
      },
    };
  }
}
