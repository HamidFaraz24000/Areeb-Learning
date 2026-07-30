const express = require('express');
const employeesRouter = require('./routes/employees');
const leavesRouter = require('./routes/leaves');

const app = express();
app.use(express.json());

app.get('/health', (req, res) => res.json({ success: true, message: 'API is running' }));
app.use('/api/employees', employeesRouter);
app.use('/api/leaves', leavesRouter);

app.use((req, res) => res.status(404).json({ success: false, message: 'Route not found' }));

app.use((err, req, res, next) => {
  if (err.code === 'ER_DUP_ENTRY') return res.status(400).json({ success: false, message: 'Email already exists' });
  if (err.code === 'ER_NO_REFERENCED_ROW_2') return res.status(404).json({ success: false, message: 'Referenced employee not found' });
  if (err.status) return res.status(err.status).json({ success: false, message: err.message });
  console.error(err);
  return res.status(500).json({ success: false, message: 'Internal server error' });
});

module.exports = app;
