# Databricks notebook source
# MAGIC %md
# MAGIC # Parquet

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Data Sources & Formats
# MAGIC
# MAGIC ### Unstructured
# MAGIC
# MAGIC *   Examples: **TXT**
# MAGIC *   Very flexible but less organized.
# MAGIC
# MAGIC ### Semi-Structured
# MAGIC
# MAGIC *   Examples: **XML, JSON**
# MAGIC *   Has some structure (tags, key–value).
# MAGIC
# MAGIC ### Structured
# MAGIC
# MAGIC *   Examples: **Avro, Parquet, ORC, MySQL**
# MAGIC *   Most organized and efficient for storage & performance.
# MAGIC *   Best for **Apache Spark** processing.
# MAGIC
# MAGIC <img src="./image_1774957376307.png" alt="image_1774957376307.png" width="600" height="450"/>
# MAGIC
# MAGIC <img src="./image_1774958592025.png" alt="image_1774958592025.png" width="600" height="450"/>

# COMMAND ----------

# MAGIC %md
# MAGIC # Delta Lake

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table of Contents
# MAGIC 1. **Datawarehouse vs Data Lake vs Delta Lake**
# MAGIC 2. **Why delta lake over data lake?**
# MAGIC 3. **ACID**
# MAGIC 4. **How ACID Works Internally in Delta Lake?**
# MAGIC 5. **The Update / Delete / Insert Problem in a Data Lake**
# MAGIC 6. **DML Operation on Delta table**
# MAGIC 7. **Compacted JSON and Checkpoint file**
# MAGIC 8. **Pessimistic and Optimistic Concurrency Control**
# MAGIC 9. **Time Travel and Versioning**
# MAGIC 10. **Schema Validation/Schema Enforcement**
# MAGIC 11. **mergeSchema VS overwriteSchema**
# MAGIC 12. **Schema Evolution**
# MAGIC 13. **Convert Parquet to Delta**
# MAGIC 14. **Managed and External Tables**
# MAGIC 15. **Deletion Vector**
# MAGIC 16. **Optimization**
# MAGIC 17. **Data Layout Optimization**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Data Warehouse vs Data Lake vs Delta Lake
# MAGIC
# MAGIC ### 1. Data Warehouse
# MAGIC
# MAGIC A **Data Warehouse** is a centralized system optimized for **structured data**, reporting, and BI analytics.
# MAGIC
# MAGIC **Key Characteristics**
# MAGIC
# MAGIC *   Stores **highly structured**, cleaned, and curated data.
# MAGIC *   Uses **schema-on-write** (data must match schema before loading).
# MAGIC *   Best for **business intelligence, dashboards, and SQL analytics**.
# MAGIC *   Examples:  
# MAGIC     **Azure Synapse Dedicated SQL Pool**, **Snowflake**, **Amazon Redshift**, **Google BigQuery**, **Teradata**.
# MAGIC
# MAGIC **Pros**
# MAGIC
# MAGIC *   Excellent performance for analytics.
# MAGIC *   Strong governance, data quality, and compliance.
# MAGIC *   Suitable for enterprise reporting (e.g., your Power BI Report Server workloads).
# MAGIC
# MAGIC **Cons**
# MAGIC
# MAGIC *   Expensive storage and compute.
# MAGIC *   Not good for raw/unstructured data.
# MAGIC *   Harder to scale for data science/AI workloads.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 2. Data Lake
# MAGIC
# MAGIC A **Data Lake** stores **raw data of any type** at low cost in object storage.
# MAGIC
# MAGIC **Key Characteristics**
# MAGIC
# MAGIC *   Supports **structured, semi-structured, and unstructured** data.
# MAGIC *   Uses **schema-on-read** (schema applied when querying).
# MAGIC *   Ideal for **big data processing**, **ML**, and **batch/stream ingestion**.
# MAGIC *   Examples:  
# MAGIC     **Azure Data Lake Storage (ADLS) Gen2**, **Amazon S3**, **Google Cloud Storage**.
# MAGIC
# MAGIC **Pros**
# MAGIC
# MAGIC *   Very low cost.
# MAGIC *   Highly scalable for large volumes of data.
# MAGIC *   Flexible storage for raw data from IoT, logs, clickstreams, etc.
# MAGIC
# MAGIC **Cons**
# MAGIC
# MAGIC *   Lacks governance and reliability (the “data swamp” problem).
# MAGIC *   Data consistency/quality issues.
# MAGIC *   No built-in ACID transactions.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 3. Delta Lake (Built on top of Data Lake)
# MAGIC
# MAGIC **Delta Lake** is an open-source **storage layer** that adds **reliability, performance, and ACID transactions** to a Data Lake.
# MAGIC
# MAGIC You typically use it on **ADLS Gen2 + Spark (Databricks)**.
# MAGIC
# MAGIC **Key Characteristics**
# MAGIC
# MAGIC *   Built on existing cloud storage (ADLS/S3).
# MAGIC *   Provides **ACID transactions**, schema enforcement, versioning.
# MAGIC *   Stores data in **Delta tables (.delta + Parquet)**.
# MAGIC *   Optimized for **batch + streaming**, ML, and Lakehouse architecture.
# MAGIC
# MAGIC **Pros**
# MAGIC
# MAGIC *   Solves the data lake problems (data quality + reliability).
# MAGIC *   Supports **time travel** & data versioning.
# MAGIC *   Huge performance improvements using ZORDER, OPTIMIZE, Auto-Compaction.
# MAGIC *   Enables a **Lakehouse** where data lake + warehouse capabilities converge.
# MAGIC
# MAGIC **Cons**
# MAGIC
# MAGIC *   Requires Spark/Databricks or compatible engines.
# MAGIC *   Slightly more complex than raw data lake.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Why delta lake over data lake?
# MAGIC - Data Governance issue
# MAGIC - Data Quality issue
# MAGIC - Lack of ACID support
# MAGIC - No support for Update, Delete and Insert

# COMMAND ----------

# MAGIC %md
# MAGIC ## ACID
# MAGIC
# MAGIC ACID is a set of **four guarantees** that ensure **reliability, correctness, and consistency** of data operations, especially when multiple readers/writers work simultaneously.
# MAGIC
# MAGIC ACID stands for:
# MAGIC
# MAGIC 1.  **A — Atomicity**
# MAGIC 2.  **C — Consistency**
# MAGIC 3.  **I — Isolation**
# MAGIC 4.  **D — Durability**
# MAGIC
# MAGIC These guarantees originated in traditional OLTP databases (MySQL, Oracle, SQL Server) but now apply to modern big‑data platforms like **Delta Lake**, which brings ACID to data lakes.
# MAGIC
# MAGIC ### 1. Atomicity — "All or Nothing"
# MAGIC
# MAGIC **Definition**
# MAGIC
# MAGIC A transaction must be treated as a **single, indivisible unit**.  
# MAGIC Either **every step succeeds**, or **the entire transaction is rolled back**.
# MAGIC
# MAGIC There is *no in-between state*.
# MAGIC
# MAGIC **Why Atomicity matters**
# MAGIC
# MAGIC Without it:
# MAGIC
# MAGIC *   Partial writes → corrupted data
# MAGIC *   Half-updated tables
# MAGIC *   Broken pipelines
# MAGIC *   Data mismatches between tables
# MAGIC
# MAGIC **Example (Simple)**
# MAGIC
# MAGIC Suppose you transfer ₹500 from Account A to Account B:
# MAGIC
# MAGIC 1.  Deduct from A
# MAGIC 2.  Add to B
# MAGIC
# MAGIC If step 1 succeeds but step 2 fails, money disappears in the middle.
# MAGIC
# MAGIC Atomicity prevents this by rolling back step 1.
# MAGIC
# MAGIC **Example in Delta Lake**
# MAGIC
# MAGIC If your Spark job writes data to a Delta table:
# MAGIC
# MAGIC ```sql
# MAGIC MERGE INTO sales USING updates ...
# MAGIC ```
# MAGIC
# MAGIC If Spark fails mid-way:
# MAGIC
# MAGIC *   Delta Lake **does NOT** leave half-written Parquet files.
# MAGIC *   It rolls back to the last valid snapshot.
# MAGIC
# MAGIC This avoids the **“partially written files”** problem of normal data lakes.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 2. Consistency — "Data Must Always Be Valid"
# MAGIC
# MAGIC **Definition**
# MAGIC
# MAGIC After a transaction completes, **the data must remain in a valid state**, following:
# MAGIC
# MAGIC *   Constraints
# MAGIC *   Rules
# MAGIC *   Data types
# MAGIC *   Checks
# MAGIC *   Business logic
# MAGIC
# MAGIC **Why Consistency matters**
# MAGIC
# MAGIC Without consistency:
# MAGIC
# MAGIC *   Bad data enters the system
# MAGIC *   Wrong schema
# MAGIC *   Violated constraints
# MAGIC *   Broken referential integrity
# MAGIC
# MAGIC **Example (Simple)**
# MAGIC
# MAGIC A rule says:
# MAGIC
# MAGIC > "Age must be > 0"
# MAGIC
# MAGIC If a transaction tries to insert age = -5, consistency rejects it.
# MAGIC
# MAGIC **Example in Delta Lake**
# MAGIC
# MAGIC Delta Lake enforces schema consistency:
# MAGIC
# MAGIC ```sql
# MAGIC ALTER TABLE events ADD COLUMN user_id STRING;
# MAGIC ```
# MAGIC
# MAGIC If a write attempts:
# MAGIC
# MAGIC ```json
# MAGIC { "user_id": 123 }  -- integer
# MAGIC ```
# MAGIC
# MAGIC Delta will **reject the write** (schema enforcement), unlike a raw Data Lake where corrupted data silently lands in Parquet files.
# MAGIC
# MAGIC This keeps the table clean and reliable.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 3. Isolation — "Transactions Don't Interfere"
# MAGIC
# MAGIC **Definition**
# MAGIC
# MAGIC Multiple transactions happening at the same time **must not affect each other**.
# MAGIC
# MAGIC It should appear as if they ran **sequentially**, even if they ran **in parallel**.
# MAGIC
# MAGIC This removes:
# MAGIC
# MAGIC *   Dirty reads
# MAGIC *   Dirty writes
# MAGIC *   Non-repeatable reads
# MAGIC *   Phantom reads
# MAGIC
# MAGIC **Why Isolation matters in Big Data**
# MAGIC
# MAGIC In a distributed system like Spark:
# MAGIC
# MAGIC *   Hundreds of writers may append/merge
# MAGIC *   Thousands of readers may query simultaneously
# MAGIC
# MAGIC Without isolation → chaos:
# MAGIC
# MAGIC *   Readers see incomplete writes
# MAGIC *   Writers overwrite each other's data
# MAGIC
# MAGIC **Isolation in Delta Lake**
# MAGIC
# MAGIC Delta Lake uses **optimistic concurrency control**.
# MAGIC
# MAGIC If two writers try to modify the same table version:
# MAGIC
# MAGIC *   First write succeeds
# MAGIC *   Second write fails with:  
# MAGIC     **“Concurrent modification exception”**  
# MAGIC     and must retry.
# MAGIC
# MAGIC This ensures **no corruption** and **no mixed snapshots**.
# MAGIC
# MAGIC Readers always get a **consistent snapshot**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ###  4. Durability — "It Stays Written Forever"
# MAGIC
# MAGIC **Definition**
# MAGIC
# MAGIC Once a transaction is committed, **the data will survive**:
# MAGIC
# MAGIC *   Server crash
# MAGIC *   Power failure
# MAGIC *   System restarts
# MAGIC *   Hardware failure
# MAGIC
# MAGIC **Why Durability matters**
# MAGIC
# MAGIC If durability didn't exist:
# MAGIC
# MAGIC *   Data could be lost after a crash
# MAGIC *   Tables could revert to old versions
# MAGIC
# MAGIC **Durability in Delta Lake**
# MAGIC
# MAGIC Delta Lake stores:
# MAGIC
# MAGIC *   Parquet files
# MAGIC *   Transaction logs (`_delta_log`)  
# MAGIC     which contain the **committed actions**
# MAGIC
# MAGIC Once committed:
# MAGIC
# MAGIC *   The transaction log writes are **atomic and permanent**
# MAGIC *   Even if your Spark cluster crashes, data is safe
# MAGIC
# MAGIC Azure Data Lake Storage (ADLS) ensures durability through:
# MAGIC
# MAGIC *   Triple replication
# MAGIC *   High availability
# MAGIC
# MAGIC So your Delta tables are highly durable.

# COMMAND ----------

# MAGIC %md
# MAGIC ## How ACID Works Internally in Delta Lake
# MAGIC
# MAGIC ### 1. ATOMICITY — Achieved using the **Atomic Commit Protocol**
# MAGIC
# MAGIC **How Atomicity works**
# MAGIC
# MAGIC Delta Lake represents each **transaction** (write/merge/update/delete) as a **single JSON commit file** inside the directory:
# MAGIC
# MAGIC     /delta_table/
# MAGIC         _delta_log/
# MAGIC             00000000000000000010.json
# MAGIC
# MAGIC Each commit file contains *all the actions* in that transaction:
# MAGIC
# MAGIC *   AddFile (new parquet files)
# MAGIC *   RemoveFile (old files invalidated)
# MAGIC *   Metadata updates
# MAGIC *   Protocol changes
# MAGIC *   Stats
# MAGIC
# MAGIC **Atomicity is achieved because:**
# MAGIC
# MAGIC A transaction is *only visible* if the final commit file is successfully written.
# MAGIC
# MAGIC **All-or-nothing” is guaranteed because:**
# MAGIC
# MAGIC If the final JSON log file is not created →  **the whole transaction is discarded**, not partially visible.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 2. CONSISTENCY — Enforced using Schema Enforcement + Constraints
# MAGIC
# MAGIC Delta Lake ensures that every committed transaction produces a **valid table state**.
# MAGIC
# MAGIC **Consistency is enforced by:**
# MAGIC
# MAGIC *   **Schema-on-write**
# MAGIC *   **Column data type checking**
# MAGIC *   **Nullability rules**
# MAGIC *   **Generated columns**
# MAGIC *   **CHECK constraints**
# MAGIC
# MAGIC For example:
# MAGIC
# MAGIC ```sql
# MAGIC ALTER TABLE customers ADD CONSTRAINT age_check CHECK (age > 0);
# MAGIC ```
# MAGIC
# MAGIC Any write that breaks the rule → **fails before commit**.
# MAGIC
# MAGIC **All validation happens before the commit JSON is written.**
# MAGIC
# MAGIC If validation fails →  
# MAGIC 1. No commit file is created →  
# MAGIC 2. Invalid data never lands in the table.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 3. ISOLATION — Achieved through Optimistic Concurrency + Snapshot Isolation
# MAGIC
# MAGIC Delta Lake uses **optimistic concurrency control** instead of locks.
# MAGIC
# MAGIC **Readers get Snapshot Isolation**
# MAGIC
# MAGIC When a reader queries a Delta table:
# MAGIC
# MAGIC *   It reads the *latest valid snapshot*
# MAGIC *   Snapshot = last successful commit JSON
# MAGIC *   Readers never see half-written data
# MAGIC *   Readers do NOT block writers (and vice-versa)
# MAGIC
# MAGIC **Writers use Optimistic Concurrency**
# MAGIC
# MAGIC Each writer:
# MAGIC
# MAGIC 1.  Reads latest table version (e.g., version 10)
# MAGIC 2.  Performs changes
# MAGIC 3.  Attempts to commit version 11
# MAGIC
# MAGIC If another writer has already committed version 11:
# MAGIC
# MAGIC *   Your commit fails: **ConcurrentModificationException**
# MAGIC *   Spark retries automatically
# MAGIC
# MAGIC **Why “optimistic”?**
# MAGIC
# MAGIC Writers assume conflicts are rare and only check at commit time.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 4. DURABILITY — Provided by **Transaction Logs + Cloud Replication**
# MAGIC
# MAGIC Durability means that once a transaction is committed:
# MAGIC
# MAGIC *   It is **permanent**
# MAGIC *   It survives cluster shutdown
# MAGIC *   It survives node failures
# MAGIC *   It survives Spark job crashes
# MAGIC
# MAGIC **Delta ensures durability via:**
# MAGIC
# MAGIC 1.  **Immutable Parquet files**
# MAGIC     *   Once written, they never change.
# MAGIC
# MAGIC 2.  **Append-only transaction logs**
# MAGIC     *   Commit files cannot be overwritten.
# MAGIC
# MAGIC 3.  **Cloud storage durability**
# MAGIC     *   ADLS/S3/GCS internally maintain multiple replicas.
# MAGIC
# MAGIC 4.  **Checkpointing**
# MAGIC     *   Every N commits (default 10), Delta writes a *checkpoint*:
# MAGIC             /_delta_log/00000000000000000020.checkpoint.parquet
# MAGIC     *   Checkpoints combine all actions into one file  
# MAGIC         → Faster recovery  
# MAGIC         → Guaranteed durability
# MAGIC
# MAGIC Even if all Spark executors crash mid-job →  
# MAGIC **the commit JSON file still guarantees correctness**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## The Update / Delete / Insert Problem in a Data Lake
# MAGIC Traditional Data Lakes (like ADLS/S3 with Parquet/ORC files) were designed for append-only, immutable files, and not for transactional operations like:
# MAGIC
# MAGIC - UPDATE
# MAGIC - DELETE
# MAGIC - MERGE
# MAGIC - UPSERT
# MAGIC - INSERT INTO (in the presence of concurrent reads)
# MAGIC - Slowly Changing Dimensions (SCD type 1/2)
# MAGIC
# MAGIC This leads to data corruption, inconsistent reads, race conditions, and partial writes.
# MAGIC
# MAGIC Object storage (ADLS/S3/GCS) does not allow in-place modification of file contents.
# MAGIC So if you want to UPDATE or DELETE a record inside a Parquet file:
# MAGIC ❌ You cannot modify the file directly
# MAGIC Instead, you must:
# MAGIC
# MAGIC - Read the full Parquet file into Spark
# MAGIC - Modify the data in memory
# MAGIC - Rewrite a new Parquet file
# MAGIC - Delete the old file
# MAGIC - Replace it with the new one
# MAGIC
# MAGIC **Problems caused:**
# MAGIC - Very slow (rewriting entire partitions)
# MAGIC - Extremely expensive (I/O heavy)
# MAGIC - Risky (failure may leave partial files)
# MAGIC - Causes inconsistent reads while updates happen

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Quality and reliability issue
# MAGIC A **Data Lake** stores raw data of any type without strict schema or governance.  
# MAGIC Because of this flexibility, Data Lakes often suffer from **poor data quality**, leading to incorrect analytics, failed pipelines, inconsistencies, and “data swamps.”
# MAGIC
# MAGIC Below are the most important **data quality issues** you must understand.
# MAGIC 1.  Missing / incomplete data
# MAGIC 2.  Duplicate data
# MAGIC 3.  Invalid / incorrect values
# MAGIC 4.  Schema drift
# MAGIC 5.  Inconsistent data across files
# MAGIC 6.  Corrupted files
# MAGIC 7.  Stale data
# MAGIC 8.  No lineage
# MAGIC 9.  Poor data standardization
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **Why Data Lakes Are Prone to Data Quality Issues**
# MAGIC
# MAGIC Because traditional Data Lakes lack:
# MAGIC
# MAGIC *   Schema enforcement
# MAGIC *   Constraints
# MAGIC *   Primary keys
# MAGIC *   Data types validation
# MAGIC *   Transactions (ACID)
# MAGIC *   Metadata management
# MAGIC *   Standard ingestion frameworks
# MAGIC
# MAGIC A Data Lake accepts **ANY** file — good or bad — which leads to a “data swamp.”
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **How Delta Lake Fixes Data Quality Issues**
# MAGIC
# MAGIC | Issue in Data Lake      | Delta Lake Solution                      |
# MAGIC | ----------------------- | ---------------------------------------- |
# MAGIC | No schema enforcement   | Schema-on-write                          |
# MAGIC | Duplicate rows          | MERGE + PK enforcement logic             |
# MAGIC | Mixed schemas           | Automatic schema evolution + enforcement |
# MAGIC | Partial writes          | ACID transactions                        |
# MAGIC | Corrupted files         | Atomic commit protocol                   |
# MAGIC | Missing data            | Constraints + expectations               |
# MAGIC | Inconsistent partitions | Transaction log ensures consistency      |
# MAGIC | Stale data              | Time travel + versioning                 |
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## DML Operation on Delta table

# COMMAND ----------

# MAGIC %fs ls abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_101_200`

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bi_dev.mo.invoices
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_101_200`;
# MAGIC     
# MAGIC SELECT *
# MAGIC FROM bi_dev.mo.invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY bi_dev.mo.invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices
# MAGIC SELECT *
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_1_100`

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY bi_dev.mo.invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM bi_dev.mo.invoices
# MAGIC WHERE customer_id = 1

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE bi_dev.mo.invoices
# MAGIC SET quantity = 15
# MAGIC WHERE customer_id = 1

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY bi_dev.mo.invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM bi_dev.mo.invoices
# MAGIC WHERE customer_id = 99

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE
# MAGIC FROM bi_dev.mo.invoices
# MAGIC WHERE customer_id = 99

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices
# MAGIC SELECT *
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_201_99457`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Compacted JSON and Checkpoints

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC
# MAGIC ### 1) **Commit JSONs**
# MAGIC
# MAGIC     00000000000000000001.json
# MAGIC     00000000000000000002.json
# MAGIC     ...
# MAGIC
# MAGIC Each is an **atomic commit** with actions like `add`, `remove`, `metaData`, etc. This is the canonical transaction history. [\[databricks.com\]](https://www.databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html)
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 2) **Compacted JSONs**
# MAGIC
# MAGIC     00000000000000000001.00000000000000000006.compacted.json
# MAGIC
# MAGIC *   Pattern: `{start}.{end}.compacted.json`
# MAGIC *   Meaning: a **single aggregated JSON** covering the actions from **version `start` through `end`**.  
# MAGIC     In your example: **versions 1–6**. These are an *optimization* to reduce the number of tiny log files readers must replay. [\[deepwiki.com\]](https://deepwiki.com/delta-io/delta/2.1-transaction-log-protocol), [\[github.com\]](https://github.com/delta-io/delta/blob/master/PROTOCOL.md)
# MAGIC
# MAGIC > ✅ This exactly matches the names you’re seeing like `01.06.compacted.json`: it’s a compaction of commits 1 through 6.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 3) **Checkpoint Parquet**
# MAGIC
# MAGIC     00000000000000000036.checkpoint.parquet
# MAGIC
# MAGIC *   A **snapshot of full table state** as of a particular version, stored in **Parquet** (v2 checkpoints).
# MAGIC *   Readers start from the latest checkpoint ≤ target version, then apply subsequent JSONs (and may use compacted JSONs to speed that up). [\[dennyglee.com\]](https://dennyglee.com/2024/01/09/computing-delta-lake-state-quickly-with-checkpoint-files/)
# MAGIC
# MAGIC ***

# COMMAND ----------

for i in range(38):
    spark.sql("INSERT INTO bi_dev.mo.invoices SELECT * FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_1_100`")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Concurrency Control in Delta Lake
# MAGIC
# MAGIC **What is concurrency control?**
# MAGIC
# MAGIC Concurrency control defines **how a data system handles multiple users or jobs reading and writing the same data simultaneously** while preserving **data correctness and consistency**.
# MAGIC
# MAGIC Delta Lake uses **Optimistic Concurrency Control (OCC)** — **not** pessimistic locking.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 1. Pessimistic Concurrency Control (Concept)
# MAGIC
# MAGIC **Definition**
# MAGIC Pessimistic concurrency control **assumes conflicts will happen**, so it **prevents them upfront** by using **locks**.
# MAGIC
# MAGIC **How it works**
# MAGIC
# MAGIC *   A transaction **locks** data before modifying it
# MAGIC *   Other transactions must **wait** until the lock is released
# MAGIC *   Guarantees strong isolation, but reduces parallelism
# MAGIC
# MAGIC **Typical flow**
# MAGIC
# MAGIC     1. Transaction A acquires lock on table/rows
# MAGIC     2. Transaction B tries to write → blocked
# MAGIC     3. Transaction A commits
# MAGIC     4. Lock released
# MAGIC     5. Transaction B proceeds
# MAGIC
# MAGIC **Example systems using it**
# MAGIC
# MAGIC *   Traditional RDBMS (Oracle, SQL Server)
# MAGIC *   Row-level or table-level locking systems
# MAGIC
# MAGIC **Problems for big data / lakehouse**
# MAGIC
# MAGIC *   Long-running jobs block others
# MAGIC *   Poor scalability
# MAGIC *   High contention in distributed systems
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 2. Optimistic Concurrency Control (OCC) – Used by Delta Lake
# MAGIC
# MAGIC **Definition**
# MAGIC
# MAGIC Optimistic concurrency control **assumes conflicts are rare** and **detects conflicts only at commit time**.
# MAGIC
# MAGIC Instead of locking data, transactions:
# MAGIC
# MAGIC *   Read **a snapshot**
# MAGIC *   Make changes independently
# MAGIC *   Validate before committing
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **How Delta Lake Implements Optimistic Concurrency Control**
# MAGIC
# MAGIC Delta Lake relies on:
# MAGIC
# MAGIC *   **Immutable Parquet files**
# MAGIC *   **Transaction log (\_delta\_log)**
# MAGIC *   **Atomic commits**
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **Delta Lake OCC – Step-by-Step**
# MAGIC
# MAGIC **Step 1: Read (Snapshot Isolation)**
# MAGIC
# MAGIC Each transaction reads from a **consistent snapshot** of the table.
# MAGIC
# MAGIC ```text
# MAGIC Transaction reads delta version v10
# MAGIC ```
# MAGIC
# MAGIC No locks are taken.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **Step 2: Write (Create New Files)**
# MAGIC
# MAGIC Instead of updating files:
# MAGIC
# MAGIC *   Delta creates **new Parquet files**
# MAGIC *   Old files are untouched
# MAGIC
# MAGIC ```text
# MAGIC UPDATE → writes new data files
# MAGIC ```
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **Step 3: Validate (Conflict Detection)**
# MAGIC
# MAGIC Before commit, Delta checks:
# MAGIC
# MAGIC *   Has the table changed since the transaction started?
# MAGIC *   Do new commits conflict with this transaction?
# MAGIC
# MAGIC Conflict checks depend on the operation type.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC **Step 4: Commit (Atomic)**
# MAGIC
# MAGIC If **no conflicts**:
# MAGIC
# MAGIC *   Delta writes a new JSON entry to `_delta_log`
# MAGIC *   Commit is **atomic**
# MAGIC
# MAGIC If **conflict detected**:
# MAGIC
# MAGIC *   Transaction **fails**
# MAGIC *   Caller must **retry**
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## Example Timeline
# MAGIC
# MAGIC | Time | Transaction A         | Transaction B     |
# MAGIC | ---- | --------------------- | ----------------- |
# MAGIC | T1   | Reads version 5       | Reads version 5   |
# MAGIC | T2   | Writes new files      | Writes new files  |
# MAGIC | T3   | Commits → version 6 ✅ | Tries commit ❌    |
# MAGIC | T4   | —                     | Conflict detected |
# MAGIC
# MAGIC 👉 **Transaction B fails and must retry**
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC | Aspect             | Pessimistic CC       | Optimistic CC (Delta Lake) |
# MAGIC | ------------------ | -------------------- | -------------------------- |
# MAGIC | Assumption         | Conflicts are common | Conflicts are rare         |
# MAGIC | Locking            | Yes                  | No                         |
# MAGIC | Scalability        | Poor                 | High                       |
# MAGIC | Failure Handling   | Blocks others        | Fails & retries            |
# MAGIC | Used by Delta Lake | ❌ No                 | ✅ Yes                      |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Time Travel and Versioning

# COMMAND ----------

# MAGIC %md
# MAGIC A Delta table is not just “data”—it is data + transaction history. Every time you make a change to a Delta table—such as:
# MAGIC - INSERT
# MAGIC - UPDATE
# MAGIC - DELETE
# MAGIC - MERGE
# MAGIC - OVERWRITE
# MAGIC
# MAGIC Delta Lake creates a new version of that table. A Delta table behaves like a Git repository for data.
# MAGIC
# MAGIC **Time travel** allows you to query a Delta table as it existed at a previous point in time.
# MAGIC You can query:
# MAGIC - By version number
# MAGIC - By timestamp

# COMMAND ----------

# MAGIC %md
# MAGIC Delta Lake provides a **DESCRIBE HISTORY** command

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY bi_dev.mo.invoices;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Time Travel by Version Number

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM bi_dev.mo.invoices
# MAGIC VERSION AS OF 5;

# COMMAND ----------

df = spark.read.option("versionAsOf", 1).table("bi_dev.mo.invoices")
df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC ###  Time Travel by Timestamp

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM bi_dev.mo.invoices
# MAGIC TIMESTAMP AS OF '2025-01-05 10:30:00';

# COMMAND ----------

df = spark.read.option("timestampAsOf", "2025-01-05 10:30:00").table("bi_dev.mo.invoices")
df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Restoring a Delta Table to an Older Version
# MAGIC You can restore (not just query) an old version.

# COMMAND ----------

# MAGIC %sql
# MAGIC RESTORE TABLE bi_dev.mo.invoices TO VERSION AS OF 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC RESTORE TABLE bi_dev.mo.invoices TO TIMESTAMP AS OF '2025-01-05 10:30:00';

# COMMAND ----------

# MAGIC %md
# MAGIC ## Schema Validation/ Schema Enforcement
# MAGIC - Schema enforcement is a Delta Lake feature that prevents you from appending data with a different schema to a table unless you explicitly specify that the table should allow data with different schemas to be written
# MAGIC - Parquet tables don't support built-in schema enforcement, so they accept data with any schema. 
# MAGIC - Data lakes (e.g. Parquet tables) are schema-on-read, which means execution engines need to determine the schema when running queries. Data warehouses are schema-on-write, which means they check the schema when data is written.
# MAGIC - You can also set a Spark property that will enable autoMerge by default. Once this property is set, you don't need to manually set mergeSchema to true when writing data with a different schema to a Delta table.
# MAGIC   ```py
# MAGIC   spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
# MAGIC   ```
# MAGIC **Note**: Delta Lakes are aware when data with other schemas have been appended. Delta Lake works out the final schema for the table by querying the transaction log, not by opening all the individual Parquet files. This makes schema evolution with Delta tables fast and more convenient for the user.

# COMMAND ----------

# MAGIC %md
# MAGIC **1. What is Schema-on-read / Schema-on-write?**
# MAGIC ![Schema Validation](/Workspace/Users/mo@fastenal.com/Delta Lake/SchemaValidation.png)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bi_dev.mo.invoice_sv (
# MAGIC   customer_id INT NOT NULL,
# MAGIC   invoice_no STRING,
# MAGIC   quantity INT,
# MAGIC   PRICE FLOAT,
# MAGIC   invoice_date DATE
# MAGIC );
# MAGIC
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC SELECT customer_id, invoice_no, quantity, price, invoice_date
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_1_100`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM bi_dev.mo.invoice_sv

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 1: Column Order Validation
# MAGIC 1. Insert does not match the column name
# MAGIC 2. Merge matches the column name

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC SELECT quantity, invoice_no, customer_id, price, invoice_date
# MAGIC FROM VALUES (99999, 'I12345', 10, 100, '2025-01-01')
# MAGIC AS T(customer_id, invoice_no, quantity, price, invoice_date)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoice_sv
# MAGIC WHERE customer_id = 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO bi_dev.mo.invoice_sv AS tgt
# MAGIC USING (
# MAGIC   SELECT quantity, invoice_no, customer_id, CAST (price AS FLOAT), invoice_date
# MAGIC   FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_101_200`
# MAGIC   ORDER BY customer_id DESC LIMIT 5
# MAGIC ) src 
# MAGIC ON tgt.customer_id = src.customer_id
# MAGIC WHEN MATCHED THEN 
# MAGIC   UPDATE SET 
# MAGIC     tgt.customer_id = src.customer_id,
# MAGIC     tgt.invoice_no = src.invoice_no,
# MAGIC     tgt.quantity = src.quantity,
# MAGIC     tgt.price = src.price,
# MAGIC     tgt.invoice_date = current_date
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT * 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoice_sv
# MAGIC WHERE customer_id > 100;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 2: Data Type Validation
# MAGIC Delta table try to convert inserted values to match the column datatype. If the casting succeeds then it will insert else it will fail.

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC VALUES (
# MAGIC   'ABC', 
# MAGIC   'I45678',
# MAGIC   10,
# MAGIC   98.75,
# MAGIC   '2025-01-01'
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC VALUES (
# MAGIC   '99499', 
# MAGIC   'I45678',
# MAGIC   10,
# MAGIC   98.75,
# MAGIC   '2025-01-01'
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoice_sv
# MAGIC WHERE customer_id = 99499;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 3: Data Name Validation
# MAGIC - INSERT matches the column position
# MAGIC - MERGE matches the column name

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC SELECT customer_id AS c_id, invoice_no, quantity AS qty, price, invoice_date
# MAGIC FROM VALUES (9998, 'I12345', 10, 100, '2025-01-01')
# MAGIC AS T(customer_id, invoice_no, quantity, price, invoice_date)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoice_sv
# MAGIC WHERE customer_id = 9998;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO bi_dev.mo.invoice_sv AS tgt
# MAGIC USING (
# MAGIC   SELECT customer_id AS c_id, invoice_no, quantity AS qty, CAST(price AS FLOAT) AS price, invoice_date
# MAGIC   FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_101_200`
# MAGIC   ORDER BY customer_id LIMIT 5
# MAGIC ) src 
# MAGIC ON tgt.customer_id = src.c_id
# MAGIC WHEN MATCHED THEN 
# MAGIC   UPDATE SET 
# MAGIC     tgt.customer_id = src.c_id,
# MAGIC     tgt.invoice_no = src.invoice_no,
# MAGIC     tgt.quantity = src.qty,
# MAGIC     tgt.price = src.price,
# MAGIC     tgt.invoice_date = current_date
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT * 

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 4: Nullability Validation

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC VALUES (NULL, NULL, NULL, NULL, NULL);

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 5: Extra columns validation

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoice_sv
# MAGIC SELECT customer_id, invoice_no, quantity, price, invoice_date, "VIP" AS customer_type
# MAGIC FROM VALUES (78999, 'I12345', 10, 100, '2025-01-01')
# MAGIC AS T(customer_id, invoice_no, quantity, price, invoice_date)

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO bi_dev.mo.invoice_sv AS tgt
# MAGIC USING (
# MAGIC   SELECT customer_id, invoice_no, quantity, price, "VIP" AS customer_type, invoice_date
# MAGIC   FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_101_200`
# MAGIC   WHERE customer_id BETWEEN 160 AND 165
# MAGIC ) src 
# MAGIC ON tgt.customer_id = src.customer_id
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT * 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM bi_dev.mo.invoice_sv
# MAGIC WHERE customer_id BETWEEN 160 AND 165

# COMMAND ----------

# MAGIC %md
# MAGIC ## mergeSchema VS overwriteSchema
# MAGIC
# MAGIC 1. **mergeSchema: Adding New Columns**  
# MAGIC If your incoming DataFrame has extra columns that are not present in the Delta table, you can use mergeSchema=True to automatically merge the new schema.
# MAGIC
# MAGIC 2. **What Happens If You Use mergeSchema for Type Changes?**  
# MAGIC A common misconception is that mergeSchema can also handle datatype changes. mergeSchema cannot change datatypes. It only adds new columns.
# MAGIC
# MAGIC 3. **overwriteSchema: Changing Column Types**  
# MAGIC - When you truly need to change the datatype of an existing column, use overwriteSchema=True. This replaces the table's schema with the new DataFrame's schema.
# MAGIC - This works only with overwrite mode not append
# MAGIC
# MAGIC **Note**
# MAGIC 1. Overwrite mode works with both mergeSchema and overwriteSchema.
# MAGIC 2. Append mode supports mergeSchema only — not overwriteSchema.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Schema Evolution
# MAGIC 1. Adding New Columns (Manual / Automatic)
# MAGIC 2. Widening Data Types (Supported Delta >= 3.2): Sometimes we need to expand a column's data type to accommodate larger values. Delta Lake allows "widening" type conversions that won't lose data, such as:
# MAGIC - `INT` to `BIGINT`
# MAGIC - `FLOAT` to `DOUBLE`
# MAGIC - `VARCHAR(10)` to `VARCHAR(20)`
# MAGIC
# MAGIC 3. Nested Structure Evolution (Manual / Automatic): Delta Lake supports evolution of complex data types like structs and arrays. We can:
# MAGIC - Add new fields to structs
# MAGIC - Modify nested field types
# MAGIC - Add new elements to arrays
# MAGIC
# MAGIC 4. Column Position Changes (Manual / Automatic): we can reorganize our columns
# MAGIC
# MAGIC Note: 
# MAGIC - `INSERT` works by matching columns by position
# MAGIC - `MERGE` works by matching columns by name

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 1: Adding New Columns 

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/Invoices/invoices_1_100.parquet`
# MAGIC WHERE customer_id BETWEEN 1 AND 5

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bi_dev.mo.invoices_se (
# MAGIC   customer_id INT NOT NULL,  
# MAGIC   invoice_no STRING,
# MAGIC   price FLOAT, 
# MAGIC   invoice_date DATE
# MAGIC ); 
# MAGIC
# MAGIC INSERT INTO bi_dev.mo.invoices_se
# MAGIC SELECT customer_id, invoice_no, price, invoice_date
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/Invoices/invoices_1_100.parquet`
# MAGIC WHERE customer_id BETWEEN 1 AND 5

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE bi_dev.mo.invoices_se
# MAGIC ADD COLUMNS (quantity INT);

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se
# MAGIC SELECT customer_id, invoice_no, price, invoice_date, quantity
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/Invoices/invoices_1_100.parquet`
# MAGIC WHERE customer_id BETWEEN 6 AND 10 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

SET spark.databricks.delta.schema.autoMerge.enabled = true;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se
# MAGIC SELECT customer_id, invoice_no, price, invoice_date, quantity, payment_method 
# MAGIC FROM PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/Invoices/invoices_1_100.parquet`
# MAGIC WHERE customer_id BETWEEN 11 AND 15 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 2: Type Widening

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE bi_dev.mo.invoices_se 
# MAGIC SET TBLPROPERTIES ('delta.enableTypeWidening' = 'true');

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE bi_dev.mo.invoices_se; 

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se 
# MAGIC VALUES (123456789012345,	'I106485',	30.299999237060547,	'2022-12-01',	2,	'Debit Card')

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE bi_dev.mo.invoices_se
# MAGIC ALTER COLUMN customer_id TYPE BIGINT;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO deltacatalog.deltadb.invoices_se 
# MAGIC VALUES (123456789012345,	'I106485',	30.299999237060547,	'2022-12-01',	2,	'Debit Card')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se
# MAGIC WHERE customer_id = 123456789012345;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 3: Nested Structure Evolution

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE bi_dev.mo.invoices_se
# MAGIC ADD COLUMNS purchase_details STRUCT<
# MAGIC   mall_pin_code INT,
# MAGIC   store_code INT
# MAGIC >;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se 
# MAGIC VALUES (16,	'I106485',	30.299999237060547,	'2022-12-01',	2,	'Debit Card', STRUCT(12345, 879));

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE bi_dev.mo.invoices_se
# MAGIC ALTER COLUMN purchase_details.mall_pin_code TYPE BIGINT;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se 
# MAGIC VALUES (17,	'I106485',	30.299999237060547,	'2022-12-01',	2,	'Debit Card', STRUCT(123456789012346, 765));

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE bi_dev.mo.invoices_se
# MAGIC ADD COLUMN purchase_details.store_loc STRING;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se 
# MAGIC VALUES (17,	'I106485',	30.299999237060547,	'2022-12-01',	2,	'Debit Card', STRUCT(7612, 765, 'ground floor'));

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO bi_dev.mo.invoices_se 
# MAGIC VALUES (21,	'I106485',	30.299999237060547,	'2022-12-01',	2,	'Debit Card', 
# MAGIC   NAMED_STRUCT(
# MAGIC     'mall_pin_code', 7612, 
# MAGIC     'store_code', 765, 
# MAGIC     'store_loc', 'ground floor', 
# MAGIC     'staff_id', 'ST12736'
# MAGIC   )
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bi_dev.mo.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Scenario 4: Column Position Changes

# COMMAND ----------

# MAGIC %sql
# MAGIC SET spark.databricks.delta.schema.autoMerge.enabled=false;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ALTER TABLE deltacatalog.deltadb.invoices_se ADD COLUMNS (age INT FIRST);
# MAGIC ALTER TABLE deltacatalog.deltadb.invoices_se ADD COLUMNS (age INT AFTER price)

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO deltacatalog.deltadb.invoices_se
# MAGIC SELECT customer_id, invoice_no, price, age, invoice_date, quantity, payment_method, NULL AS purchase_details
# MAGIC FROM PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC WHERE customer_id BETWEEN 50 AND 55

# COMMAND ----------

# MAGIC %sql
# MAGIC SET spark.databricks.delta.schema.autoMerge.enabled = true;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_se;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO deltacatalog.deltadb.invoices_se
# MAGIC SELECT customer_id, invoice_no, price, age, invoice_date, quantity, payment_method, category, NULL AS purchase_details
# MAGIC FROM PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC WHERE customer_id BETWEEN 56 AND 60

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO deltacatalog.deltadb.invoices_se tgt
# MAGIC USING (
# MAGIC   SELECT customer_id, invoice_no, price, age, invoice_date, quantity, payment_method, category, NULL AS purchase_details
# MAGIC   FROM PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE customer_id BETWEEN 56 AND 60
# MAGIC ) src 
# MAGIC ON tgt.customer_id = src.customer_id
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT *

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_se;

# COMMAND ----------

from pyspark.sql.functions import *
df = (
  spark.read.parquet("abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_1_100.parquet")
  .filter(col("customer_id").between(1, 10))
  .select("customer_id", "price", "invoice_date")
)
df.write.saveAsTable("deltacatalog.deltadb.invoices_se_spark_df")

# COMMAND ----------

df = (
  spark.read.parquet("abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_1_100.parquet")
  .filter(col("customer_id").between(11, 25))
  .select("customer_id", "price", "invoice_date", "quantity", "payment_method")
)
df.write.mode("append").option("mergeSchema", "true").saveAsTable("deltacatalog.deltadb.invoices_se_spark_df")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Convert Parquet to Delta

# COMMAND ----------

df = spark.read.parquet(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices/invoices_1_100"
)

df.write.mode('overwrite').parquet(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices_v1"
)

df.write.mode('overwrite').parquet(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices_v2"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC CONVERT TO DELTA PARQUET.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices_v1`

# COMMAND ----------

from delta.tables import DeltaTable

DeltaTable.convertToDelta(
    spark,
    "parquet.`abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices_v2`",
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Managed and External Tables

# COMMAND ----------

# MAGIC %md
# MAGIC **Managed Table**
# MAGIC
# MAGIC When you create a managed table, Databricks takes care of everything. Managed tables are the default type of table in Spark:
# MAGIC   - It decides where to store the data
# MAGIC   - It controls how the data is managed
# MAGIC   - If you drop the table, the data is deleted too!!

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bi_dev.mo.sales_data (
# MAGIC   id INT,
# MAGIC   revenue DOUBLE
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %md
# MAGIC **External Table**
# MAGIC
# MAGIC An external table means you point Databricks to data you already have somewhere else—maybe in a HDFS, relational database, data lake or on S3. External tables are designed to access data stored outside of Spark’s control.
# MAGIC   - You manage the location
# MAGIC   - Databricks reads the data, but doesn’t own it
# MAGIC   - Dropping the table does not delete the data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE bi_dev.mo.invoices_v3
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/delta_course/invoices_v3' AS
# MAGIC SELECT *
# MAGIC FROM bi_dev.mo.invoices ;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Shallow Clones

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE deltacatalog.deltadb.invoices_c1_100
# MAGIC AS
# MAGIC SELECT * FROM 
# MAGIC PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_c1_100
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM deltacatalog.deltadb.invoices_c1_100
# MAGIC WHERE customer_id BETWEEN 15 AND 20; 

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE deltacatalog.deltadb.invoices_c1_100
# MAGIC SET quantity = 10
# MAGIC WHERE customer_id = 3

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO deltacatalog.deltadb.invoices_c1_100
# MAGIC VALUES (1099,	'I178410',	'Male',	61,	'Clothing',	5,	1500.4,	'Credit Card',	'2021-11-26',	'Metrocity',	null);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE deltacatalog.deltadb.invoices_c1_100_scl SHALLOW CLONE deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100_scl;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_c1_100 LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE deltacatalog.deltadb.invoices_c1_100
# MAGIC SET quantity = 10
# MAGIC WHERE customer_id = 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_c1_100
# MAGIC WHERE customer_id = 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_c1_100_scl
# MAGIC WHERE customer_id = 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM deltacatalog.deltadb.invoices_c1_100_scl
# MAGIC WHERE customer_id = 99;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_c1_100_scl
# MAGIC WHERE customer_id = 99; 

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100_scl;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM deltacatalog.deltadb.invoices_c1_100
# MAGIC WHERE customer_id = 99; 

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deep Clone

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE deltacatalog.deltadb.invoices_c1_100_dcl DEEP CLONE deltacatalog.deltadb.invoices_c1_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_c1_100_dcl;

# COMMAND ----------

# MAGIC %md
# MAGIC **What is difference between CTAS and DEEP Clone?**
# MAGIC
# MAGIC - **CTAS (Create Table As Select):**
# MAGIC   - Creates a new table from the results of a SELECT query.
# MAGIC   - Only copies the data returned by the query.
# MAGIC   - Does not copy table metadata, history, or properties.
# MAGIC
# MAGIC - **DEEP Clone:**
# MAGIC   - Creates a new Delta table by copying all data files, metadata, and transaction history.
# MAGIC   - The clone is a full, independent copy of the original table.
# MAGIC   - Useful for backup, testing, or migration.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deletion Vector
# MAGIC A **deletion vector** in Delta Lake is a storage optimization feature that marks rows as deleted or updated without rewriting the entire Parquet file. Instead of physically removing data, deletion vectors record which rows are logically deleted or modified, making DELETE, UPDATE, and MERGE operations much faster and more efficient.
# MAGIC
# MAGIC - **How it works:**  
# MAGIC   - When you delete or update rows, Delta Lake creates a deletion vector that tracks which rows are affected.
# MAGIC   - Reads apply these vectors to show the current state of the table.
# MAGIC   - The underlying data files remain unchanged until a vacuum or purge operation.
# MAGIC
# MAGIC - **Benefits:**  
# MAGIC   - Faster DELETE, UPDATE, and MERGE operations.
# MAGIC   - Reduces I/O and storage costs.
# MAGIC   - Enables row-level concurrency and efficient modifications.
# MAGIC
# MAGIC - **Note:**  Supported in Databricks Runtime 12.2 LTS and above.

# COMMAND ----------

# MAGIC %md
# MAGIC ### CoW (Copy-on-Write)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM 
# MAGIC PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE deltacatalog.deltadb.invoices_cow 
# MAGIC TBLPROPERTIES ('delta.enableDeletionVectors' = false)
# MAGIC AS 
# MAGIC SELECT * FROM 
# MAGIC PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_101_200.parquet`;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED deltacatalog.deltadb.invoices_cow;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE deltacatalog.deltadb.invoices_cow 
# MAGIC SET age = 55 
# MAGIC WHERE customer_id = 105;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_cow;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM deltacatalog.deltadb.invoices_cow 
# MAGIC WHERE customer_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_cow;

# COMMAND ----------

# MAGIC %md
# MAGIC ### MoR (Merge-on-Read)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE deltacatalog.deltadb.invoices_mor
# MAGIC TBLPROPERTIES ('delta.enableDeletionVectors' = true)
# MAGIC AS 
# MAGIC SELECT * FROM 
# MAGIC PARQUET.`abfss://labdata@dbdeltalabstorageacct.dfs.core.windows.net/invoices/invoices_101_200.parquet`;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED deltacatalog.deltadb.invoices_mor;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM deltacatalog.deltadb.invoices_mor
# MAGIC WHERE customer_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_mor;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE deltacatalog.deltadb.invoices_mor
# MAGIC SET age = 55 
# MAGIC WHERE customer_id = 105;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY deltacatalog.deltadb.invoices_mor;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optimize
# MAGIC
# MAGIC - Compacts small files into larger, more efficient sizes.
# MAGIC - Uses the Binpacking algorithm in Spark:
# MAGIC     - Files are sorted by size (largest first).
# MAGIC     - Files are placed into bins to maximize bin utilization.
# MAGIC     - Default bin size is **1 GB** (can be changed).
# MAGIC     - Bin size can be set via: spark.databricks.delta.optimize.maxFileSize
# MAGIC     - Helps reduce the number of small files, improving read performance and resource utilization.
# MAGIC
# MAGIC ### Root Causes for Small Size Files:
# MAGIC
# MAGIC
# MAGIC #### 1. Repartition
# MAGIC
# MAGIC *   **10 GB → 10,000**
# MAGIC *   `df.repartition(10000)`
# MAGIC *   (Right side note:)
# MAGIC         10 × 1000 MB
# MAGIC         ---------------
# MAGIC              10,000
# MAGIC             = 1 MB
# MAGIC
# MAGIC #### 2. Partitioning → High Cardinality Column
# MAGIC
# MAGIC *   **500 MB** dataset
# MAGIC *   **Category → 1000's**
# MAGIC *   `df.write.partitionBy("category")`
# MAGIC
# MAGIC #### 3. Frequently updated datasets: 5 mins
# MAGIC
# MAGIC *   Small updates → small files
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F
df = spark.read.table("de_prd.base_psoft.ps_fzbi_invc_dtl").filter(
    F.trunc(F.col("invoice_dt"), 'year') == F.to_date(F.lit("2026-01-01"), "yyyy-MM-dd")
)

# COMMAND ----------

df.rdd.getNumPartitions()

# COMMAND ----------

df.write.format("delta").mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/filtered_invoice",
).saveAsTable("bi_dev.mo.filtered_invoice")

# COMMAND ----------

df.write.format("delta").mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/filtered_invoice_optimize",
).saveAsTable("bi_dev.mo.filtered_invoice_optimize")

# COMMAND ----------

from delta.tables import DeltaTable
table = DeltaTable.forName(spark, "bi_dev.mo.filtered_invoice_optimize")
table.optimize().executeCompaction()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Optimize VS Without Optimize

# COMMAND ----------

optimize_df = spark.read.table("bi_dev.mo.filtered_invoice_optimize")
optimize_df.collect()

# COMMAND ----------

optimize_wo_df = spark.read.table("bi_dev.mo.filtered_invoice")
optimize_wo_df.collect()

# COMMAND ----------

# MAGIC %sql 
# MAGIC SET spark.databricks.delta.retentionDurationCheck.enabled = false;

# COMMAND ----------

table.vacuum(0)

# COMMAND ----------

## SQL Command to optimize the table
spark.sql("OPTIMIZE bi_dev.mo.filtered_invoice")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Optimizing specific partitions

# COMMAND ----------

df.withColumn("invoice_month", F.trunc(F.col("invoice_dt"), "month")).write.partitionBy(
    "invoice_month"
).mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/partition_invoice",
).saveAsTable(
    "bi_dev.mo.partition_invoice"
)

# COMMAND ----------

table = DeltaTable.forName(spark, "bi_dev.mo.partition_invoice")
table.optimize().where("invoice_month = '2026-02-01'").executeCompaction()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Automatic Optimize: Optimize Write
# MAGIC Optimize Write is a feature in Databricks that automatically compacts small files during write operations. When enabled, it reduces the creation of small files by combining data into larger, more efficient files as data is written, improving read performance and resource utilization without requiring manual optimization steps. It doesn't write smaller files first instead it puts all the data on same node, combines it and then writes into storage

# COMMAND ----------

# This write will create 8 files in each partition
from pyspark.sql import functions as F

df = spark.read.table("de_prd.base_psoft.ps_fzbi_invc_dtl").filter(
    F.trunc(F.col("invoice_dt"), "month")
    == F.to_date(F.lit("2026-03-01"), "yyyy-MM-dd")
).repartition(8)

df.write.format("delta").partitionBy("invoice_dt").mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/invoice_optimize_partition",
).saveAsTable("bi_dev.mo.invoice_optimize_partition")

# COMMAND ----------

df.write.format("delta").partitionBy("invoice_dt").mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/invoice_optimize_partition_write",
).option("optimizeWrite", True).saveAsTable(
    "bi_dev.mo.invoice_optimize_partition_write"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Auto Compaction
# MAGIC Auto Compaction is a Databricks feature that automatically merges small files into larger ones during write operations. This process helps optimize storage and improves query performance by reducing the number of small files, minimizing overhead, and making data access more efficient. It works in the background without manual intervention.
# MAGIC
# MAGIC ### Auto Compaction vs Optimize Write
# MAGIC
# MAGIC **Optimize Write** automatically combines data into larger files during write operations, reducing the creation of small files as data is written.
# MAGIC
# MAGIC **Auto Compaction** works in the background after data is written, merging existing small files into larger ones to further optimize storage and query performance.
# MAGIC
# MAGIC - *Optimize Write*: Prevents small files at write time.
# MAGIC - *Auto Compaction*: Merges small files after write, running in the background.

# COMMAND ----------

spark.conf.set("spark.databricks.delta.autoCompact.minNumFiles", 8)

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.read.table("de_prd.base_psoft.ps_fzbi_invc_dtl").filter(
    F.trunc(F.col("invoice_dt"), "month")
    == F.to_date(F.lit("2026-03-01"), "yyyy-MM-dd")
).repartition(8)

df.write.format("delta").partitionBy("invoice_dt").mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/invoice_autocompaction",
).saveAsTable("bi_dev.mo.invoice_autocompaction")

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE
# MAGIC   bi_dev.mo.invoice_autocompaction
# MAGIC SET TBLPROPERTIES (
# MAGIC   "spark.databricks.delta.autoCompact.enabled" = "true");
# MAGIC
# MAGIC ALTER TABLE
# MAGIC   bi_dev.mo.invoice_autocompaction
# MAGIC SET TBLPROPERTIES (
# MAGIC   "spark.databricks.delta.optimizeWrite.enabled" = "false")

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.read.table("de_prd.base_psoft.ps_fzbi_invc_dtl").filter(
    F.trunc(F.col("invoice_dt"), "month")
    == F.to_date(F.lit("2026-02-01"), "yyyy-MM-dd")
).repartition(8)

df.write.format("delta").partitionBy("invoice_dt").mode("overwrite").option(
    "path",
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/invoice_autocompaction",
).saveAsTable("bi_dev.mo.invoice_autocompaction")

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC ## Delta Retention Period
# MAGIC
# MAGIC Delta Lake maintains historical versions of data to support **Time Travel** and **VACUUM** operations. The retention period controls how long old data files and transaction log entries are kept before they can be cleaned up.
# MAGIC
# MAGIC ### Two Retention Settings
# MAGIC
# MAGIC #### 1. `delta.deletedFileRetentionDuration` (default: **7 days**)
# MAGIC - Controls how long deleted data files (Parquet files) are retained on storage.
# MAGIC - Used by the `VACUUM` command — only files older than this threshold are removed.
# MAGIC - Example: After an `UPDATE` or `DELETE`, the old Parquet files are kept for 7 days before `VACUUM` can clean them.
# MAGIC
# MAGIC #### 2. `delta.logRetentionDuration` (default: **30 days**)
# MAGIC - Controls how long the Delta transaction log (JSON + checkpoint files in `_delta_log/`) is retained.
# MAGIC - Determines how far back **Time Travel** queries can go.
# MAGIC - After this period, log entries are cleaned up during checkpointing.
# MAGIC
# MAGIC ### How to Change Retention
# MAGIC
# MAGIC ```sql
# MAGIC -- Change deleted file retention to 30 days
# MAGIC ALTER TABLE my_catalog.my_schema.my_table
# MAGIC SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 30 days');
# MAGIC
# MAGIC -- Change log retention to 60 days
# MAGIC ALTER TABLE my_catalog.my_schema.my_table
# MAGIC SET TBLPROPERTIES ('delta.logRetentionDuration' = 'interval 60 days');
# MAGIC ```
# MAGIC
# MAGIC ### Key Points
# MAGIC - `VACUUM` removes files older than `deletedFileRetentionDuration` — it does **not** delete the transaction log.
# MAGIC - Setting retention to `0` is dangerous — it disables the safety check (`retentionDurationCheck`) and can break concurrent readers.
# MAGIC - The safety check `spark.databricks.delta.retentionDurationCheck.enabled = false` (used in Cell 164) must be explicitly disabled to allow `VACUUM` with retention < 7 days.
# MAGIC - **Time Travel** depends on **both** the log retention (to know which version to query) and the file retention (to have the actual data files available).

# COMMAND ----------

# MAGIC %sql
# MAGIC desired_deleted_file_retention = "interval 60 days"
# MAGIC desired_log_retention = "interval 60 days"
# MAGIC ALTER TABLE {table_full_name} SET TBLPROPERTIES (delta.logRetentionDuration = '{desired_log_retention}')
# MAGIC ALTER TABLE {table_full_name} SET TBLPROPERTIES (delta.deletedFileRetentionDuration = '{desired_deleted_file_retention}')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Layout Optimization
# MAGIC ### Z Ordering
# MAGIC Z-Ordering is a technique that physically reorganizes data within files by interleaving values from multiple columns. Think of it as creating a multi-dimensional index that preserves data locality across several dimensions simultaneously.
# MAGIC
# MAGIC The algorithm uses a space-filling curve (the Z-order curve) that maps multi-dimensional data to one dimension while maintaining locality. This means that rows with similar values across multiple columns end up physically close to each other in storage.  
# MAGIC
# MAGIC **How Z-Ordering Works**
# MAGIC
# MAGIC When you run OPTIMIZE table_name ZORDER BY (col1, col2, col3), Delta Lake:
# MAGIC - Reads data from existing files
# MAGIC - Sorts data using the Z-order curve algorithm across specified columns
# MAGIC - Writes new compacted files with the optimized layout
# MAGIC - Updates metadata with new file statistics
# MAGIC - Marks old files for deletion (handled by VACUUM)
# MAGIC
# MAGIC ```sql
# MAGIC OPTIMIZE sales_transactions
# MAGIC ZORDER BY (order_date, customer_id, product_category);
# MAGIC ```
# MAGIC
# MAGIC ### Liquid Clustering
# MAGIC - Liquid clustering provides flexibility to redefine clustering columns without rewriting existing data, allowing data layout to evolve alongside analytic needs over time.
# MAGIC - Liquid Clustering allows you to change the clustering keys without rewriting existing data during the ALTER operation, which is metadata-only.
# MAGIC - If you want existing data to be reorganized according to the new keys, you must run OPTIMIZE, which incrementally reclusters data.
# MAGIC ```sql
# MAGIC CREATE TABLE sales_transactions_clustered (
# MAGIC     transaction_id STRING,
# MAGIC     order_date DATE,
# MAGIC     customer_id STRING,
# MAGIC     product_category STRING,
# MAGIC     region STRING,
# MAGIC     amount DECIMAL(10,2)
# MAGIC )
# MAGIC USING DELTA
# MAGIC CLUSTER BY (order_date, customer_id, product_category);
# MAGIC ```
# MAGIC
# MAGIC ### The Adaptive Advantage
# MAGIC What impressed me most was how Liquid Clustering adapted to our changing requirements:
# MAGIC - Month 1-2: Primary queries focused on order_date and customer_id
# MAGIC - Month 3-4: Business started requesting region-specific analysis
# MAGIC - Month 5-6: Product category became a critical filter
# MAGIC
# MAGIC With Z-Ordering, each shift would require:
# MAGIC - Analyzing new query patterns
# MAGIC - Deciding on new Z-Order columns
# MAGIC - Running expensive OPTIMIZE operations
# MAGIC - Testing performance  
# MAGIC
# MAGIC With Liquid Clustering:
# MAGIC - Simply ran ALTER TABLE CLUSTER BY (...new_columns...)
# MAGIC - New writes automatically optimized
# MAGIC - Background optimization handled existing data