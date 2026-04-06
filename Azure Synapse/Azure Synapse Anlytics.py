# Databricks notebook source
# MAGIC %md
# MAGIC # Azure Synapse Analytics

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. What is Azure Synapse Analytics?
# MAGIC
# MAGIC Azure Synapse is a limitless analytics service that combines:
# MAGIC
# MAGIC *   Enterprise data warehousing
# MAGIC *   Big Data analytics
# MAGIC
# MAGIC It allows you to query data on your own terms, using:
# MAGIC
# MAGIC *   Serverless compute
# MAGIC *   Dedicated (provisioned) resources
# MAGIC
# MAGIC All at massive scale.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 2. Key Components Brought Together in One Unified Service
# MAGIC
# MAGIC Azure Synapse Analytics unifies multiple technologies under one platform:
# MAGIC
# MAGIC ### a. SQL for Data Warehousing
# MAGIC
# MAGIC *   Includes Synapse SQL
# MAGIC *   Supports data warehousing use cases
# MAGIC *   Enables T-SQL–based analytics
# MAGIC
# MAGIC ### b. Apache Spark for Big Data
# MAGIC
# MAGIC *   Fully integrated Apache Spark runtime
# MAGIC *   Used for large-scale data processing, machine learning, and batch workloads
# MAGIC
# MAGIC ### c. Pipelines for Data Integration (ETL/ELT)
# MAGIC
# MAGIC *   Built-in Synapse Pipelines, powered by Azure Data Factory
# MAGIC *   Enables data movement, transformation, and orchestration
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 3. Deep Integration with Azure Ecosystem
# MAGIC
# MAGIC Azure Synapse works seamlessly with:
# MAGIC
# MAGIC *   Power BI (for analytics and visualization)
# MAGIC *   Azure Cosmos DB (operational NoSQL data)
# MAGIC *   Azure Machine Learning (ML model training and scoring)
# MAGIC *   Other Azure services for end‑to‑end analytics

# COMMAND ----------

# MAGIC %md
# MAGIC # ⭐ Top Level Concepts of Azure Synapse Analytics
# MAGIC
# MAGIC Azure Synapse Analytics is a unified platform that combines **data warehousing**, **big‑data processing**, and **data integration** into one collaborative workspace.
# MAGIC
# MAGIC Below are the **core concepts you must know**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 1️⃣ Synapse Workspace
# MAGIC
# MAGIC **The Synapse Workspace is the central environment where all Synapse activities happen.**
# MAGIC
# MAGIC ### Key points
# MAGIC
# MAGIC *   It is a **collaboration environment** for cloud analytics where teams work together using SQL, Spark, and pipelines.
# MAGIC *   Each workspace is associated with an **Azure Data Lake Storage (ADLS) Gen2** account (used as primary storage).
# MAGIC *   It allows you to perform analytics using **SQL** and **Apache Spark** engines.
# MAGIC *   Compute resources inside the workspace are organized as **SQL Pools** and **Spark Pools**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 2️⃣ Linked Services
# MAGIC
# MAGIC **Linked Services** act like **connection strings** to external systems.
# MAGIC
# MAGIC ### Key points
# MAGIC
# MAGIC *   They store the connection information needed for Synapse to connect to:
# MAGIC     *   ADLS Gen2
# MAGIC     *   SQL Database, SQL Server
# MAGIC     *   Cosmos DB
# MAGIC     *   Snowflake, Amazon S3, SaaS systems, etc.
# MAGIC *   Pipelines and activities use linked services to read/write data.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 3️⃣ Synapse SQL
# MAGIC
# MAGIC This is the **SQL-based analytics engine** inside Synapse.
# MAGIC
# MAGIC ### Important components
# MAGIC
# MAGIC *   Supports T‑SQL for analytics, transformations, and reporting.
# MAGIC
# MAGIC *   Offers **two compute models**:
# MAGIC
# MAGIC     #### ✔ Dedicated SQL Pool (Provisioned)
# MAGIC
# MAGIC     *   MPP architecture for data warehousing
# MAGIC     *   Predictable performance and reserved capacity
# MAGIC
# MAGIC     #### ✔ Serverless SQL Pool (On‑Demand)
# MAGIC
# MAGIC     *   No provisioning, pay‑per‑query
# MAGIC     *   Query files directly in ADLS (Parquet, CSV, JSON)
# MAGIC
# MAGIC *   SQL Pools let you run SQL scripts, build warehouses, create views, external tables, etc.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 4️⃣ Apache Spark in Synapse
# MAGIC
# MAGIC Synapse includes a fully managed **Apache Spark runtime**.
# MAGIC
# MAGIC ### Key points
# MAGIC
# MAGIC *   Enables **big‑data processing**, machine learning, and data engineering.
# MAGIC *   You can create **Spark Pools** (cluster-like compute environments).
# MAGIC *   Spark sessions are automatically started when you run notebooks or jobs.
# MAGIC *   Two ways to use Spark:
# MAGIC     *   **Spark Notebooks** (Scala, PySpark, Spark SQL, C#)
# MAGIC     *   **Spark Job Definitions** (submit JAR‑based batch jobs)
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 5️⃣ Synapse Pipelines (Data Integration)
# MAGIC
# MAGIC Pipelines are the **Azure Data Factory (ADF)** capabilities built inside Synapse.
# MAGIC
# MAGIC ### Key concepts
# MAGIC
# MAGIC *   A **Pipeline** is a logical group of activities that perform a data workflow.
# MAGIC *   **Activities** define what to do:
# MAGIC     *   Copy data
# MAGIC     *   Run a Notebook
# MAGIC     *   Execute SQL scripts
# MAGIC     *   Web activity, validation, transformations
# MAGIC *   **Data Flows**
# MAGIC     *   Visual/no-code transformations
# MAGIC     *   Uses Spark under the hood
# MAGIC *   **Triggers**
# MAGIC     *   Run pipelines manually or on a schedule
# MAGIC     *   Event‑based, tumbling window, etc.
# MAGIC *   **Integration Dataset**
# MAGIC     *   Describes the structure of data used as input/output in pipeline activities
# MAGIC     *   Belongs to a Linked Service
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🎯 Final Summary
# MAGIC
# MAGIC  Concept              | Purpose                                                   |
# MAGIC  -------------------- | --------------------------------------------------------- |
# MAGIC  **Workspace**        | Central environment for analytics (SQL, Spark, Pipelines) |
# MAGIC  **Linked Services**  | Connection info to external data sources                  |
# MAGIC  **Synapse SQL**      | SQL analytics using Serverless or Dedicated pools         |
# MAGIC  **Spark in Synapse** | Big-data processing using Spark notebooks & jobs          |
# MAGIC  **Pipelines**        | Data orchestration (ADF inside Synapse)                   |

# COMMAND ----------

# MAGIC %md
# MAGIC # ⭐ Serverless SQL Pool — Top‑Level Concept Notes
# MAGIC
# MAGIC ## ✅ 1. What is Serverless SQL Pool?
# MAGIC
# MAGIC Serverless SQL pool is the **on‑demand SQL query engine** in Azure Synapse Analytics.  
# MAGIC It lets you run **T‑SQL queries directly over data stored in your Data Lake (ADLS Gen2)** *without* provisioning or managing any compute clusters.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ 2. Key Characteristics
# MAGIC
# MAGIC ### ✔ No capacity reservation
# MAGIC
# MAGIC You **do not create or manage a SQL cluster**.  
# MAGIC Compute is allocated only when you run a query, and then released automatically.
# MAGIC
# MAGIC ### ✔ Pay‑per‑query model
# MAGIC
# MAGIC You are billed **only for the amount of data scanned** by your query.  
# MAGIC No charges when you are not running analytics.
# MAGIC
# MAGIC ### ✔ Always available in every workspace
# MAGIC
# MAGIC Each Synapse workspace comes with a **built‑in serverless SQL endpoint** that is ready to use immediately.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ 3. Accessing Data with OPENROWSET
# MAGIC
# MAGIC Serverless SQL can read files from:
# MAGIC
# MAGIC *   ADLS Gen2
# MAGIC *   Azure Blob Storage
# MAGIC *   Cosmos DB (via Synapse link)
# MAGIC *   External data sources
# MAGIC
# MAGIC The **OPENROWSET()** function lets you query files like Parquet, CSV, JSON directly as if they were tables.
# MAGIC ***
# MAGIC
# MAGIC ## ✅ 4. When to Use Serverless SQL Pool
# MAGIC
# MAGIC Use it when you want:
# MAGIC
# MAGIC *   Ad‑hoc exploration of raw data
# MAGIC *   Quick SQL‑based profiling of files in the data lake
# MAGIC *   Lightweight dashboards on data‑lake files
# MAGIC *   Low‑cost analytics without managing warehouses
# MAGIC
# MAGIC It is ideal for:
# MAGIC
# MAGIC *   Data analysts querying raw CSV/Parquet files
# MAGIC *   Data engineers validating ingested data
# MAGIC *   BI teams building quick insights before modeling data in a warehouse
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ 5. Visualization Support in Synapse Studio
# MAGIC
# MAGIC Serverless SQL results can be visualized directly in Synapse Studio:
# MAGIC
# MAGIC *   Table view → Chart view
# MAGIC *   Supported chart types include bar, column, line, area, pie, and scatter
# MAGIC
# MAGIC This makes it easy to generate simple visual insights without exporting to Power BI.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT TOP 100 *
# MAGIC FROM
# MAGIC     OPENROWSET(
# MAGIC         BULK 'https://azuresynapsemo.dfs.core.windows.net/curated/employees.csv',
# MAGIC         FORMAT = 'CSV',
# MAGIC         HEADER_ROW =  TRUE,
# MAGIC         PARSER_VERSION = '2.0'
# MAGIC     ) AS [result]

# COMMAND ----------

# MAGIC %md
# MAGIC # Dedicated SQL Pool — Notes
# MAGIC
# MAGIC ## ✅ What is a Dedicated SQL Pool?
# MAGIC
# MAGIC A **Dedicated SQL Pool** in Azure Synapse Analytics is a **provisioned MPP (Massively Parallel Processing) data warehouse**.  
# MAGIC It provides **high‑performance, scalable SQL analytics** using reserved compute resources.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ How Dedicated SQL Pool Works
# MAGIC
# MAGIC *   It uses **provisioned compute** (measured in DWUs).
# MAGIC *   Compute and storage are **separated**, allowing you to scale compute independently.
# MAGIC *   Data is distributed across multiple compute nodes for parallel processing.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ Billing & Cost Behavior
# MAGIC
# MAGIC *   **Billing starts as soon as the pool is active**.  
# MAGIC     You are charged for:
# MAGIC     *   The compute resources (DWUs)
# MAGIC     *   The duration the pool remains *running*
# MAGIC *   **Pausing** the pool stops compute charges.  
# MAGIC     Storage charges continue, but compute cost drops to zero.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ When Should You Use It?
# MAGIC
# MAGIC *   Large‑scale enterprise data warehousing
# MAGIC *   Predictable, repeatable analytics workloads
# MAGIC *   High‑performance reporting pipelines
# MAGIC *   Scenarios requiring consistent, optimized SQL execution speeds
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ Association with Dedicated SQL Database
# MAGIC
# MAGIC *   Every Dedicated SQL Pool is backed by a **dedicated SQL database** inside Synapse.
# MAGIC *   This database contains:
# MAGIC     *   Tables
# MAGIC     *   Views
# MAGIC     *   Schemas
# MAGIC     *   Metadata required for warehouse operations
# MAGIC *   You connect to it using the SQL endpoint (just like working with SQL Server).
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ Key Takeaways
# MAGIC
# MAGIC *   Dedicated SQL Pool = **Provisioned, high‑performance data warehouse**.
# MAGIC *   It **consumes billable compute** whenever it is **running**.
# MAGIC *   You can **pause/resume** at any time to manage costs.
# MAGIC *   It is always paired with a **dedicated SQL database** within your Synapse workspace.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 📘 Notes: Serverless Spark Pool in Azure Synapse Analytics
# MAGIC
# MAGIC ## ⭐ What is a Serverless Spark Pool?
# MAGIC
# MAGIC A **serverless Spark pool** in Azure Synapse Analytics allows users to run Apache Spark code **without managing any cluster infrastructure**.
# MAGIC
# MAGIC *   When you start working with Spark (e.g., running a notebook), **a Spark session is automatically created** in the selected pool.
# MAGIC *   You do not need to create, configure, or scale clusters manually.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ How a Serverless Spark Pool Works
# MAGIC
# MAGIC *   The **pool determines the amount of Spark compute resources** used for each session.
# MAGIC *   It also controls **how long the session can stay idle** before the system automatically pauses the resources.
# MAGIC *   Since it is “serverless,” all resource handling (start, scale, pause) is automated.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ Billing Model
# MAGIC
# MAGIC *   You **only pay for the Spark resources consumed during the session**.
# MAGIC *   There is **no cost for just having the pool itself**.
# MAGIC *   Billing stops when the session automatically pauses.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ Comparison to Serverless SQL Pool
# MAGIC
# MAGIC *   A Serverless Spark Pool functions **similar to a Serverless SQL Pool** in Synapse.
# MAGIC *   In both cases:
# MAGIC     *   You do **not** manage servers or clusters.
# MAGIC     *   You pay only for the compute used.
# MAGIC     *   The platform handles provisioning and scaling.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ Key Benefits
# MAGIC
# MAGIC *   **Zero cluster management**: No need to start or stop clusters manually.
# MAGIC *   **Automatic scaling**: Resources are adjusted per session needs.
# MAGIC *   **Cost-efficient**: Pay only for execution time.
# MAGIC *   **Fast startup**: Sessions start quickly without waiting for cluster provisioning.

# COMMAND ----------

# MAGIC %md
# MAGIC # 📘 Notes: Adding an Administrator to an Azure Synapse Workspace
# MAGIC
# MAGIC When configuring administrative access for an Azure Synapse workspace, you need to assign roles across multiple layers: **Azure RBAC**, **Synapse RBAC**, **Storage Account RBAC**, and **Dedicated SQL Pool roles**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 1. Azure RBAC: Owner Role for the Workspace
# MAGIC
# MAGIC *   The user must have the **Owner** role assigned at the **workspace level**.
# MAGIC *   This grants full access to manage the workspace and assign roles to others.
# MAGIC *   Required for managing resources tied to the Synapse workspace.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 2. Synapse RBAC: Synapse Administrator Role
# MAGIC
# MAGIC *   Inside Synapse Studio, Synapse-specific permissions are controlled through **Synapse RBAC**.
# MAGIC *   The **Synapse Administrator** role provides:
# MAGIC     *   Full control over Synapse artifacts (pipelines, notebooks, SQL scripts, Spark pools, triggers, etc.)
# MAGIC     *   The ability to manage linked services and security policies within Synapse.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 3. Azure RBAC: Storage Account Role Assignments
# MAGIC
# MAGIC *   The Synapse workspace uses a **primary storage account** (the default linked Data Lake Storage Gen2).
# MAGIC *   Administrator must be assigned required roles on this storage account, such as:
# MAGIC     *   **Storage Blob Data Contributor** (for read/write)
# MAGIC     *   **Storage Blob Data Owner** (optional but more privileged)
# MAGIC *   These permissions are needed because Synapse stores pipelines, notebooks, logs, and data in this storage account.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 4. Dedicated SQL Pool: db\_owner Role
# MAGIC
# MAGIC *   For dedicated SQL pools (formerly SQL DW), the admin must be given **db\_owner** role.
# MAGIC *   This role provides full control inside the SQL database:
# MAGIC     *   Create tables, views, schemas
# MAGIC     *   Manage permissions
# MAGIC     *   Load data into the warehouse
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # ⭐ Summary Table
# MAGIC
# MAGIC  Layer                | Role Needed                     | Purpose                                           |
# MAGIC  -------------------- | ------------------------------- | ------------------------------------------------- |
# MAGIC  Azure RBAC           | **Owner**                       | Full resource management for Synapse workspace    |
# MAGIC  Synapse RBAC         | **Synapse Administrator**       | Full access inside Synapse Studio                 |
# MAGIC  Azure RBAC (Storage) | **Blob Data Contributor/Owner** | Access to workspace’s primary storage (ADLS Gen2) |
# MAGIC  Dedicated SQL Pool   | **db\_owner**                   | Full control inside SQL pool database             |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Azure Synapse SQL Architecture
# MAGIC Azure Synapse SQL is built on a **distributed, scale‑out architecture** where **compute and storage are separated**. This allows the system to scale for performance and cost efficiency.
# MAGIC
# MAGIC ![image_1773421576349.png](./image_1773421576349.png "image_1773421576349.png")
# MAGIC
# MAGIC
# MAGIC # 🧠 **1. Core Components of Synapse SQL Architecture**
# MAGIC
# MAGIC ### **✔ Control Node (Brain of the system)**
# MAGIC
# MAGIC *   Acts as the **entry point** for all SQL queries.
# MAGIC *   Runs the **Distributed Query Engine**.
# MAGIC *   Breaks queries into **smaller parallel tasks**.
# MAGIC *   Coordinates and optimizes execution.
# MAGIC
# MAGIC Dedicated SQL pool → Control node distributes queries to distributions.  
# MAGIC Serverless SQL pool → Control node uses DQP to split queries into tasks and assign files to nodes.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # ⚙️ **2. Compute Nodes (Workers that run your data operations)**
# MAGIC
# MAGIC ### **Dedicated SQL pool**
# MAGIC
# MAGIC *   Compute nodes process query tasks in parallel.
# MAGIC *   They store distributed data in Azure Storage.
# MAGIC *   Number of compute nodes varies from **1 to 60** depending on DWU level.
# MAGIC *   Distributions (60 total) are mapped across compute nodes.
# MAGIC
# MAGIC ### **Serverless SQL pool**
# MAGIC
# MAGIC *   Automatically scales compute nodes based on query needs.
# MAGIC *   Each compute node receives tasks and assigned files.
# MAGIC *   The system adapts automatically during topology changes.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🔄 **3. Data Movement Service (DMS)**
# MAGIC
# MAGIC *   Internal system-level service used **only in dedicated SQL pool**.
# MAGIC *   Moves data between compute nodes when queries require joins or aggregations across distributions.
# MAGIC *   Ensures correct results even when data must be reshuffled.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🧱 **4. Distributions (Smallest unit of data & parallelism)**
# MAGIC
# MAGIC *   There are **always 60 distributions** in a dedicated SQL pool.
# MAGIC *   Every query is broken into **60 parallel tasks**, one per distribution.
# MAGIC *   Compute nodes manage one or more distributions depending on DWU size.
# MAGIC *   At maximum compute (DW6000+), each node hosts one distribution.
# MAGIC *   At minimum compute, one node hosts all distributions.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🗂️ **5. Storage Layer — Azure Storage**
# MAGIC
# MAGIC *   All user data resides in Azure Storage (safe, durable, separate billing).
# MAGIC *   Dedicated SQL pool ingests data from ADLS and distributes it across 60 distributions.
# MAGIC *   Serverless SQL pool directly queries data in the data lake without ingestion.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🧩 **6. Table Distribution Methods (Sharding Patterns)**
# MAGIC
# MAGIC ### **A. Hash Distribution**
# MAGIC
# MAGIC *   Best for **large fact tables** used in joins and aggregations.
# MAGIC *   Uses a deterministic hash function on a chosen column to assign rows to distributions.
# MAGIC *   Ensures repeatable and balanced partitioning.
# MAGIC
# MAGIC ### **B. Round-Robin Distribution**
# MAGIC
# MAGIC *   Simple, fast loading.
# MAGIC *   Rows are spread randomly and sequentially across all 60 distributions.
# MAGIC *   Best for staging tables.
# MAGIC *   Joins require shuffling data → slower queries.
# MAGIC
# MAGIC ### **C. Replicated Tables**
# MAGIC
# MAGIC *   Entire table is **copied to every compute node**.
# MAGIC *   Best for **small dimension tables** frequently used in joins.
# MAGIC *   Eliminates the need for data movement before joins.
# MAGIC *   Not suitable for large tables due to storage overhead.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🚀 **7. Scaling & Elasticity**
# MAGIC
# MAGIC ### **Dedicated SQL pool**
# MAGIC
# MAGIC *   Scale compute **up/down** without moving data.
# MAGIC *   **Pause/resume** compute to save cost.
# MAGIC *   Distributions get remapped to available compute nodes after scaling.
# MAGIC
# MAGIC ### **Serverless SQL pool**
# MAGIC
# MAGIC *   Automatically scales compute for each query.
# MAGIC *   Automatically handles node addition/removal/failover.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🧾 **Overall Summary**
# MAGIC
# MAGIC Azure Synapse SQL delivers high performance through:
# MAGIC
# MAGIC *   **Scale-out compute with 60 logical distributions**
# MAGIC *   **Separation of compute and storage**
# MAGIC *   **Parallel execution of every query**
# MAGIC *   **A control node that orchestrates distributed execution**
# MAGIC *   **Compute nodes that run work in parallel**
# MAGIC *   **DMS for data movement when needed**
# MAGIC *   **Flexible table distribution methods** (hash, round-robin, replicated)
# MAGIC *   **Serverless and dedicated options** for different workload needs
# MAGIC
# MAGIC It combines MPP (massively parallel processing) architecture with Azure Storage to deliver scalable, powerful SQL analytics.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 📘 **Azure Synapse – Serverless SQL Pool**
# MAGIC
# MAGIC ## ⭐ 1. What is Serverless SQL Pool?
# MAGIC
# MAGIC *   Every Azure Synapse workspace automatically includes a **serverless SQL endpoint**.
# MAGIC *   This endpoint allows you to **query data directly** from:
# MAGIC     *   Azure Data Lake (Parquet, Delta Lake, CSV, JSON, delimited text)
# MAGIC     *   Cosmos DB
# MAGIC     *   Dataverse
# MAGIC *   No need to ingest or load data into a specialized data store.
# MAGIC *   You can use **standard T‑SQL syntax** to query files.
# MAGIC *   Fully **pay‑as‑you‑go**:
# MAGIC     *   You pay only for **query execution**, not for provisioning computing resources.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ 2. Key Features of Serverless SQL Pool
# MAGIC
# MAGIC *   **Zero infrastructure management**  
# MAGIC     No clusters or nodes to set up or maintain.
# MAGIC *   **On-demand compute**  
# MAGIC     Automatically scales based on query requirements.
# MAGIC *   **Ideal for exploratory analytics**  
# MAGIC     Query files directly without ETL.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **T‑SQL Support in Serverless SQL Pool**
# MAGIC
# MAGIC ## ⭐ 3. Supported Concepts
# MAGIC
# MAGIC Serverless SQL pool exposes a **T‑SQL querying surface area**, also known as LDW (Logical Data Warehouse).
# MAGIC
# MAGIC ### ✔ Objects supported:
# MAGIC
# MAGIC *   **Databases**
# MAGIC     *   A serverless SQL endpoint can contain **multiple databases**.
# MAGIC *   **Schemas**
# MAGIC     *   Each database can contain multiple schemas.
# MAGIC *   **Metadata objects** (stored inside the database)
# MAGIC     *   Views
# MAGIC     *   Stored procedures
# MAGIC     *   Inline table-valued functions
# MAGIC     *   External resources:
# MAGIC         *   Data sources
# MAGIC         *   File formats
# MAGIC         *   External tables
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ 4. No Local Storage
# MAGIC
# MAGIC Serverless SQL pool **does not maintain any local storage**.  
# MAGIC Only **metadata** is stored in the database.
# MAGIC
# MAGIC ### ❌ Therefore, the following T‑SQL features are NOT supported:
# MAGIC
# MAGIC *   Regular relational **tables**
# MAGIC *   **Triggers**
# MAGIC *   **Materialized views**
# MAGIC *   **DML statements** (INSERT, UPDATE, DELETE, MERGE)
# MAGIC *   **DDL** statements (except those related to security, metadata, and views)
# MAGIC
# MAGIC In other words:
# MAGIC
# MAGIC *   You **cannot** physically store data inside serverless SQL pool.
# MAGIC *   You **only query external data** + maintain metadata.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **Serverless SQL Pool – Summary**
# MAGIC
# MAGIC ### ✔ What it **IS**
# MAGIC
# MAGIC *   A distributed SQL query engine that reads data **directly** from data lakes and external sources.
# MAGIC *   A cost‑effective option for data exploration, ad‑hoc queries, and dashboards.
# MAGIC
# MAGIC ### ✔ What it is **NOT**
# MAGIC
# MAGIC *   It is not a relational database engine.
# MAGIC *   It is not meant for ETL heavy transformations.
# MAGIC *   It does not store tables or maintain transactional data.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # 📘 **1. External Data Source**
# MAGIC
# MAGIC ## ✅ **Definition**
# MAGIC
# MAGIC An **External Data Source** is a database object used to define connectivity to external storage systems such as:
# MAGIC
# MAGIC *   Azure Blob Storage
# MAGIC *   Azure Data Lake Storage (ADLS Gen2)
# MAGIC *   Other external data systems (via PolyBase)
# MAGIC
# MAGIC It is mainly used for:
# MAGIC
# MAGIC *   **Data virtualization** (querying data without ingestion)
# MAGIC *   **Data loading using PolyBase**
# MAGIC *   **Serverless SQL Pool external tables**
# MAGIC *   **Dedicated SQL Pool external tables**
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ **Why External Data Source is Needed**
# MAGIC
# MAGIC *   SQL engine must know **where the external files are stored**
# MAGIC *   It allows Synapse to access file paths securely
# MAGIC *   It binds storage location + credentials together
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ✅ **Syntax Example**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE EXTERNAL DATA SOURCE SqlOnDemandDemo
# MAGIC WITH (
# MAGIC     LOCATION = 'https://sqlondemandstorage.blob.core.windows.net',
# MAGIC     CREDENTIAL = sqlondemand
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC ### Explanation:
# MAGIC
# MAGIC *   **LOCATION** → Base path of storage account
# MAGIC *   **CREDENTIAL** → Auth object that contains SAS token or Managed Identity
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **2. Credentials (Database Scoped Credential)**
# MAGIC
# MAGIC ## ✅ **Definition**
# MAGIC
# MAGIC A **Database Scoped Credential** stores authentication information required to access external resources.  
# MAGIC Examples of authentication:
# MAGIC
# MAGIC *   SAS Token
# MAGIC *   Storage Account Key
# MAGIC *   Managed Identity (for Synapse)
# MAGIC *   OAuth tokens (in some cases)
# MAGIC
# MAGIC It is required when creating:
# MAGIC
# MAGIC *   External Data Source
# MAGIC *   External Tables
# MAGIC *   OPENROWSET with external authentication
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🔐 **Credential Requirements**
# MAGIC
# MAGIC Before creating a credential, the database must have a **Master Key**.
# MAGIC
# MAGIC ### Create Master Key
# MAGIC
# MAGIC ```sql
# MAGIC CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Welcome1$Hello@';
# MAGIC ```
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🔐 **Create Credential Example**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE DATABASE SCOPED CREDENTIAL demoCredential
# MAGIC WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
# MAGIC SECRET = 'sv=2020-08-04&ss=bq...<SAS Token>...';
# MAGIC ```
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🔐 **Using Credential Inside an External Data Source**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE EXTERNAL DATA SOURCE demoDataSource
# MAGIC WITH (
# MAGIC     LOCATION = 'https://maheeraldslgen2.dfs.core.windows.net',
# MAGIC     CREDENTIAL = demoCredential
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **3. External File Format**
# MAGIC
# MAGIC ## ✅ **Definition**
# MAGIC
# MAGIC An **External File Format** defines the **structure and layout** of the external data stored in:
# MAGIC
# MAGIC *   Azure Blob Storage
# MAGIC *   Azure Data Lake Storage (ADLS)
# MAGIC
# MAGIC It describes:
# MAGIC
# MAGIC *   File type
# MAGIC *   Encoding
# MAGIC *   Field delimiters
# MAGIC *   Compression
# MAGIC *   Parser version
# MAGIC *   Parquet/DelimitedText options
# MAGIC
# MAGIC 👉 It is a **prerequisite for creating External Tables** (Dedicated SQL Pool).
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## ⭐ **Why File Format is required?**
# MAGIC
# MAGIC Because Synapse must understand **how the file is structured**:
# MAGIC
# MAGIC *   Is it Parquet?
# MAGIC *   Is it CSV?
# MAGIC *   What delimiter?
# MAGIC *   What encoding?
# MAGIC *   What compression?
# MAGIC
# MAGIC Serverless SQL pool **does NOT require external file format**, but **Dedicated SQL pool does**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **4. Supported File Formats in Synapse External Tables**
# MAGIC
# MAGIC Azure Synapse supports **two file types** for external tables:
# MAGIC
# MAGIC ### ✔ **1. Parquet**
# MAGIC
# MAGIC *   Columnar format
# MAGIC *   Highly compressed, efficient
# MAGIC *   Best for analytical workloads
# MAGIC
# MAGIC ### ✔ **2. Delimited Text**
# MAGIC
# MAGIC *   CSV, TSV, pipe-separated files
# MAGIC *   Row-based format
# MAGIC *   Flexible for ingestion and staging scenarios
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **5. External File Format – Syntax Examples**
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟣 **A. Parquet File Format**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE EXTERNAL FILE FORMAT ParquetFormat
# MAGIC WITH (
# MAGIC     FORMAT_TYPE = PARQUET,
# MAGIC     DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC Optional compression:
# MAGIC
# MAGIC *   Snappy (default)
# MAGIC *   GZip
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟣 **B. Delimited Text (CSV) File Format**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE EXTERNAL FILE FORMAT CsvFormat
# MAGIC WITH (
# MAGIC     FORMAT_TYPE = DELIMITEDTEXT,
# MAGIC     DATA_COMPRESSION = 'org.apache.hadoop.io.compress.GzipCodec',
# MAGIC     FORMAT_OPTIONS (
# MAGIC         FIELD_TERMINATOR = ',',
# MAGIC         STRING_DELIMITER = '"',
# MAGIC         FIRST_ROW = 2,
# MAGIC         USE_TYPE_DEFAULT = TRUE,
# MAGIC         ENCODING = 'UTF8'
# MAGIC     )
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC ### Common Format Options:
# MAGIC
# MAGIC | Option             | Description                              |           |
# MAGIC | ------------------ | ---------------------------------------- | --------- |
# MAGIC | `FIELD_TERMINATOR` | Character that separates values (`,`, \` | `, `\t\`) |
# MAGIC | `STRING_DELIMITER` | Quotes around text (`"`)                 |           |
# MAGIC | `FIRST_ROW`        | Skip header row                          |           |
# MAGIC | `USE_TYPE_DEFAULT` | Use SQL default data types               |           |
# MAGIC | `ENCODING`         | UTF8, UTF16                              |           |
# MAGIC | `PARSER_VERSION`   | Version of parser                        |           |
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 📘 **6. How These Objects Work Together**
# MAGIC
# MAGIC ### External Table Creation Requires:
# MAGIC
# MAGIC 1.  **Credential** → to authenticate storage
# MAGIC 2.  **External Data Source** → points to storage location
# MAGIC 3.  **External File Format** → defines file structure
# MAGIC 4.  **External Table** → maps schema to external files
# MAGIC
# MAGIC Workflow:
# MAGIC
# MAGIC     Credential → External Data Source → External File Format → External Table
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🎯 **Final Summary (Perfect for Revision)**
# MAGIC
# MAGIC ### **External Data Source**
# MAGIC
# MAGIC *   Defines **WHERE** the data is located
# MAGIC *   Requires a credential
# MAGIC *   Used for PolyBase, Dedicated SQL Pool external tables
# MAGIC
# MAGIC ### **Credential**
# MAGIC
# MAGIC *   Stores **HOW** to authenticate
# MAGIC *   Needs a Master Key
# MAGIC *   Used for secure access to ADLS / Blob
# MAGIC
# MAGIC ### **External File Format**
# MAGIC
# MAGIC *   Defines **HOW the external file is structured**
# MAGIC *   Required for Dedicated SQL Pool external tables
# MAGIC *   Supports **Parquet** & **DelimitedText**

# COMMAND ----------

# MAGIC %md
# MAGIC TYPE = HADOOP means "this external data source follows the Hadoop filesystem interface (HDFS-compatible APIs)"
# MAGIC Azure Data Lake Storage (ADLS Gen2) implements the Hadoop-compatible filesystem API, so Synapse uses TYPE = HADOOP for:
# MAGIC - Azure Data Lake Storage Gen2 (abfss://)
# MAGIC - Azure Blob Storage (wasbs://)
# MAGIC - Any HDFS-compatible storage endpoint

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA [Ext]
# MAGIC     AUTHORIZATION [dbo];
# MAGIC     
# MAGIC CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Welcome1$Hello@';
# MAGIC
# MAGIC CREATE DATABASE SCOPED CREDENTIAL [msi_cred]
# MAGIC     WITH IDENTITY = N'Managed Service Identity';
# MAGIC
# MAGIC CREATE EXTERNAL DATA SOURCE [Staging_ADLS]
# MAGIC     WITH (
# MAGIC     TYPE = HADOOP,
# MAGIC     LOCATION = N'abfss://azuresynapsemo.dfs.core.windows.net',
# MAGIC     CREDENTIAL = [msi_cred]
# MAGIC     );
# MAGIC
# MAGIC CREATE EXTERNAL FILE FORMAT [PARQUETFF]
# MAGIC     WITH (
# MAGIC     FORMAT_TYPE = PARQUET,
# MAGIC     DATA_COMPRESSION = N'org.apache.hadoop.io.compress.SnappyCodec'
# MAGIC     );
# MAGIC
# MAGIC CREATE EXTERNAL TABLE [Ext].[COMA_SA_SALES_GROUP_BOB_Ext] (
# MAGIC     [SUB_SALES_GROUP_ID] INT NULL,
# MAGIC     [NAOS_NODE] VARCHAR (30) NULL,
# MAGIC     [PRIMARY_FLG] VARCHAR (1) NULL,
# MAGIC     [VISIBILITY_FLG] VARCHAR (1) NULL,
# MAGIC     [LAST_MAINT_USER] VARCHAR (30) NULL,
# MAGIC     [LAST_MAINT_DATE] VARCHAR (35) NULL
# MAGIC )
# MAGIC     WITH (
# MAGIC     DATA_SOURCE = [Staging_ADLS],
# MAGIC     LOCATION = N'/CostSavings/COMA_SA_SALES_GROUP_BOB/',
# MAGIC     FILE_FORMAT = [PARQUETFF],
# MAGIC     REJECT_TYPE = VALUE,
# MAGIC     REJECT_VALUE = 0
# MAGIC     );

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 📘 **Notes on CETAS & CTAS (Azure Synapse Analytics)**
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 **1. CETAS – Create External Table As SELECT**
# MAGIC
# MAGIC ### **What is CETAS?**
# MAGIC
# MAGIC CETAS allows you to:
# MAGIC
# MAGIC *   **Create an external table** in a dedicated SQL pool or serverless SQL pool.
# MAGIC *   **Export data in parallel** from a SQL SELECT statement to external storage such as:
# MAGIC     *   Hadoop
# MAGIC     *   Azure Storage Blob
# MAGIC     *   Azure Data Lake Storage Gen2 (ADLS Gen2)
# MAGIC
# MAGIC ### **Why use CETAS?**
# MAGIC
# MAGIC *   Extremely fast because of *parallel export*.
# MAGIC *   Useful for:
# MAGIC     *   Data archival
# MAGIC     *   Data offloading
# MAGIC     *   Creating curated datasets in external storage
# MAGIC     *   Sharing data with other systems (Spark, ADF, Databricks, etc.)
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 **2. CETAS Syntax**
# MAGIC
# MAGIC     CREATE EXTERNAL TABLE [database_name].[schema_name].[table_name]
# MAGIC     WITH (
# MAGIC         LOCATION = 'path_to_folder',
# MAGIC         DATA_SOURCE = external_data_source_name,
# MAGIC         FILE_FORMAT = external_file_format_name
# MAGIC     )
# MAGIC     AS
# MAGIC     SELECT <select_criteria>
# MAGIC
# MAGIC ### **Important Notes**
# MAGIC
# MAGIC *   `LOCATION` → folder path in ADLS / Blob
# MAGIC *   `DATA_SOURCE` → points to ADLS Gen2 (linked storage)
# MAGIC *   `FILE_FORMAT` → Parquet, CSV, etc.
# MAGIC *   You *can* use CTEs inside the SELECT.
# MAGIC *   ❗ **ORDER BY is NOT allowed** in a CETAS SELECT.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 **3. CTAS – Create Table As SELECT**
# MAGIC
# MAGIC ### **What is CTAS?**
# MAGIC
# MAGIC *   CTAS creates a **new internal table** from the output of a SELECT query.
# MAGIC *   One of the fastest ways to:
# MAGIC     *   Create a table
# MAGIC     *   Insert data into a table in a single operation
# MAGIC
# MAGIC ### **Key Features**
# MAGIC
# MAGIC *   Parallel operation
# MAGIC *   Often used for:
# MAGIC     *   Data transformation
# MAGIC     *   Staging tables
# MAGIC     *   ELT pipelines
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 🟦 **4. SELECT INTO vs CTAS**
# MAGIC
# MAGIC ### **SELECT INTO Limitations**
# MAGIC
# MAGIC *   Cannot change:
# MAGIC     *   **Distribution method**
# MAGIC     *   **Index type**
# MAGIC *   Uses defaults:
# MAGIC     *   Distribution: **ROUND\_ROBIN**
# MAGIC     *   Index: **CLUSTERED COLUMNSTORE INDEX**
# MAGIC
# MAGIC ### **CTAS Advantages**
# MAGIC
# MAGIC You *can* define:
# MAGIC
# MAGIC *   Distribution (HASH, REPLICATE, ROUND\_ROBIN)
# MAGIC *   Table structure (index types)
# MAGIC
# MAGIC ### **Example of CTAS**
# MAGIC
# MAGIC     CREATE TABLE [dbo].[FactInternetSales_new]
# MAGIC     WITH
# MAGIC     (
# MAGIC         DISTRIBUTION = ROUND_ROBIN,
# MAGIC         CLUSTERED COLUMNSTORE INDEX
# MAGIC     )
# MAGIC     AS
# MAGIC     SELECT *
# MAGIC     FROM [dbo].[FactInternetSales];
# MAGIC
# MAGIC ### **SELECT INTO equivalent**
# MAGIC
# MAGIC     SELECT *
# MAGIC     INTO [dbo].[FactInternetSales_new]
# MAGIC     FROM [dbo].[FactInternetSales];
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC # 🟩 Final Summary
# MAGIC
# MAGIC | Feature             | CETAS                | CTAS               | SELECT INTO        |
# MAGIC | ------------------- | -------------------- | ------------------ | ------------------ |
# MAGIC | Creates table       | External table       | Internal table     | Internal table     |
# MAGIC | Storage             | ADLS / Blob / Hadoop | Dedicated SQL pool | Dedicated SQL pool |
# MAGIC | Parallelism         | Yes                  | Yes                | Yes                |
# MAGIC | Custom Distribution | ❌                    | ✔️                 | ❌                  |
# MAGIC | Custom Index        | ❌                    | ✔️                 | ❌                  |
# MAGIC | ORDER BY allowed    | ❌                    | ✔️                 | ✔️                 |
# MAGIC