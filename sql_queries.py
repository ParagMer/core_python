-- 🔹 1. Basic Queries

-- Select all data from a table
SELECT * FROM table_name;

-- Select specific columns
SELECT column1, column2 FROM table_name;

-- Apply WHERE condition
SELECT * FROM table_name WHERE column1 = 'value';

-- Order results ascending or descending
SELECT * FROM table_name ORDER BY column1 ASC;
SELECT * FROM table_name ORDER BY column1 DESC;

-- Limit number of results
SELECT * FROM table_name LIMIT 10;

-- Get unique/distinct values
SELECT DISTINCT column_name FROM table_name;



----------------------------------------------------------------------------------------------------------

-- 🔹 2. INSERT, UPDATE, DELETE

-- Insert a new record
INSERT INTO table_name (column1, column2) VALUES ('value1', 'value2');

-- Update an existing record
UPDATE table_name SET column1 = 'new_value' WHERE column2 = 'some_value';

-- Delete a record
DELETE FROM table_name WHERE column1 = 'value';


----------------------------------------------------------------------------------------------------------



-- 🔹 3. Filtering with WHERE, IN, BETWEEN, LIKE

-- WHERE with AND/OR
SELECT * FROM table_name WHERE column1 = 'A' AND column2 = 'B';
SELECT * FROM table_name WHERE column1 = 'A' OR column2 = 'B';

-- LIKE for pattern matching
SELECT * FROM table_name WHERE column1 LIKE 'A%';    -- starts with A
SELECT * FROM table_name WHERE column1 LIKE '%A';    -- ends with A
SELECT * FROM table_name WHERE column1 LIKE '%A%';   -- contains A

-- BETWEEN for range
SELECT * FROM table_name WHERE column1 BETWEEN 10 AND 20;

-- IN for matching multiple values
SELECT * FROM table_name WHERE column1 IN ('value1', 'value2', 'value3');


----------------------------------------------------------------------------------------------------------


-- 🔹 4. Aggregate Functions

-- Count rows
SELECT COUNT(*) FROM table_name;

-- Sum values
SELECT SUM(column_name) FROM table_name;

-- Average value
SELECT AVG(column_name) FROM table_name;

-- Minimum and maximum
SELECT MIN(column_name), MAX(column_name) FROM table_name;


----------------------------------------------------------------------------------------------------------


-- 🔹 5. GROUP BY and HAVING

-- Group by column and count rows per group
SELECT department, COUNT(*) FROM employees GROUP BY department;

-- Use HAVING to filter groups
SELECT department, COUNT(*) FROM employees
GROUP BY department
HAVING COUNT(*) > 5;



----------------------------------------------------------------------------------------------------------





-- 🔹 6. JOINs

-- INNER JOIN (only matching rows)
SELECT a.*, b.*
FROM table_a a
INNER JOIN table_b b ON a.id = b.a_id;

-- LEFT JOIN (all from left, matching from right)
SELECT a.*, b.*
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id;

-- RIGHT JOIN (all from right, matching from left)
SELECT a.*, b.*
FROM table_a a
RIGHT JOIN table_b b ON a.id = b.a_id;

-- FULL OUTER JOIN (all from both tables - PostgreSQL only)
SELECT a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.a_id;






----------------------------------------------------------------------------------------------------------




-- 🔹 7. Subqueries

-- Subquery in WHERE clause
SELECT * FROM employees
WHERE department_id = (
    SELECT id FROM departments WHERE name = 'IT'
);

-- Subquery in SELECT clause
SELECT name, (
    SELECT COUNT(*) FROM tasks WHERE tasks.emp_id = employees.id
) AS task_count
FROM employees;


----------------------------------------------------------------------------------------------------------



-- 🔹 8. Table & Schema Management

-- Create a new table
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2)
);

-- Drop a table
DROP TABLE employees;

-- Alter a table
ALTER TABLE employees ADD COLUMN join_date DATE;
ALTER TABLE employees MODIFY COLUMN salary DECIMAL(12,2);
ALTER TABLE employees DROP COLUMN join_date;
