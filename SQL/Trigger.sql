/*
Types of Trigger
1. DML Trigger
	1. After 
	2. Instead of 
2. DDL Trigger
3. Loggon Trigger

Use Case: Audit tables
*/
CREATE TRIGGER dbo.tr_employee on dbo.Employee
AFTER INSERT AS
BEGIN
	INSERT INTO dbo.EmployeeLogs (EmployeeID, LogMessage, LogDate)
	SELECT EmpID, concat('New Employee ', EmpName, ' inserted'), cast(GETDATE() as date) 
	FROM INSERTED
END;

SELECT * FROM dbo.Employee;
SELECT * FROM dbo.EmployeeLogs

INSERT INTO dbo.Employee VALUES (1, 'Mohan', 10)