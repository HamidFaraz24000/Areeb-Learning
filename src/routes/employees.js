const express = require('express');
const pool = require('../db');
const { ROLES, isPositiveId, missingFields, error } = require('../utils');

const router = express.Router();

router.post('/', async (req, res, next) => {
  try {
    const missing = missingFields(req.body, ['name', 'email', 'department', 'role']);
    if (missing.length) throw error(`Required fields missing: ${missing.join(', ')}`);
    const { name, email, department, role } = req.body;
    if (!ROLES.includes(role)) throw error('Role must be employee or manager');
    if (!/^\S+@\S+\.\S+$/.test(email.trim())) throw error('Email must be valid');
    const [result] = await pool.execute(
      'INSERT INTO employees (name, email, department, role) VALUES (?, ?, ?, ?)',
      [name.trim(), email.trim().toLowerCase(), department.trim(), role]
    );
    const [rows] = await pool.execute('SELECT * FROM employees WHERE id = ?', [result.insertId]);
    res.status(201).json({ success: true, data: rows[0] });
  } catch (err) { next(err); }
});

router.get('/', async (req, res, next) => {
  try {
    const params = [];
    let sql = 'SELECT * FROM employees';
    if (req.query.department) { sql += ' WHERE department = ?'; params.push(req.query.department); }
    sql += ' ORDER BY id';
    const [rows] = await pool.execute(sql, params);
    res.json({ success: true, data: rows });
  } catch (err) { next(err); }
});

router.get('/:id', async (req, res, next) => {
  try {
    if (!isPositiveId(req.params.id)) throw error('Employee ID must be a positive integer');
    const [rows] = await pool.execute('SELECT * FROM employees WHERE id = ?', [req.params.id]);
    if (!rows.length) throw error('Employee not found', 404);
    res.json({ success: true, data: rows[0] });
  } catch (err) { next(err); }
});

router.put('/:id', async (req, res, next) => {
  try {
    if (!isPositiveId(req.params.id)) throw error('Employee ID must be a positive integer');
    const allowed = ['name', 'email', 'department', 'role'];
    const updates = Object.entries(req.body).filter(([key, value]) => allowed.includes(key) && value !== undefined);
    if (!updates.length) throw error('Provide at least one valid field to update');
    if (req.body.role && !ROLES.includes(req.body.role)) throw error('Role must be employee or manager');
    if (req.body.email && !String(req.body.email).trim()) throw error('Email cannot be empty');
    if (req.body.email && !/^\S+@\S+\.\S+$/.test(String(req.body.email).trim())) throw error('Email must be valid');
    const [exists] = await pool.execute('SELECT id FROM employees WHERE id = ?', [req.params.id]);
    if (!exists.length) throw error('Employee not found', 404);
    const setClause = updates.map(([key]) => `${key} = ?`).join(', ');
    const values = updates.map(([key, value]) => key === 'email' ? String(value).trim().toLowerCase() : typeof value === 'string' ? value.trim() : value);
    await pool.execute(`UPDATE employees SET ${setClause} WHERE id = ?`, [...values, req.params.id]);
    const [rows] = await pool.execute('SELECT * FROM employees WHERE id = ?', [req.params.id]);
    res.json({ success: true, data: rows[0] });
  } catch (err) { next(err); }
});

router.delete('/:id', async (req, res, next) => {
  try {
    if (!isPositiveId(req.params.id)) throw error('Employee ID must be a positive integer');
    const [result] = await pool.execute('DELETE FROM employees WHERE id = ?', [req.params.id]);
    if (!result.affectedRows) throw error('Employee not found', 404);
    res.json({ success: true, message: 'Employee and associated leave requests deleted' });
  } catch (err) { next(err); }
});

module.exports = router;
