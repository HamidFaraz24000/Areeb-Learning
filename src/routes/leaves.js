const express = require('express');
const pool = require('../db');
const { LEAVE_TYPES, DECISION_STATUSES, isPositiveId, isValidDate, missingFields, error } = require('../utils');

const router = express.Router();
const leaveSelect = `SELECT l.id, l.employee_id AS employeeId, e.name AS employeeName,
  e.department AS employeeDepartment, l.leave_type AS leaveType,
  DATE_FORMAT(l.start_date, '%Y-%m-%d') AS startDate,
  DATE_FORMAT(l.end_date, '%Y-%m-%d') AS endDate, l.reason, l.status,
  l.manager_id AS managerId, l.created_at AS createdAt, l.updated_at AS updatedAt
  FROM leave_requests l JOIN employees e ON e.id = l.employee_id`;

router.get('/summary', async (req, res, next) => {
  try {
    const [rows] = await pool.execute(`SELECT COUNT(*) AS totalRequests,
      COALESCE(SUM(status = 'pending'), 0) AS pendingRequests,
      COALESCE(SUM(status = 'approved'), 0) AS approvedRequests,
      COALESCE(SUM(status = 'rejected'), 0) AS rejectedRequests
      FROM leave_requests`);
    res.json(rows[0]);
  } catch (err) { next(err); }
});

router.get('/department-summary', async (req, res, next) => {
  try {
    const [rows] = await pool.execute(`SELECT e.department, COUNT(l.id) AS totalRequests
      FROM employees e JOIN leave_requests l ON l.employee_id = e.id
      GROUP BY e.department ORDER BY e.department`);
    res.json(rows);
  } catch (err) { next(err); }
});

router.post('/', async (req, res, next) => {
  try {
    const missing = missingFields(req.body, ['employeeId', 'leaveType', 'startDate', 'endDate', 'reason']);
    if (missing.length) throw error(`Required fields missing: ${missing.join(', ')}`);
    const { employeeId, leaveType, startDate, endDate, reason } = req.body;
    if (!isPositiveId(employeeId)) throw error('employeeId must be a positive integer');
    if (!LEAVE_TYPES.includes(leaveType)) throw error('Leave type must be sick, casual, or annual');
    if (!isValidDate(startDate) || !isValidDate(endDate)) throw error('Start date and end date must use YYYY-MM-DD format');
    if (startDate > endDate) throw error('Start date cannot be after end date');
    const [employees] = await pool.execute('SELECT id FROM employees WHERE id = ?', [employeeId]);
    if (!employees.length) throw error('Employee not found', 404);
    const [result] = await pool.execute(
      `INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason, status)
       VALUES (?, ?, ?, ?, ?, 'pending')`,
      [employeeId, leaveType, startDate, endDate, reason.trim()]
    );
    const [rows] = await pool.execute(`${leaveSelect} WHERE l.id = ?`, [result.insertId]);
    res.status(201).json({ success: true, data: rows[0] });
  } catch (err) { next(err); }
});

router.get('/', async (req, res, next) => {
  try {
    const clauses = [], params = [];
    const { status, department, employeeId } = req.query;
    if (status) {
      if (!['pending', ...DECISION_STATUSES].includes(status)) throw error('Status must be pending, approved, or rejected');
      clauses.push('l.status = ?'); params.push(status);
    }
    if (department) { clauses.push('e.department = ?'); params.push(department); }
    if (employeeId) {
      if (!isPositiveId(employeeId)) throw error('employeeId must be a positive integer');
      clauses.push('l.employee_id = ?'); params.push(employeeId);
    }
    const where = clauses.length ? ` WHERE ${clauses.join(' AND ')}` : '';
    const [rows] = await pool.execute(`${leaveSelect}${where} ORDER BY l.id DESC`, params);
    res.json({ success: true, data: rows });
  } catch (err) { next(err); }
});

router.get('/:id', async (req, res, next) => {
  try {
    if (!isPositiveId(req.params.id)) throw error('Leave request ID must be a positive integer');
    const [rows] = await pool.execute(`${leaveSelect} WHERE l.id = ?`, [req.params.id]);
    if (!rows.length) throw error('Leave request not found', 404);
    res.json({ success: true, data: rows[0] });
  } catch (err) { next(err); }
});

router.patch('/:id/status', async (req, res, next) => {
  try {
    if (!isPositiveId(req.params.id)) throw error('Leave request ID must be a positive integer');
    const { managerId, status } = req.body;
    if (!isPositiveId(managerId)) throw error('managerId must be a positive integer');
    if (!DECISION_STATUSES.includes(status)) throw error('Status must be approved or rejected');
    const [leaves] = await pool.execute('SELECT id, status FROM leave_requests WHERE id = ?', [req.params.id]);
    if (!leaves.length) throw error('Leave request not found', 404);
    if (leaves[0].status !== 'pending') throw error('This leave request has already been decided');
    const [managers] = await pool.execute('SELECT id FROM employees WHERE id = ? AND role = \'manager\'', [managerId]);
    if (!managers.length) throw error('Manager not found or employee is not a manager', 404);
    await pool.execute('UPDATE leave_requests SET status = ?, manager_id = ? WHERE id = ?', [status, managerId, req.params.id]);
    const [rows] = await pool.execute(`${leaveSelect} WHERE l.id = ?`, [req.params.id]);
    res.json({ success: true, data: rows[0] });
  } catch (err) { next(err); }
});

router.delete('/:id', async (req, res, next) => {
  try {
    if (!isPositiveId(req.params.id)) throw error('Leave request ID must be a positive integer');
    const [result] = await pool.execute('DELETE FROM leave_requests WHERE id = ?', [req.params.id]);
    if (!result.affectedRows) throw error('Leave request not found', 404);
    res.json({ success: true, message: 'Leave request deleted' });
  } catch (err) { next(err); }
});

module.exports = router;
