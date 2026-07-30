const ROLES = ['employee', 'manager'];
const LEAVE_TYPES = ['sick', 'casual', 'annual'];
const DECISION_STATUSES = ['approved', 'rejected'];

function isPositiveId(value) {
  return Number.isInteger(Number(value)) && Number(value) > 0;
}

function isValidDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const [year, month, day] = value.split('-').map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCFullYear() === year && date.getUTCMonth() === month - 1 && date.getUTCDate() === day;
}

function missingFields(body, fields) {
  return fields.filter((field) => !body[field] || (typeof body[field] === 'string' && !body[field].trim()));
}

function error(message, status = 400) {
  const err = new Error(message);
  err.status = status;
  return err;
}

module.exports = { ROLES, LEAVE_TYPES, DECISION_STATUSES, isPositiveId, isValidDate, missingFields, error };
