<img width="1683" height="504" alt="image" src="https://github.com/user-attachments/assets/2dd131c4-ee25-4160-ac8a-55b4d51d8a00" />

## Difference between OLTP and OLAP
OLTP and OLAP are two different types of database systems designed for **very different workloads and goals**.

***

### OLTP (Online Transaction Processing)

**Purpose:**  
Handle **day-to-day transactional operations** efficiently and reliably.

**Key Characteristics:**

*   Focuses on **insert, update, delete, and short read operations**
*   Handles a **large number of concurrent users**
*   Transactions are **small, fast, and frequent**
*   Strong emphasis on **data integrity, consistency, and ACID compliance**

**Typical Use Cases:**

*   Banking transactions (deposits, withdrawals)
*   E-commerce orders
*   Ticket bookings
*   Payroll systems

**Example Query:**

```sql
UPDATE Orders
SET status = 'Shipped'
WHERE order_id = 12345;
```

***

### OLAP (Online Analytical Processing)

**Purpose:**  
Support **data analysis, reporting, and decision-making**.

**Key Characteristics:**

*   Focuses on **read-heavy, complex queries**
*   Works with **large volumes of historical data**
*   Queries are **long-running and computation-intensive**
*   Optimized for **aggregations, trends, and insights**

**Typical Use Cases:**

*   Sales performance analysis
*   Business intelligence dashboards
*   Financial forecasting
*   Data warehousing

**Example Query:**

```sql
SELECT region, SUM(sales_amount)
FROM sales_fact
GROUP BY region;
```

***

| Aspect           | OLTP                           | OLAP                                |
| ---------------- | ------------------------------ | ----------------------------------- |
| Primary Goal     | Transaction processing         | Data analysis                       |
| Data Type        | Current, operational data      | Historical, aggregated data         |
| Operations       | INSERT, UPDATE, DELETE         | SELECT (complex queries)            |
| Query Complexity | Simple                         | Complex                             |
| Data Volume      | Small to medium                | Very large                          |
| Users            | Many concurrent users          | Fewer users (analysts, managers)    |
| Response Time    | Milliseconds                   | Seconds to minutes                  |
| Schema Design    | Highly normalized              | Denormalized (Star/Snowflake)       |
| Example Systems  | MySQL, PostgreSQL, Oracle OLTP | Snowflake, Redshift, BigQuery, SSAS |


## Explain the following terms
### 1. **Data Redundancy**

**Definition:**  
Data redundancy refers to the **unnecessary duplication of the same data** in multiple places within a database or across systems.

**Why it occurs:**

*   Poor database design
*   Lack of normalization
*   Storing the same data in different tables or files

**Problems caused:**

*   Wasted storage space
*   Increased maintenance effort
*   Higher risk of inconsistencies

**Example:**  
If a customer’s phone number is stored in:

*   `Orders` table
*   `Customers` table
*   `Invoices` table

➡ The same data is repeated multiple times.

***

### 2. **Data Inconsistency**

**Definition:**  
Data inconsistency occurs when **different copies of the same data do not match**, leading to conflicting information.

**Relationship with data redundancy:**  
Data inconsistency is often a **result of data redundancy**.

**Problems caused:**

*   Incorrect reports
*   Wrong business decisions
*   Loss of data reliability

**Example:**  
A customer’s address:

*   Updated in the `Customers` table
*   Not updated in the `Orders` table

➡ The system shows two different addresses for the same customer.

***

### 3. **Data Integration**

**Definition:**  
Data integration is the process of **combining data from multiple sources** into a **single, unified view**.

**Purpose:**

*   Enable consistent reporting
*   Improve data quality
*   Support analytics and decision-making

**Common data sources:**

*   Databases
*   Flat files (CSV, Excel)
*   APIs
*   Cloud applications

**Example:**  
Combining:

*   Sales data from an ERP system
*   Customer data from a CRM
*   Marketing data from online platforms

➡ Loaded into a **data warehouse** for reporting.

***

### 4. **Data Normalisation**

**Definition:**  
Data normalization is the process of **organizing data in a database to reduce redundancy and improve data integrity**.

**How it works:**

*   Breaks large tables into smaller, related tables
*   Uses relationships (primary key & foreign key)
*   Stores each piece of data in only one place

**Benefits:**

*   Reduces data redundancy
*   Prevents data inconsistency
*   Makes updates easier and safer

**Example:**  
Instead of storing customer details in every order:

*   `Customers` table → customer info
*   `Orders` table → order info with customer ID

➡ Customer data is maintained in one place.
***

### Keys:
Here are **clear, concise explanations** of the different types of database keys, with examples (exam‑ and interview‑friendly).

***

## **Keys**

***

### 1. Primary Key

**Definition:**  
A **primary key** is a column (or set of columns) that **uniquely identifies each record** in a table.

**Key Properties:**

*   Must be **unique**
*   Cannot be **NULL**
*   Only **one primary key** per table
*   Ensures **entity integrity**

**Example:**

```text
Customers Table
----------------
CustomerID (PK)
CustomerName
Email
```

Here, `CustomerID` uniquely identifies each customer.

***

### 2. Foreign Key

**Definition:**  
A **foreign key** is a column in one table that **refers to the primary key of another table**, establishing a relationship between tables.

**Key Properties:**

*   Can contain duplicate values
*   Can be NULL (depending on design)
*   Enforces **referential integrity**

**Example:**

```text
Orders Table
------------
OrderID (PK)
OrderDate
CustomerID (FK)
```

`CustomerID` in the `Orders` table references `CustomerID` in the `Customers` table.

➡ This means *every order must belong to a valid customer*.

***

### 3. Surrogate Key

**Definition:**  
A **surrogate key** is an **artificial, system-generated key** with no business meaning, used only for identification.

**Key Properties:**

*   Usually numeric (Auto Increment / Identity)
*   Immutable (never changes)
*   Preferred in **data warehouses and OLAP systems**

**Why use it?**

*   Business data may change
*   Improves performance and joins
*   Simplifies ETL processes

**Example:**

```text
Employee Table
--------------
EmployeeSK (Surrogate Key)
EmployeeCode (Business Key)
Name
```

`EmployeeSK` is generated by the system and has no real-world meaning.

***

### 4. Business Key

**Definition:**  
A **business key** (also called a natural key) is a column that **has business meaning** and uniquely identifies an entity.

**Key Properties:**

*   Comes from real business data
*   Can change over time
*   May be composite (multiple columns)

**Example:**

*   Employee Email ID
*   Aadhaar Number
*   Customer Account Number

```text
Employee Table
--------------
EmployeeCode (Business Key)
Name
Department
```

`EmployeeCode` is meaningful to the business and unique.

***

### Primary vs Surrogate vs Business Key

| Aspect           | Primary Key               | Surrogate Key               | Business Key                  |
| ---------------- | ------------------------- | --------------------------- | ----------------------------- |
| Purpose          | Uniquely identify records | System-level identification | Business-level identification |
| Business Meaning | May or may not            | ❌ No                        | ✅ Yes                         |
| Can Change       | No                        | No                          | Possibly                      |
| Common Usage     | OLTP systems              | Data warehouses             | Master data                   |

***

### Important Note

*   A **primary key** can be either:
    *   a **business key**, or
    *   a **surrogate key**
*   In modern systems:
    *   **OLTP** → often business keys
    *   **OLAP / Data Warehouse** → surrogate keys

***


### What is data modeling?
Data modeling is the process of designing how data is structured and related before storing it in a database or warehouse.  
It answers:
1. What tables do we need?
2. What columns should each table have?
3. How are tables connected?
4. What is fact and what is dimension

### Dimensional data modeling
1. **Star Schema**
2. **Snowflake Schema**
3. **Fact Table**
4. **Dimension Table**

### Types of Fact Table

### Slowly changing dimension

### Types of Dimensions

### How Do You Handle Late Arriving Dimension?
1. Create dummy record and update later
2. Delay fact load
3. Use inferred members

Most common approach: Create placeholder record and update when dimension arrives.

### Which should be loaded first: Fact table or Dimension table?
- Dimension tables should be loaded before fact tables.
- Because fact tables contain foreign keys that reference dimension tables.

### What Datawarehouse
#### Traditional VS Modern Datawarehouse
#### Characterstics:


### ETL and ELT

### Data Mart
