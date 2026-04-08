CREATE OR ALTER PROCEDURE dbo.DepSalary @dep_id [int] = 11 AS
DECLARE @total_salary INT;
DECLARE @ErrMsg VARCHAR(500);
	BEGIN
		BEGIN TRY
			SET @ErrMsg = 'Duplicate records are found in emp_salary table'

			IF EXISTS (SELECT 1 FROM dbo.emp_salary GROUP BY emp_id HAVING COUNT(*) > 1)
			THROW 50004, @ErrMsg, 1;
	
			IF EXISTS(SELECT 1 FROM dbo.emp_salary WHERE dept_id = @dep_id AND salary IS NULL)
			BEGIN
				UPDATE dbo.emp_salary
				SET salary = 0
				WHERE dept_id = @dep_id AND salary IS NULL;
			END 
			ELSE
			BEGIN
				PRINT'No records with NULL salary'
			END

			SELECT @total_salary = AVG(cast(salary as int))
			FROM dbo.emp_salary
			WHERE dept_id = @dep_id
			GROUP BY dept_id

			SELECT dept_id, AVG(cast(salary as int)) AS avg_salary
			FROM dbo.emp_salary
			WHERE dept_id = @dep_id
			GROUP BY dept_id

			PRINT 'Avg Salary of the department ' + CAST(@dep_id AS NVARCHAR(10))
			+ ' :' + CAST(@total_salary  AS NVARCHAR(10))
		END TRY
		BEGIN CATCH
			PRINT('ERROR_NUMBER: ' + cast(ERROR_NUMBER() as varchar(200)))
			PRINT('ERROR_SEVERITY: ' + cast(ERROR_SEVERITY() as varchar(200)))
			PRINT('ERROR_STATE: ' + cast(ERROR_STATE() as varchar(200)))
			PRINT('ERROR_PROCEDURE: ' + cast(ERROR_PROCEDURE() as varchar(200)))
			PRINT('ERROR_LINE: ' + cast(ERROR_LINE() as varchar(200)))
			PRINT('ERROR_MESSAGE: ' + cast(ERROR_MESSAGE() as varchar(200)))
		END CATCH
END;

EXEC dbo.DepSalary 11

UPDATE dbo.emp_salary SET salary = NULL WHERE name ='cat'

SELECT * FROM dbo.emp_salary;

INSERT INTO dbo.emp_salary VALUES (104, 'cat', 120, 21)
