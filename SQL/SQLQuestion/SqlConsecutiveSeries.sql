-- Consecutive Sequence

-----------------------------------------------------------------------------------------------------
/*
Problem 1: Seating Chart

Given the set of integers provided in the following DDL statement, write the SQL statements to determine the following:
    1. 4 consecutive number
    2. Series start and end
    2. Gap start and end

Expected Output:

GapStart	GapEnd
1	           6
8	           12
16	           26
36	           51

*/
-- Table Creation
DROP TABLE IF EXISTS #SeatingChart;

CREATE TABLE #SeatingChart (SeatNumber INTEGER);

INSERT INTO #SeatingChart VALUES
(1), (7),(13),(14),(15),(16), (27),(28),(29),(30),
(31),(33),(34),(35),(52),(53),(54);

-- Solution 1
With Gap AS
(
SELECT SeatNumber, SeatNumber - ROW_NUMBER() OVER(ORDER BY SeatNumber) rowDiff
FROM #SeatingChart
)
SELECT SeatNumber 
FROM (
    SELECT SeatNumber, COUNT(*) OVER(PARTITION BY rowDiff) as Cnt
    FROM Gap
) a 
WHERE Cnt >=4

-- Solution 2
SELECT MIN(SeatNumber) SeriesStart, MAX(SeatNumber) SeriesEnd
FROM (
SELECT SeatNumber, SeatNumber - ROW_NUMBER() OVER(ORDER BY SeatNumber) diff
FROM #SeatingChart
) a
GROUP BY diff

-- Solution 3
SELECT PreSeatNumber + 1 AS StartSeries, SeatNumber - 1 AS EndSeries
FROM (
SELECT ISNULL(LAG(SeatNumber) OVER(ORDER BY SeatNumber), 0) PreSeatNumber, SeatNumber,
(SeatNumber - ISNULL(LAG(SeatNumber) OVER(ORDER BY SeatNumber), 0)) diff
FROM #SeatingChart
) a
WHERE diff > 1

-----------------------------------------------------------------------------------------------------
/*
Problem 2: Consecutive Number
Table: Logs

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
In SQL, id is the primary key for this table.
id is an autoincrement column starting from 1.
Find all numbers that appear at least three times consecutively.

Input: 
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
Output: 
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
Explanation: 1 is the only number that appears consecutively for at least three times.
*/

-- Table creation
DROP TABLE IF EXISTS #NumTable;

CREATE TABLE #NumTable (
    id INT,
    num INT
);

-- Insert data
INSERT INTO #NumTable (id, num) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 2),
(5, 1),
(6, 2),
(7, 2);

-- Solution

SELECT DISTINCT num
FROM (
SELECT id, num, ROW_NUMBER() OVER(PARTITION BY num ORDER BY id) AS rowNum,
(id - ROW_NUMBER() OVER(PARTITION BY num ORDER BY id)) as gap
FROM #NumTable
) a
GROUP BY num, gap
HAVING COUNT(*) >= 3

-----------------------------------------------------------------------------------------------------
/*
Problem 3
+------+------------+
| Name | Repetition |
+------+------------+
| A    |          2 |
| B    |          4 |
| C    |          1 |
| B    |          2 |
+------+------------+
*/
DROP TABLE IF EXISTS #t;

create table #t (Id int, Name char)

insert into #t values
(1, 'A'),
(2, 'A'),
(3, 'B'),
(4, 'B'),
(5, 'B'),
(6, 'B'),
(7, 'C'),
(8, 'B'),
(9, 'B')

SELECT NAME, COUNT(*) AS cnt
FROM (
SELECT NAME, (Id - ROW_NUMBER() OVER(PARTITION BY Name ORDER BY Id)) as rowNumDiff
FROM #t
) t
GROUP BY NAME, rowNumDiff


/*
Problem 4:
Find ranges of consecutive dates for each user.

Input – UserLogins

| user_id | login_date |
| -------- | ----------- |
| A        | 2024‑01‑01  |
| A        | 2024‑01‑02  |
| A        | 2024‑01‑04  |
| A        | 2024‑01‑05  |
| B        | 2024‑01‑10  |

Expected Output

| user_id | start_date | end_date  |
| -------- | ----------- | ---------- |
| A        | 2024‑01‑01  | 2024‑01‑02 |
| A        | 2024‑01‑04  | 2024‑01‑05 |
| B        | 2024‑01‑10  | 2024‑01‑10 |
*/

-- Create temp table
IF OBJECT_ID('tempdb..#UserLogins') IS NOT NULL
    DROP TABLE #UserLogins;

CREATE TABLE #UserLogins (
    user_id VARCHAR(10),
    login_date DATE
);

-- Insert sample data
INSERT INTO #UserLogins (user_id, login_date)
VALUES
    ('A', '2024-01-01'),
    ('A', '2024-01-02'),
    ('A', '2024-01-04'),
    ('A', '2024-01-05'),
    ('B', '2024-01-10');

SELECT user_id, MIN(login_date) start_date, MAX(login_date) end_date
FROM (
SELECT user_id,
	login_date,
	rowNum,
	DATEADD(DAY, - 1 * rowNum, login_date) AS Dt
FROM (
	SELECT user_id,
		login_date,
		ROW_NUMBER() OVER (
			PARTITION BY USER_ID ORDER BY login_date
			) AS rowNum
	FROM #UserLogins
	) a
) b
GROUP BY user_id, Dt

/*
Problem 5:

Find user who logins at least 3 consecutive days.

Input – UserLogins

| user_id | login_date |
| -------- | ----------- |
| A        | 2024‑01‑01  |
| A        | 2024‑01‑02  |
| A        | 2024‑01‑04  |
| A        | 2024‑01‑05  |
| B        | 2024‑01‑10  |

*/
-- Create temp table
IF OBJECT_ID('tempdb..#UserLogins') IS NOT NULL
    DROP TABLE #UserLogins;

CREATE TABLE #UserLogins (
    user_id VARCHAR(10),
    login_date DATE
);

-- Insert sample data
INSERT INTO #UserLogins (user_id, login_date)
VALUES
    ('A', '2024-01-01'),
    ('A', '2024-01-02'),
    ('A', '2024-01-03'),
    ('A', '2024-01-05'),
    ('B', '2024-01-10'),
    ('B', '2024-01-10')

-- Solution
SELECT user_id
FROM (
SELECT user_id, login_date, 
DATEADD(day, -1 * ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_date), login_date) AS dateadd
FROM #UserLogins
) a
GROUP BY user_id, dateadd
HAVING COUNT(*) >= 3

/*
Problem 6:
For each user, you must find the longest sequence of days where the user logged in continuously without missing any day.
This is also called the maximum consecutive login streak.

Find user who logins at least 3 consecutive days.

Input – UserLogins

| user_id | login_date |
| -------- | ----------- |
| A        | 2024‑01‑01  |
| A        | 2024‑01‑02  |
| A        | 2024‑01‑03  |
| A        | 2024‑01‑05  |
| B        | 2024‑01‑10  |
| B        | 2024‑01‑11  |
*/

-- Drop temp table if it already exists
IF OBJECT_ID('tempdb..#UserLogins') IS NOT NULL
    DROP TABLE #UserLogins;

-- Create temp table
CREATE TABLE #UserLogins (
    user_id VARCHAR(10),
    login_date DATE
);

-- Insert data
INSERT INTO #UserLogins (user_id, login_date)
VALUES
    ('A', '2024-01-01'),
    ('A', '2024-01-02'),
    ('A', '2024-01-03'),
    ('A', '2024-01-05'),
    ('B', '2024-01-10'),
    ('B', '2024-01-11');

SELECT user_id,
	MAX(cnt) MaxLoginStreak
FROM (
	SELECT user_id,
		COUNT(*) AS cnt
	FROM (
		SELECT user_id,
			login_date,
			DATEADD(day, - 1 * ROW_NUMBER() OVER (
					PARTITION BY user_id ORDER BY login_date
					), login_date) AS DayAdd
		FROM #UserLogins
		) a
	GROUP BY user_id,
		DayAdd
	) b
GROUP BY [user_id]

/*
Problem 7:
Given attendance per day, find employees absent 3 or more consecutive days.

Input – Attendance

| emp_id | day | status |
| ------- | --- | ------ |
| 10      | 1   | P      |
| 10      | 2   | A      |
| 10      | 3   | A      |
| 10      | 4   | A      |
| 10      | 5   | P      |

Expected Output

| emp_id | start_day | end_day | count |
| ------- | ---------- | -------- | ----- |
| 10      | 2          | 4        | 3     |
*/

-- Drop temp table if exists
IF OBJECT_ID('tempdb..#Attendance') IS NOT NULL
    DROP TABLE #Attendance;

-- Create temp table
CREATE TABLE #Attendance (
    emp_id INT,
    day INT,
    status CHAR(1)   -- P = Present, A = Absent
);

-- Insert more test data
INSERT INTO #Attendance (emp_id, day, status)
VALUES
    -- Employee 10
    (10, 1, 'P'),
    (10, 2, 'A'),
    (10, 3, 'A'),
    (10, 4, 'A'),
    (10, 5, 'P'),
    (10, 6, 'A'),
    (10, 7, 'A'),

    -- Employee 20: multiple scattered absences
    (20, 1, 'A'),
    (20, 2, 'P'),
    (20, 3, 'A'),
    (20, 4, 'A'),
    (20, 5, 'P'),
    (20, 6, 'A'),
    (20, 7, 'P'),

    -- Employee 30: long absence streak
    (30, 1, 'A'),
    (30, 2, 'A'),
    (30, 3, 'A'),
    (30, 4, 'A'),
    (30, 5, 'A'),
    
    -- Employee 40: no absences
    (40, 1, 'P'),
    (40, 2, 'P'),
    (40, 3, 'P'),

    -- Employee 50: small streaks
    (50, 1, 'A'),
    (50, 2, 'A'),
    (50, 3, 'P'),
    (50, 4, 'A'),
    (50, 5, 'A'),
    (50, 6, 'A');

SELECT emp_id, MIN(day) AS start_day, MAX(day) end_day, count(day) AS count
FROM (
SELECT emp_id, day, (day - ROW_NUMBER() OVER(PARTITION BY emp_id ORDER BY day)) AS dayDiff
FROM #Attendance 
WHERE [status] = 'A'
) emp
GROUP BY emp_id, dayDiff
HAVING COUNT(*) >= 3
ORDER BY 1

/*
Problem 8:
Group consecutive integer IDs into ranges.

Input

| id  |
| --- |
| 100 |
| 101 |
| 102 |
| 200 |
| 202 |
| 203 |
| 204 |

Expected Output:

| start_id | end_id |
| --------- | ------- |
| 100       | 102     |
| 200       | 200     |
| 202       | 204     |
*/

-- Drop temp table if already exists
IF OBJECT_ID('tempdb..#IDs') IS NOT NULL
    DROP TABLE #IDs;

-- Create temp table
CREATE TABLE #IDs (
    id INT
);

-- Insert sample data
INSERT INTO #IDs (id)
VALUES
    (100),
    (101),
    (102),
    (200),
    (202),
    (203),
    (204);

SELECT MIN(id) AS start_id, MAX(id) AS end_id
FROM (
SELECT id, ROW_NUMBER() OVER(ORDER BY id) AS row_num,
(id - ROW_NUMBER() OVER(ORDER BY id)) AS diff
FROM #IDs
) a
GROUP BY diff

/*
Problem 9
Find streaks where the stock price decreased consecutively.

### Input

| dt | price |
| -- | ----- |
| 1  | 100   |
| 2  | 98    |
| 3  | 97    |
| 4  | 99    |
| 5  | 95    |
| 6  | 94    |

### Expected Output

| start | end | length |
| ----- | --- | ------ |
| 1     | 3   | 3      |
| 4     | 6   | 3      |

*/

-- Drop temp table if it already exists
IF OBJECT_ID('tempdb..#StockPrices') IS NOT NULL
    DROP TABLE #StockPrices;

-- Create temp table
CREATE TABLE #StockPrices (
    dt INT,        -- day or timestamp index
    price INT      -- stock price
);

-- Insert sample data
INSERT INTO #StockPrices (dt, price)
VALUES
    (1, 100),
    (2, 102),
    (3, 97),
    (4, 96),
    (5, 99),
    (6, 98),
    (7, 97);

SELECT MIN(dt) - 1 AS start_date, MAX(dt) AS end_date, COUNT(*) + 1 AS length
FROM (
SELECT dt, price, ROW_NUMBER() OVER(ORDER BY dt) row_num, (dt - ROW_NUMBER() OVER(ORDER BY dt)) AS dayDiff
FROM (
SELECT dt, price, CASE WHEN LAG(price) OVER(ORDER BY dt) > price THEN 1 ELSE 0 END  AS flag
FROM #StockPrices
) a
WHERE flag = 1
) b
GROUP BY dayDiff
HAVING COUNT(*) >= 2;

-- Solution 2
WITH cte AS (
    SELECT
        dt,
        price,
        LAG(price) OVER (ORDER BY dt) AS prev_price
    FROM #StockPrices
),
flags AS (
    SELECT
        dt,
        price,
        CASE WHEN price < prev_price THEN 0 ELSE 1 END AS break_flag
    FROM cte
),
groups AS (
    SELECT
        dt,
        price,
        SUM(break_flag) OVER (ORDER BY dt ROWS UNBOUNDED PRECEDING) AS grp
    FROM flags
),
final AS (
    SELECT
        MIN(dt) AS start_dt,
        MAX(dt) AS end_dt,
        COUNT(*) AS length
    FROM groups
    GROUP BY grp
)
SELECT *
FROM final
WHERE length > 1
ORDER BY start_dt;

/*
Problem 10
Detect runs of the same value.

### **Input**

| event |
| ----- |
| A     |
| A     |
| B     |
| B     |
| B     |
| C     |
| A     |

### **Expected Output**

| event | start_row | end_row | count |
| ----- | ---------- | -------- | ----- |
| A     | 1          | 2        | 2     |
| B     | 3          | 5        | 3     |
| C     | 6          | 6        | 1     |
| A     | 7          | 7        | 1     |
*/

-- Drop temp table if it exists
IF OBJECT_ID('tempdb..#Events') IS NOT NULL
    DROP TABLE #Events;

-- Create temp table
CREATE TABLE #Events (
    event CHAR(1)
);

-- Insert sample data
INSERT INTO #Events (event)
VALUES
    ('A'),
    ('A'),
    ('B'),
    ('B'),
    ('B'),
    ('C'),
    ('A');

WITH Events
AS (
	SELECT event,
		ROW_NUMBER() OVER (
			ORDER BY (
					SELECT 1
					)
			) AS rowNum
	FROM #Events
	)
SELECT event,
	MIN(rowNum) start_row,
	MAX(rowNum) end_row
FROM (
	SELECT event,
		rowNum,
		(
			rowNum - ROW_NUMBER() OVER (
				PARTITION BY event ORDER BY rowNum
				)
			) rowDiff
	FROM Events
	) a
GROUP BY event,
	rowDiff
HAVING COUNT(*) > 1

/*
Problem 11
Group consecutive timestamps where the gap between rows is ≤ 1 hour.

Input

| ts    |
| ----- |
| 10:00 |
| 10:30 |
| 11:00 |
| 13:00 |
| 13:30 |

Expected Output

| start | end   |
| ----- | ----- |
| 10:00 | 11:00 |
| 13:00 | 13:30 |
*/

-- Drop temp table if it exists
IF OBJECT_ID('tempdb..#TimeStamps') IS NOT NULL
    DROP TABLE #TimeStamps;

-- Create temp table
CREATE TABLE #TimeStamps (
    ts TIME
);

-- Insert sample data
INSERT INTO #TimeStamps (ts)
VALUES
    ('10:00'),
    ('10:30'),
    ('11:00'),
    ('13:00'),
    ('13:30');
SELECT MIN(ts) start_time, MAX(ts) end_time
FROM (
SELECT ts, SUM(flag) OVER(ORDER BY ts) AS st
FROM (
SELECT ts,  CASE WHEN DATEDIFF(MINUTE, LAG(ts) OVER(ORDER BY ts), ts) <= 60 THEN 0  ELSE 1 END AS flag
FROM #TimeStamps
) t
) o 
GROUP BY st


/*
Problem 12
Find each player's longest win streak.

Input

| player | match | result |
| ------ | ----- | ------ |
| A      | 1     | W      |
| A      | 2     | W      |
| A      | 3     | L      |
| A      | 4     | W      |
| A      | 5     | W      |
| A      | 6     | W      |

Expected Output

| player | max\_win_streak |
| ------ | ---------------- |
| A      | 3                |

*/

-- Drop temp table if it already exists
IF OBJECT_ID('tempdb..#GameResults') IS NOT NULL
    DROP TABLE #GameResults;

-- Create temp table
CREATE TABLE #GameResults (
    player VARCHAR(10),
    match_no INT,
    result CHAR(1)   -- W = Win, L = Loss
);

-- Insert sample data
INSERT INTO #GameResults (player, match_no, result)
VALUES
    ('A', 1, 'W'),
    ('A', 2, 'W'),
    ('A', 3, 'L'),
    ('A', 4, 'W'),
    ('A', 5, 'W'),
    ('A', 6, 'W');

SELECT player, MAX(total_match) AS max_streak
FROM (
SELECT player, MIN(match_no) AS min_match, MAX(match_no) AS max_match, COUNT(*) AS total_match
FROM (
SELECT Player, match_no, result, (match_no - ROW_NUMBER() OVER(PARTITION BY player ORDER BY match_no)) as rowDiff
FROM #GameResults
WHERE result = 'W'
) a
GROUP BY player, rowDiff
) b
GROUP BY player

-- Problem 2: Consecutive Sequence with condition



-- Problem 2: Find 3 Consecutive IDs With ≥ 100 Students
-- Expected qualifying sequence: IDs 4, 5, 6

DROP TABLE IF EXISTS #StudentCounts;

-- Create temp table
CREATE TABLE #StudentCounts (
    id INT,
    students INT
);

-- Insert data
INSERT INTO #StudentCounts (id, students) VALUES
(1, 4),
(2, 110),
(3, 3),
(4, 120),
(5, 130),
(6, 140);

SELECT id, students
FROM #StudentCounts

SELECT * FROM
(
SELECT id, students, COUNT(*) OVER(PARTITION BY row_diff) cnt
FROM (
SELECT id, students, (id - ROW_NUMBER() OVER(ORDER BY id)) row_diff
FROM #StudentCounts
WHERE students >= 100
) a
) b
WHERE cnt >= 3

/*

*/

-- Temp table
CREATE TABLE #Sales (
    emp_id INT,
    sale_date DATE,
    amount DECIMAL(10,2),
    region VARCHAR(50)
);

-- Sample data
INSERT INTO #Sales (emp_id, sale_date, amount, region) VALUES
(101, '2024-01-01', 100, 'North'),
(101, '2024-01-02', 150, 'North'),
(101, '2024-01-04', 120, 'North'),     -- gap (breaks the island)
(101, '2024-01-05', 200, 'South'),     -- region change (new island)

(102, '2024-02-10', 300, 'East'),
(102, '2024-02-11', 250, 'East'),
(102, '2024-02-13', 180, 'East'),      -- gap
(102, '2024-02-14', 500, 'East'),      -- continues another island

(103, '2024-03-01', 400, 'West'),
(103, '2024-03-02', 450, 'West'),
(103, '2024-03-03', 350, 'South');     -- region change (new island)

SELECT * FROM #Sales