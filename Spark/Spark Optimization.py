# Databricks notebook source
# MAGIC %md
# MAGIC # Table of Contents
# MAGIC 1. **Query Execution Plan**
# MAGIC     1. **Narrow Transformation**: (filter, withColumn, select)
# MAGIC     2. **Wide Transformation**: (repartition, coalesce, join, groupBy (count, sum, DistinctCount))
# MAGIC     3. **Why predicate pushdown doesn't work in some scenarios?**
# MAGIC 2. **Directed Acyclic Graph (DAG)**
# MAGIC     1. **File Read**
# MAGIC     2. **show()**
# MAGIC     3. **Narrow Transformation**: (filter, withColumn, select)
# MAGIC     4. **Wide Transformation**: (join (sort merge join, broadcast join), groupBy (count, sum, DistinctCount))
# MAGIC 3. **Memory Management**
# MAGIC     1. **Executor Memory Management**
# MAGIC     2. **Unified Memory**
# MAGIC     3. **Off Heap Memory**
# MAGIC 4. **Shuffle Partition**
# MAGIC 5. **Data Skew**
# MAGIC     1. **Difference b/w Partition skew and Data Skew**
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

sc.defaultParallelism
spark.conf.get("spark.sql.files.maxPartitionBytes")
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.shuffle.partitions", 4)
spark.conf.set("spark.sql.adaptive.enabled", False)
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Repartition VS Coalesce
# MAGIC - **Adopting best partition strategy**: Designing the best partition strategy ensures optimal performance in Spark applications. 
# MAGIC - **Right number of partitions**: Partitions should be created based on the number of cores to boost performance. If not, performance suffers.
# MAGIC - **Even distribution of partitions**: Evenly distributed partitions improve performance, while uneven distribution negatively impacts performance. 
# MAGIC - **Example scenario**: If only one partition of size 500 MB is created on a worker node with 16 cores, the partition cannot be shared among cores. Result: One core processes 500 MB, while 15 cores remain idle.
# MAGIC
# MAGIC | **Aspect**           | **Repartition**                                             | **Coalesce**                                                          |
# MAGIC | -------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------- |
# MAGIC | **Purpose**          | Can **increase or decrease** number of partitions.          | Used to **decrease** number of partitions only.                       |
# MAGIC | **Shuffle Behavior** | Always performs a **full shuffle** of data.                 | **Avoids full shuffle**; combines partitions or shuffles minimally.   |
# MAGIC | **Performance**      | **Slower** than Coalesce due to full shuffle.               | **Better performance** than Repartition because shuffle is minimized. |
# MAGIC | **Partition Size**   | Creates **almost equal-sized partitions**.                  | Output partitions can be **uneven in size**.                          |
# MAGIC | **Use Case**         | Good when you need **balanced partitions** for parallelism. | Good when reducing partitions without major reshuffling.              |
# MAGIC | **Impact on Data**   | Builds new partitions from scratch.                         | Merges existing partitions, avoiding unnecessary data movement.       |
# MAGIC
# MAGIC ## Default Partitions for RDD/DataFrame
# MAGIC **sc.defaultParallelism**
# MAGIC - Determines the number of partitions when creating data within Spark.
# MAGIC - Default value: Number of cores.
# MAGIC
# MAGIC **spark.sql.files.maxPartitionBytes**
# MAGIC - Controls partition size when reading data from external systems.Default value: 128 MB.
# MAGIC - Applies to file-based sources like Parquet, JSON, ORC.
# MAGIC - Display: spark.conf.get(spark.sql.files.maxPartitionBytes)
# MAGIC - This is applicable only while reading the data from external files. Once the data is loaded then we can partition where partiton can have more than 128MB size
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

sc.defaultParallelism

# COMMAND ----------

spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating Data within the Spark Application

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType
df = spark.createDataFrame(range(10), IntegerType())
df.rdd.getNumPartitions()
df.rdd.glom().collect()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading Data from External Files

# COMMAND ----------

dbutils.fs.ls('abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust')

# COMMAND ----------

spark.conf.set("spark.sql.files.maxPartitionBytes", 35000)
spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
)
df.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Repartition

# COMMAND ----------


df1 = df.repartition(8)
df1.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Coalesce

# COMMAND ----------

df2 = df.coalesce(3)
df2.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query Execution Plan (QEP)
# MAGIC ![SparkQueryExecutionPlan](/Workspace/Users/mo@fastenal.com/Spark/SparkQueryExecution.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Narrow Transformation QEP

# COMMAND ----------

from pyspark.sql import functions as F

df = (
    spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/emp"
    )
)

# COMMAND ----------

from pyspark.sql import functions as F

df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
    )
)

df1 = (
    df.filter(F.col("id") > 10)
    .withColumn("first_name", F.split(F.col("name"), " ")[0])
    .select("id", "first_name")
)

df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Wide Transformation QEP

# COMMAND ----------

# MAGIC %md
# MAGIC #### Repartition

# COMMAND ----------

df = spark.read.format("parquet").option("inferSchema", "true").load("abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust")
df.rdd.getNumPartitions()
df1 = df.repartition(8)
df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Coalesce

# COMMAND ----------

df = spark.read.format("parquet").option("inferSchema", "true").load("abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust")
df.rdd.getNumPartitions()
df1 = df.coalesce(3)
df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Join

# COMMAND ----------

# MAGIC %md
# MAGIC Without disabling broadcast join

# COMMAND ----------

cust_df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
    )
)
transaction_df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)

joined_df = transaction_df.alias("t").join(
    cust_df.alias("cust"), F.col("t.cust_id") == F.col("cust.id"), "inner"
).select(
    "t.transaction_id",
    "t.cust_id",
    "cust.name",
    "t.product_id",
    "t.amount"
    )
joined_df.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC With disabling braodcast join

# COMMAND ----------

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)

# COMMAND ----------

# MAGIC %md
# MAGIC **Hash Partitioning**  
# MAGIC - Hash partitioning is a data distribution strategy used by Spark during shuffle operations (like joins, aggregations, etc.). 
# MAGIC - It ensures that rows with the same join key end up in the same partition across all nodes.
# MAGIC - Spark must ensure that rows with the same key from both tables are co-located in the same partition so they can be joined without excessive network communication.
# MAGIC
# MAGIC **How it works:**
# MAGIC - Spark computes a hash function on the join key:  
# MAGIC _partition_id = hash(key) % numPartitions_
# MAGIC - Each row is assigned to a partition based on this hash.
# MAGIC - Both sides of the join (left and right DataFrames) are shuffled so that matching keys go to the same partition.
# MAGIC
# MAGIC **Key points:**
# MAGIC - Exchange hashpartitioning(key#12, 200) means Spark is shuffling data using hash partitioning on key into 200 partitions (default).
# MAGIC - This happens before the actual join to ensure data locality.
# MAGIC - Control number of partitions via spark.sql.shuffle.partitions (default = 200).

# COMMAND ----------

cust_df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
    )
)
transaction_df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)

joined_df = transaction_df.alias("t").join(
    cust_df.alias("cust"), F.col("t.cust_id") == F.col("cust.id"), "inner"
).select(
    "t.transaction_id",
    "t.cust_id",
    "cust.name",
    "t.product_id",
    "t.amount"
    )
joined_df.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy - Count

# COMMAND ----------

df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
    )
)
df1 = df.groupBy("id").count()
df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy - sum

# COMMAND ----------

from pyspark.sql import functions as F
df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)
df1 = df.groupBy("transaction_id").agg(F.sum("amount").alias("total_amount"))
df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy - DistinctCount

# COMMAND ----------

df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)
df1 = df.groupBy("cust_id").agg(F.countDistinct("product_id").alias("distinct_inv"))
df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **Predicate Pushdown and Complex Types**
# MAGIC
# MAGIC **Why It Fails**
# MAGIC
# MAGIC *   Spark cannot push down filters on **complex types** (arrays, maps, structs) to Parquet because:
# MAGIC     *   Parquet stores these as nested structures.
# MAGIC     *   The Parquet reader cannot evaluate conditions like `map.getItem("eye") == "brown"` at the file level.
# MAGIC *   Result: Spark reads **all data** and applies the filter **after loading into memory**, which is inefficient.
# MAGIC
# MAGIC **Example**
# MAGIC
# MAGIC ```python
# MAGIC # Schema: properties is a map<string, string>
# MAGIC df.filter(df.properties.getItem("eye") == "brown").show()
# MAGIC ```
# MAGIC
# MAGIC **Physical Plan Output:**
# MAGIC
# MAGIC     *(1) Filter (metadata#123[key] = value)
# MAGIC     +- *(1) ColumnarToRow
# MAGIC        +- FileScan parquet ...
# MAGIC
# MAGIC *   Filter is **not pushed down**; happens after `ColumnarToRow`.

# COMMAND ----------

# MAGIC %md
# MAGIC **Why Casting in Filter Prevents Pushdown**
# MAGIC
# MAGIC *   **Predicate pushdown** works when Spark can translate the filter into a condition that the Parquet reader understands.
# MAGIC *   When you **cast a column inside the filter**, Spark cannot guarantee that the cast operation is compatible with Parquet’s native filtering.
# MAGIC *   As a result:
# MAGIC     *   Spark applies the filter **after reading the data** (post-scan).
# MAGIC     *   The physical plan will show `ColumnarToRow` before the filter, meaning **no pushdown**.
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F
df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)
df1 = df.filter(F.col("amount").cast("int") > F.lit(10)).select("transaction_id")
df1.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark's DAG

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading File
# MAGIC - For reading the data, spark creates a job.
# MAGIC - Read can be considered as an action because while reading it just read the metadata not the actual data - This can be confirmed by the input size of the stage

# COMMAND ----------

df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### show
# MAGIC - 2 Jobs are created.
# MAGIC     - Job1: First job is created for reading the data
# MAGIC     - Job2: Second is created for the action show

# COMMAND ----------

df = (
    spark.read.format("parquet")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
    )
)
df.show(15, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Narrow Transformation

# COMMAND ----------

df.rdd.getNumPartitions()

# COMMAND ----------

from pyspark.sql import functions as F

df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
    )
)

df1 = (
    df.filter(F.col("id") > 10)
    .withColumn("first_name", F.split(F.col("name"), " ")[0])
    .withColumn("second_name", F.split(F.col("name"), " ")[1])
    .select("id", "first_name", "second_name")
)

df1.write.format("noop").mode("overwrite").save("mohan")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Wide Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC #### Sort Merge Join

# COMMAND ----------

cust_df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
)
transaction_df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
)

# COMMAND ----------

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")

# COMMAND ----------

joined_df = transaction_df.alias("t").join(
    cust_df.alias("c"), F.col("t.cust_id") == F.col("c.id"), "inner"
)

joined_df.explain(True)

# COMMAND ----------

joined_df.write.format("noop").mode("overwrite").save("mohan")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Broadcast Join
# MAGIC
# MAGIC The smaller dataframe size should be less than autoBroadcastJoinThreshold

# COMMAND ----------

cust_df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/cust"
)
transaction_df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
)

# COMMAND ----------

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10 * 1024 * 1024)

# COMMAND ----------

from pyspark.sql import functions as F

joined_df = transaction_df.alias("t").join(
    F.broadcast(cust_df).alias("c"), F.col("t.cust_id") == F.col("c.id"), "inner"
)

joined_df.explain(True)

# COMMAND ----------

joined_df.write.format("noop").mode("overwrite").save("mohan")

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy - count

# COMMAND ----------

grouped_df = transaction_df.groupBy("cust_id").agg(
    F.count("product_id").alias("product")
)
grouped_df.write.format("noop").mode("overwrite").save("mohan")

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC #### GroupBy - countDistinct

# COMMAND ----------

grouped_df = transaction_df.groupBy("cust_id").agg(
    F.countDistinct("product_id").alias("product")
)
grouped_df.explain(True)
grouped_df.write.format("noop").mode("overwrite").save("mohan")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Memory Management
# MAGIC
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/memory_management.png)
# MAGIC
# MAGIC Spark memory management is a critical concept for understanding how Spark allocates and uses memory within executors to perform distributed computations efficiently.
# MAGIC
# MAGIC **Note**:
# MAGIC 1. When we request a memory, not all memory will be allocated to executor. Only 89% of memory will be allocated remaining 10% will be used for executor inhouse process like GC vcalled Overhead memory. Out of 90%, 300MB will be reserved momory
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 1. Spark Executor Container
# MAGIC
# MAGIC Each Spark executor runs inside a container with a fixed amount of memory allocated by `spark.executor.memory` plus overhead. Memory inside the executor is divided into several regions:
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 2. On-Heap Memory
# MAGIC
# MAGIC *   Controlled by **`spark.executor.memory`**.
# MAGIC *   This is JVM heap memory where most Spark operations occur.
# MAGIC *   It is further divided into:
# MAGIC     *   **Execution Memory**  
# MAGIC         Used for runtime operations like:
# MAGIC         *   Joins
# MAGIC         *   Shuffles
# MAGIC         *   Sorting
# MAGIC         *   Aggregations (`groupBy`)
# MAGIC     *   **Storage Memory**  
# MAGIC         Used for:
# MAGIC         *   Caching RDDs/DataFrames
# MAGIC         *   Broadcast variables
# MAGIC         *   Serialized data blocks
# MAGIC     *   **User Memory**  
# MAGIC         For user-defined data structures, variables, and objects.
# MAGIC     *   **Reserved Memory**  
# MAGIC         A fixed 300 MB reserved for Spark’s internal operations to prevent OutOfMemory errors.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 3. Off-Heap Memory
# MAGIC
# MAGIC *   Controlled by **`spark.memory.offHeap.enabled`** and **`spark.memory.offHeap.size`**.
# MAGIC *   Used when off-heap storage is enabled for Tungsten (Spark’s optimized execution engine).
# MAGIC *   Helps reduce GC overhead by storing data outside JVM heap.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 4. Memory Overhead
# MAGIC
# MAGIC *   Controlled by **`spark.executor.memoryOverhead`**.
# MAGIC *   Default: **max(384 MB, 10% of `spark.executor.memory`)**.
# MAGIC *   Used for:
# MAGIC     *   JVM overhead
# MAGIC     *   Native libraries
# MAGIC     *   Python processes (in PySpark)
# MAGIC     *   Shuffle buffers
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### 5. Unified Memory Management
# MAGIC
# MAGIC Spark uses a **unified memory model** where **Execution Memory** and **Storage Memory** share space dynamically:
# MAGIC
# MAGIC *   If caching needs more space, it can borrow from execution memory and vice versa.
# MAGIC *   This flexibility improves resource utilization.
# MAGIC 1. Storage memory can borrow space from execution memory only if Execution memory is free.
# MAGIC 2. Execution memory can borrow space from Storage memory if its empty and has not reached its storageFraction limit (immune to eviction).
# MAGIC 3. Execution memory is used by Storage memory and Execution needs more memory, it can forcefully evict the memory occupied by Storage Memory at Execution side.
# MAGIC 4. Storage needs more memory, it cannot forcefully evict the excess blocks occupied by Execution Memory. It has to wait for Execution.
# MAGIC 5. The executor memory should be atleast 1.5 times of reserved memory
# MAGIC
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/unified_memory.png)
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### Key Configurations
# MAGIC
# MAGIC *   `spark.executor.memory`: Main heap memory for executor.
# MAGIC *   `spark.executor.memoryOverhead`: Extra memory for non-heap usage.
# MAGIC *   `spark.memory.fraction`: Fraction of heap for unified memory (default 0.6).
# MAGIC *   `spark.memory.storageFraction`: Fraction of unified memory reserved for storage (default 0.5).
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### Best Practices
# MAGIC
# MAGIC *   Increase `spark.executor.memory` for large joins or caching.
# MAGIC *   Tune `spark.executor.memoryOverhead` for PySpark or heavy shuffles.
# MAGIC *   Enable off-heap memory for large datasets to reduce GC pressure.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark Executor Tuning
# MAGIC
# MAGIC - Choosing right number of cores and size of memory matters
# MAGIC - While spark submit we need to specify number of executor, cores in each executor and size of memory
# MAGIC
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/executor_tuning.png)
# MAGIC
# MAGIC ### Fat Executor
# MAGIC
# MAGIC #### Advantages
# MAGIC
# MAGIC **Increased Parallelism**  
# MAGIC With more cores, fat executors can run more tasks in parallel, improving application performance. It is good for cases where:
# MAGIC
# MAGIC *   Tasks require significant amount of data to be loaded in memory
# MAGIC *   Managing many executors is a concern
# MAGIC
# MAGIC **Enhanced Data Locality**  
# MAGIC With fewer, large executors, the chances of data being processed on the node where it is stored increases, enhancing data locality. This reduces network traffic, improving overall application speed.
# MAGIC
# MAGIC **HDFS Throughput**  
# MAGIC Improves the rate at which data can be read from or written to HDFS.
# MAGIC
# MAGIC #### Disadvantages
# MAGIC
# MAGIC **Under Utilisation**  
# MAGIC Can lead to inefficient use of resources if all cores or memory are not utilised.
# MAGIC
# MAGIC **Fault Tolerance**  
# MAGIC Failure of a single executor has a bigger impact because each executor is handling a large portion of data. Recovering from such failures can be costly in terms of time and computation, reducing overall application reliability.
# MAGIC
# MAGIC **HDFS Throughput Issue**  
# MAGIC HDFS throughput might suffer (if you’re using HDFS) because of the high number of cores per executor. HDFS throughput refers to the rate at which data can be read from or written to HDFS. Recommendation is to have 3–5 cores per executor.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### Thin Executor
# MAGIC
# MAGIC #### Advantages
# MAGIC
# MAGIC **Increased Parallelism**  
# MAGIC Increases parallelism as there are more executors handling smaller tasks. This is beneficial when tasks are lightweight.
# MAGIC
# MAGIC **Fault Tolerance**  
# MAGIC One executor going down amounts to losing a small unit of work done, which is easier to recover.
# MAGIC
# MAGIC
# MAGIC #### Disadvantages
# MAGIC
# MAGIC **High Network Traffic**  
# MAGIC Thin executors may increase network traffic because each executor has a small memory and therefore, data has to be distributed across more executors for processing.
# MAGIC
# MAGIC **Reduced Data Locality**  
# MAGIC Having thin executors spread across multiple nodes can reduce the effectiveness of data locality.
# MAGIC
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/et1.png)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Shuffle Partitions
# MAGIC - Shuffling happens whenever there is wide transformation involved. For example, Join, GroupBy.
# MAGIC - The idea behind shuffling is to bring the data together that are related which is reside across different node.
# MAGIC - Optimal shuffle partition size is 1-200 MB.
# MAGIC
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/shuffle_partition.png)
# MAGIC
# MAGIC **Shuffle Files**  
# MAGIC - Are serialized in Tungsten Binary Format (Unsafe Row). These files can directly be read in memory thus improving read performance.
# MAGIC - Tungsten binary format is Spark’s compact, CPU‑ and cache‑friendly in‑memory/on‑disk row layout introduced as part of the Tungsten project (with whole‑stage codegen).

# COMMAND ----------

spark.conf.get("spark.sql.shuffle.partitions")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Skew
# MAGIC - Data unevenly partitioned
# MAGIC - Few partitions have lot of data than others
# MAGIC - Data skew can be checked at:
# MAGIC     - Job Run
# MAGIC     - Event timeline
# MAGIC     - Summary metrics
# MAGIC
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/Skew.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Partition Skew vs. Data Skew in Spark
# MAGIC
# MAGIC **1. Data Skew (Root Cause)**
# MAGIC
# MAGIC **Definition:**  
# MAGIC Data skew happens when **certain keys occur far more frequently** than others in your dataset.
# MAGIC
# MAGIC **Example:**
# MAGIC
# MAGIC Suppose you have a column `country` and 90% of your records are `"India"`.
# MAGIC
# MAGIC     India: 9,000,000 rows
# MAGIC     USA:      300,000 rows
# MAGIC     UK:        50,000 rows
# MAGIC     Others:    20,000 rows
# MAGIC
# MAGIC **Why it's a problem:**
# MAGIC
# MAGIC Operations such as:
# MAGIC
# MAGIC *   `groupBy`
# MAGIC *   `reduceByKey`
# MAGIC *   `join`
# MAGIC *   `distinct`
# MAGIC
# MAGIC cause all values of the **same key** to end up on the **same executor task**, creating huge imbalance.
# MAGIC
# MAGIC **2. Partition Skew (Symptom/Effect)**
# MAGIC
# MAGIC **Definition:**  
# MAGIC Partition skew happens when **some partitions contain many more records than others**, causing long-running tasks.
# MAGIC
# MAGIC **How it happens:**
# MAGIC
# MAGIC Usually as a *direct result of data skew*.  
# MAGIC For example, after a shuffle (join/groupBy), Spark partitions data by key:
# MAGIC
# MAGIC *   Partition 0 → 9 million rows (all “India”)
# MAGIC *   Partition 1 → 200k rows
# MAGIC *   Partition 2 → 20k rows
# MAGIC
# MAGIC The task handling partition 0 becomes a **straggler**.
# MAGIC
# MAGIC **Why it matters:**
# MAGIC
# MAGIC *   Some tasks finish fast, but one or two tasks run for minutes/hours.
# MAGIC *   Cluster resources stay idle waiting for slow tasks.
# MAGIC *   Jobs take much longer.

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.range(1000000000).repartition(1)
df1 = spark.range(20).repartition(1)
df2 = spark.range(30).repartition(1)
final_df = df.union(df1).union(df2)

# COMMAND ----------

# MAGIC %md
# MAGIC Skewed data

# COMMAND ----------

skewed_df = final_df.groupBy(F.spark_partition_id()).agg(F.count("id").alias("count"))
skewed_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Evenly distributed data

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.range(1000000000).repartition(1)
df1 = spark.range(20).repartition(1)
df2 = spark.range(30).repartition(1)
final_df = df.union(df1).union(df2).repartition(3)

# COMMAND ----------

skewed_df = final_df.groupBy(F.spark_partition_id()).agg(F.count("id").alias("count"))
skewed_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Consider the time of only GroupBy operation. Evenly distributed data takes less time than the skewed data

# COMMAND ----------

# MAGIC %md
# MAGIC ## Partitioning
# MAGIC
# MAGIC ### Problems Solved by Partitioning:
# MAGIC
# MAGIC 1.  **Fast / Easy Access**
# MAGIC     *   Partitioning organizes data into smaller, manageable chunks based on a partition key.
# MAGIC     *   This allows Spark to **read only the relevant partitions** instead of scanning the entire dataset, reducing I/O and improving query performance.
# MAGIC     *   Example: If you query data for `P3`, Spark only reads the partition containing `P3` instead of all partitions.
# MAGIC
# MAGIC 2.  **Parallelism / Resource Utilization**
# MAGIC     *   Partitioning enables Spark to **distribute data across multiple executors and cores**.
# MAGIC     *   Each partition can be processed independently, allowing **parallel execution**.
# MAGIC     *   This maximizes cluster resource utilization and reduces job execution time.
# MAGIC     *   In the diagram:
# MAGIC         *   There are multiple compute nodes (C1, C2, C3).
# MAGIC         *   Without proper partitioning, some nodes may be overloaded while others remain idle (shown with X marks).
# MAGIC         *   With partitioning, tasks are evenly distributed across nodes, improving efficiency.
# MAGIC
# MAGIC ### Key Factors for Choosing Partition Column:
# MAGIC
# MAGIC 1.  **Cardinality of the Column**
# MAGIC     *   **High Cardinality** (many unique values):
# MAGIC         *   Example: `Customer → Customer-ID`
# MAGIC         *   Pros:
# MAGIC             *   Creates many partitions, which can improve parallelism.
# MAGIC         *   Cons:
# MAGIC             *   Too many small partitions can lead to overhead and inefficient execution.
# MAGIC     *   **Low Cardinality** (few unique values):
# MAGIC         *   Example: `State`
# MAGIC         *   Pros:
# MAGIC             *   Fewer partitions, easier to manage.
# MAGIC         *   Cons:
# MAGIC             *   Risk of **data skew** (some partitions may have much more data than others), reducing parallelism.
# MAGIC     *   **Medium Cardinality**:
# MAGIC         *   Often ideal because it balances partition count and data distribution.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC 2.  **Filter Usage**
# MAGIC     *   Choose columns that are **frequently used in filters** or **WHERE clauses**.
# MAGIC     *   This ensures **partition pruning**, meaning Spark reads only relevant partitions instead of scanning the entire dataset.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC #### Best Practices:
# MAGIC
# MAGIC *   Avoid partitioning on columns with **extremely high cardinality** (e.g., unique IDs for billions of rows) unless you have a large cluster.
# MAGIC *   Avoid columns with **very low cardinality** (e.g., gender, yes/no) because they create very few partitions and cause skew.
# MAGIC *   Prefer columns that:
# MAGIC     *   Have **medium cardinality**.
# MAGIC     *   Are **commonly used in queries for filtering**.
# MAGIC     *   Distribute data evenly across partitions.

# COMMAND ----------

from pyspark.sql import functions as F
listen_df = spark.read.format("csv").option('inferSchema', 'true').option('header', 'true').load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/spotify"
)

# COMMAND ----------

activity_df = (
    listen_df.withColumnRenamed("listen_date", "listen_time")
    .withColumn("listen_date", F.to_date(F.col("listen_time")))
    .withColumn("listen_hour", F.hour(F.col("listen_time")))
)
#activity_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **Single Level Partitioning**

# COMMAND ----------

activity_df.write.format("parquet").partitionBy("listen_date").mode("overwrite").save(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/single_level_partition"
)

# COMMAND ----------

# MAGIC %md
# MAGIC **Multi-level Partitioning**
# MAGIC
# MAGIC The ordering of partition is importanat.

# COMMAND ----------

activity_df.write.format("parquet").partitionBy("listen_date", "listen_hour").mode("overwrite").save(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/multi_level_partition"
)

# COMMAND ----------

activity_df.write.format("parquet").partitionBy("listen_hour", "listen_date").mode("overwrite").save(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/multi_level_partition2"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### repartiton / coalesce with partitionBy

# COMMAND ----------

# TO create multiple partition inside partiotioned directory
activity_df.repartition(3).write.format("parquet").partitionBy("listen_date").mode(
    "overwrite"
).save(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/repartiton"
)

# COMMAND ----------

# coalesce will avoid shuffling and avoid increasing partition. It does create only one partition
activity_df.coalesce(3).write.format("parquet").partitionBy("listen_date").mode(
    "overwrite"
).save(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/coalesce"
)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Partition Practice
# MAGIC

# COMMAND ----------

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.adaptive.enabled", False)
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", False)

sales = (
    spark.read.format("csv")
    .option("header", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/sales"
    )
)

# COMMAND ----------

sales.rdd.getNumPartitions()

# COMMAND ----------

from pyspark.sql import functions as F

sales.withColumn("transaction_month", F.month("transacted_at")).repartition(
    "transaction_month"
).write.format("parquet").partitionBy("transaction_month").mode("overwrite").save(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/sales_repa_month"
)

# COMMAND ----------

sales_partition = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/sales_repa_month"
)

# COMMAND ----------

sales_partition.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bucketing
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/Bucketing.png)
# MAGIC This is the one of the technique to divide that data into more managable chunks based on hash value.
# MAGIC
# MAGIC | **Scenario**                  | **DS1 Bucketing**               | **DS2 Bucketing**                         | **Join Column** | **Performance**               |
# MAGIC | ----------------------------- | ------------------------------- | ----------------------------------------- | --------------- | ----------------------------- |
# MAGIC | **1. Ideal Case**             | Buckets = **B**, Column = **X** | Buckets = **B**, Column = **X**           | Same            | ✅ **No Shuffle**              |
# MAGIC | **2. Different Bucket Count** | Buckets = **B**, Column = **X** | Buckets = **Y**, Column = **X**           | Same            | **OK** (One dataset shuffled) |
# MAGIC | **3. Different Join Column**  | Buckets = **B**, Column = **X** | Buckets = **B**, Column = **product\_id** | Different       | ❌ **Full Shuffle**            |
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ✅ **Key Insight**:
# MAGIC
# MAGIC *   Bucketing works best when **both datasets have the same join column and same bucket count**.
# MAGIC *   If bucket counts differ → partial shuffle.
# MAGIC *   If join columns differ → full shuffle (bucketing gives no benefit).
# MAGIC
# MAGIC ### How to Choose Optimize Bucketing Number?
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/BucketingNumber.png)
# MAGIC

# COMMAND ----------

product_df = (
    spark.read.format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/products"
    )
)

order_df = (
    spark.read.format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/orders"
    )
)

# COMMAND ----------

spark.conf.set('spark.sql.autoBroadcastJoinThreshold', -1)

# COMMAND ----------

joined_df = product_df.join(order_df, product_df.product_id == order_df.product_id, "inner")
joined_df.explain()

# COMMAND ----------

# MAGIC %md
# MAGIC bucketBy() requires Spark to manage metadata about buckets, which is only possible when creating a table in a metastore (Hive or Spark catalog).

# COMMAND ----------

product_df.write.bucketBy(4, "product_id").mode("overwrite").format(
    "parquet"
).saveAsTable("product_bucket")

# COMMAND ----------

order_df.write.bucketBy(4, "product_id").mode("overwrite").format(
    "parquet"
).saveAsTable("order_bucket")

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS product_bucket")

# COMMAND ----------

product_df = spark.table("product_bucket")
order_df = spark.table("order_bucket")

# COMMAND ----------

joined_df = product_df.join(order_df, product_df.product_id == order_df.product_id, "inner")
joined_df.explain()

# COMMAND ----------

from pyspark.sql import functions as F
grouped_df = (
    order_df.groupBy("product_id")
    .agg(F.sum("total_amount").alias("amount"))
    .select("product_id", "amount")
)

grouped_df.explain()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Bucket Pruning
# MAGIC
# MAGIC Only required buckets will be selected instead of selecting entire buckets - SelectedBucketsCount: 1 out of 4
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F
grouped_df = (
    order_df.filter(F.col("product_id") == 1)
    .groupBy("product_id")
    .agg(F.sum("total_amount").alias("amount"))
    .select("product_id", "amount")
)

grouped_df.explain()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cache, Persit and Storage Level

# COMMAND ----------

df_customers = spark.read.parquet(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/customers"
)

# COMMAND ----------

df_customers.show(5, False)

# COMMAND ----------

from pyspark.sql import functions as F
df_base = (
    df_customers
    .filter(F.col("city") == "boston")
    .withColumn(
        "customer_group", 
        F.when(
            F.col("age").between(20, 30), 
            F.lit("young") 
        )
        .when(
            F.col("age").between(31, 50), 
            F.lit("mid") 
        )
        .when(
            F.col("age") > 51, 
            F.lit("old") 
        )
        .otherwise(F.lit("kid"))
     )
    .select("cust_id", "name", "age", "gender", "birthday", "zip", "city", "customer_group")
)

# COMMAND ----------

df1 = (
    df_base
    .withColumn("test_column_1", F.lit("test_column_1"))
    .withColumn("birth_year", F.split("birthday", "/").getItem(2))
)

df1.explain(True)
#df1.show(5, False)

# COMMAND ----------

df2 = (
    df_base
    .withColumn("test_column_2", F.lit("test_column_2"))
    .withColumn("birth_month", F.split("birthday", "/").getItem(1))
)

df2.explain(True)
df2.show(5, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### cache

# COMMAND ----------

from pyspark.sql import functions as F
df_base = (
    df_customers
    .filter(F.col("city") == "boston")
    .withColumn(
        "customer_group", 
        F.when(
            F.col("age").between(20, 30), 
            F.lit("young") 
        )
        .when(
            F.col("age").between(31, 50), 
            F.lit("mid") 
        )
        .when(
            F.col("age") > 51, 
            F.lit("old") 
        )
        .otherwise(F.lit("kid"))
     )
    .select("cust_id", "name", "age", "gender", "birthday", "zip", "city", "customer_group")
)

df_base.cache() 
df_base.show(5, False)

# COMMAND ----------

df1 = (
    df_base
    .withColumn("test_column_1", F.lit("test_column_1"))
    .withColumn("birth_year", F.split("birthday", "/").getItem(2))
)

df1.explain(True)
df1.show(5, False)

# COMMAND ----------

df2 = (
    df_base
    .withColumn("test_column_2", F.lit("test_column_2"))
    .withColumn("birth_month", F.split("birthday", "/").getItem(1))
)

df2.explain(True)
df2.show(5, False)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### `StorageLevel` Types:
# MAGIC
# MAGIC (As of Spark `3.4`)
# MAGIC
# MAGIC - `DISK_ONLY`: CPU efficient, memory efficient, slow to access, data is serialized when stored on disk
# MAGIC - `DISK_ONLY_2`: disk only, replicated 2x
# MAGIC - `DISK_ONLY_3`: disk only, replicated 3x
# MAGIC
# MAGIC - `MEMORY_AND_DISK`: spills to disk if there's no space in memory
# MAGIC - `MEMORY_AND_DISK_2`: memory and disk, replicated 2x
# MAGIC - `MEMORY_AND_DISK_DESER`(default): same as `MEMORY_AND_DISK`, deserialized in both for fast access
# MAGIC - `MEMORY_ONLY`: CPU efficient, memory intensive
# MAGIC - `MEMORY_ONLY_2`: memory only, replicated 2x - for resilience, if one executor fails
# MAGIC
# MAGIC **Note**:
# MAGIC - `SER` is CPU intensive, memory saving as data is compact while `DESER` is CPU efficient, memory intensive
# MAGIC - Size of data on disk is lesser as data is in serialized format, while deserialized in memory as JVM objects for faster access
# MAGIC
# MAGIC ### When to use what?
# MAGIC
# MAGIC | Storage Level        | Space used | CPU time | In memory | On-disk | Serialized |
# MAGIC |----------------------|------------|----------|-----------|---------|------------|
# MAGIC | MEMORY_ONLY          | High       | Low      | Y         | N       | N          |
# MAGIC | MEMORY_ONLY_SER      | Low        | High     | Y         | N       | Y          |
# MAGIC | MEMORY_AND_DISK      | High       | Medium   | Some      | Some    | Some       |
# MAGIC | MEMORY_AND_DISK_SER  | Low        | High     | Some      | Some    | Y          |
# MAGIC | DISK_ONLY            | Low        | High     | N         | Y       | Y          |

# COMMAND ----------

df_base.unpersist()
df_base.persist(StorageLevel.MEMORY_ONLY)

df2 = (
    df_base
    .withColumn("test_column_1", F.lit("test_column_1"))
    .withColumn("birth_year", F.split("birthday", "/").getItem(2))
)

df1.show(5, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Salting
# MAGIC Adding randomness to distribute uneven data evenly

# COMMAND ----------

from pyspark.sql import functions as F
# partions have equal size of data
uniform_df = spark.range(10000000)

# COMMAND ----------

uniform_df.withColumn("partition_id", F.spark_partition_id()).groupBy("partition_id").agg(
    F.count("id").alias("id")
).show()

# COMMAND ----------

df = spark.createDataFrame([(0, )] * 1000000, ["id"]).repartition(1)
df1 = spark.createDataFrame([(1,)] * 20, ["id"]).repartition(1)
df2 = spark.createDataFrame([(2,)] * 10, ["id"]).repartition(1)

skewed_df = df.union(df1).union(df2)

# COMMAND ----------

skewed_df.withColumn("partition_id", F.spark_partition_id()).groupBy(
    "partition_id"
).agg(F.count("id").alias("id")).show()

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions",3)

# COMMAND ----------

# MAGIC %md
# MAGIC Skewed join

# COMMAND ----------

skewed_join = skewed_df.join(uniform_df, "id", "inner")
skewed_join.withColumn("partition_id", F.spark_partition_id()).groupBy(
    "partition_id"
).agg(F.count("id").alias("id")).show()

# COMMAND ----------

SALT_NUMBER = int(spark.conf.get("spark.sql.shuffle.partitions"))
print(SALT_NUMBER)

# COMMAND ----------

skewed_df = skewed_df.withColumn("salt", (F.rand() * SALT_NUMBER).cast("int"))

# COMMAND ----------

skewed_df.show(10, False)

# COMMAND ----------

uniform_df = uniform_df.withColumn(
    "salt_value", F.lit([i for i in range(SALT_NUMBER)])
).withColumn("salt", F.explode(F.col("salt_value")))

# COMMAND ----------

# MAGIC %md
# MAGIC Evenly distributed join

# COMMAND ----------

spark.conf.set("spark.sql.autoBroadcastJoinThreshold",-1)

# COMMAND ----------

uniform_join = skewed_df.join(uniform_df, ["id", "salt"], "inner")
uniform_join.withColumn("partition_id", F.spark_partition_id()).groupBy(
    "partition_id", "id"
).agg(F.count("id").alias("id")).show()

# COMMAND ----------

uniform_join.explain()

# COMMAND ----------

df = spark.createDataFrame([(0, )] * 1000000, ["id"]).repartition(1)
df1 = spark.createDataFrame([(1,)] * 20, ["id"]).repartition(1)
df2 = spark.createDataFrame([(2,)] * 10, ["id"]).repartition(1)

skewed_df = df.union(df1).union(df2)

# COMMAND ----------

from pyspark.sql import functions as F
spark.conf.set("spark.sql.shuffle.partitions", 4)

# COMMAND ----------

salt_number = spark.conf.get("spark.sql.shuffle.partitions")
print(salt_number)

# COMMAND ----------

skewed_df = skewed_df.withColumn("salt_number", (F.rand() * salt_number).cast("int"))
skewed_df.show(10, False)

# COMMAND ----------

skewed_df.groupBy("id", "salt_number").agg(F.count("id").alias("cnt")).groupBy(
    "id"
).agg(F.sum("cnt").alias("cnt")).display()

# COMMAND ----------

skewed_df.groupBy("id").count().display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## AQE and Broadcast Join
# MAGIC Techniques to solve data skew

# COMMAND ----------

# MAGIC %md
# MAGIC ### Adaptive Query Execution Plan (AQE)
# MAGIC AQE, a feature introduced in Spark 3.0, uses runtime statistics to select the most efficient query plan, optimizing shuffle partitions, joins, and skewed joins.
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/AQE.png)
# MAGIC

# COMMAND ----------

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("saprk.sql.adaptive.skewJoin.enabled", "false")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "false")

# COMMAND ----------

# This is a target size for shuffle partitions after Spark has seen real runtime statistics (i.e., with AQE on).
#  (default is usually 64MB in Spark 3.x).
# This is not the strict rule.
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "8MB")

#Controls skew detection during skew join optimization in AQE. (default is usually 256MB)
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "10MB")

# COMMAND ----------

from pyspark.sql import functions as F
cust_df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/customer_skew"
    )
)
transaction_df = (
    spark.read.format("parquet")
    .option("inferSchema", "true")
    .load(
        "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction"
    )
)

# joined_df = transaction_df.alias("t").join(
#     cust_df.alias("cust"), F.col("t.cust_id") == F.col("cust.cust_id"), "inner"
# ).select(
#     "t.transaction_id",
#     "t.cust_id",
#     "cust.name",
#     "t.product_id",
#     "t.amount"
#     )
# joined_df.display()

# COMMAND ----------

transaction_df.groupBy("cust_id").count().display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Distributed Variable
# MAGIC These variables allow information to be shared across executors in a distributed cluster, but each serves a very different purpose.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Broadcast Variables
# MAGIC Broadcast variables let you send a read‑only value to all executors in an efficient way.
# MAGIC They are used when you want workers to have a local copy of some reference data without shipping it repeatedly with tasks.
# MAGIC
# MAGIC **How they work**  
# MAGIC 1. Spark distributes the variable once to each executor.
# MAGIC 2. Workers then cache the variable locally.
# MAGIC 3. It avoids sending large objects over the network with every task → improves performance.

# COMMAND ----------

from pyspark.sql import functions as F

emp_data = [
    (1, "John", 10, 50000),
    (2, "Alice", 20, 60000),
    (3, "Bob", 10, 55000),
    (4, "David", 30, 70000),
    (5, "Emma", 40, 65000),
]

emp_columns = ["emp_id", "name", "dept_id", "salary"]

employee_df = spark.createDataFrame(emp_data, emp_columns)

dept_var = {10: "Sales", 20: "HR", 30: "IT", 40: "Finance"}

department_broadcast_var = spark.sparkContext.broadcast(dept_var)
print(type(department_broadcast_var), department_broadcast_var.value.get(10))

# COMMAND ----------

def department_lookup(dept_id):
    return department_broadcast_var.value.get(dept_id)


from pyspark.sql.types import StringType
department_lookup_udf = F.udf(department_lookup, StringType())


employee_df.withColumn("dept_name", department_lookup_udf(F.col("dept_id"))).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Accumulators
# MAGIC Accumulators are variables used for aggregating information across tasks.
# MAGIC They support only additions (or an associative operation), which makes them safe in a distributed environment.
# MAGIC
# MAGIC **How they work**
# MAGIC 1. Executers update the accumulator
# MAGIC 2. Only the driver can read the final value
# MAGIC 3. Used mostly for monitoring or debugging (e.g., counters)

# COMMAND ----------

acc = spark.sparkContext.accumulator(0)

def salary_sum(salary):
    acc.add(salary)

employee_df.foreach(lambda rows: salary_sum(rows.salary))

# COMMAND ----------

print(acc.value)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Joins

# COMMAND ----------

# MAGIC %md
# MAGIC ### Shuffle Hash Join
# MAGIC Shuffle Hash Join is a Spark join strategy used when both datasets are too large to broadcast, but one side is significantly smaller than the other. Here's how it works:
# MAGIC
# MAGIC **How Shuffle Hash Join Works**  
# MAGIC **Two-Phase Process:**
# MAGIC
# MAGIC 1. **Shuffle Phase** - Both datasets are shuffled (redistributed) across the cluster based on the join key's hash value. Records with the same join key end up on the same partition/executor.
# MAGIC
# MAGIC 2. **Hash Phase** - The smaller dataset on each partition is loaded into a hash table in memory. Spark then iterates through the larger dataset, probing the hash table for matching keys.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Dynamic Partition Pruning

# COMMAND ----------

# MAGIC %md
# MAGIC ### Static Partition Pruning
# MAGIC ![](/Workspace/Users/mo@fastenal.com/Spark/static_partition_pruning.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Out of Memory in Spark
# MAGIC **What is OOM in Spark?**  
# MAGIC OOM (Out of Memory) in Spark occurs when a process (executor or driver) tries to use more memory than is allocated to it, causing the process to fail.
# MAGIC
# MAGIC **Why do we get driver OOM?**
# MAGIC Driver OOM happens when the Spark driver process exceeds its allocated memory. This can occur if:
# MAGIC - The driver collects or aggregates too much data (e.g., using `.collect()`, `.toPandas()`, or large broadcast variables).
# MAGIC - Large job plans or metadata are kept in memory.
# MAGIC - Too many tasks or stages are scheduled at once.
# MAGIC
# MAGIC **What is driver overhead memory?**
# MAGIC Driver overhead memory is extra memory reserved for non-JVM needs of the driver, such as:
# MAGIC - Python processes (in PySpark)
# MAGIC - Native libraries
# MAGIC - Network buffers
# MAGIC - Serialization/deserialization
# MAGIC It is configured with `spark.driver.memoryOverhead`.
# MAGIC
# MAGIC **Common reason to get a driver OOM?**
# MAGIC - Collecting large datasets to the driver (`.collect()`, `.toPandas()`)
# MAGIC - Large broadcast variables
# MAGIC - Large job DAGs or metadata
# MAGIC - Insufficient driver memory or overhead settings
# MAGIC
# MAGIC **How to handle OOM?** 
# MAGIC - Avoid collecting large datasets to the driver; use distributed operations.
# MAGIC - Increase driver memory and overhead (`spark.driver.memory`, `spark.driver.memoryOverhead`).
# MAGIC - Optimize code to reduce memory usage (filter early, avoid large UDFs).
# MAGIC - Use caching judiciously and unpersist unused data.
# MAGIC
# MAGIC **Why do we get OOM when data can be spilled to the disk?**
# MAGIC   - Spilling works only when Spark can safely break data into chunks and write part of it to disk without affecting correctness.
# MAGIC   - If one key’s data (example: key = 1) is so large that the entire key group is bigger than the available memory, it cannot be spilled, because Spark must keep the entire key group together for joins and aggregations.  
# MAGIC   **Example**
# MAGIC     - Suppose executor has 2.9 GB execution memory.
# MAGIC     - Key “1” alone needs 3+ GB to perform a join or aggregation.
# MAGIC     - Spark must load all rows with key “1” together → cannot spill half of them.
# MAGIC     - Since it cannot split this key‑group → Spark throws OOM.
# MAGIC
# MAGIC **How Spark manages storage inside executor internally?**
# MAGIC   - Memory management
# MAGIC
# MAGIC **How task is splitted in executor?**
# MAGIC
# MAGIC Suppose executor has 4 cores.
# MAGIC   - It can run 4 tasks in parallel.
# MAGIC   - If fewer tasks arrive (e.g., 2), then only 2 run.
# MAGIC   - Each task takes its own chunk of execution memory.
# MAGIC
# MAGIC And:
# MAGIC   - More cores = more parallel tasks = more memory pressure.
# MAGIC   - Using >5 cores per executor commonly leads to memory overhead OOM, because more tasks → more objects → more overhead.
# MAGIC   - Recommended cores per executor: 3-5.
# MAGIC
# MAGIC **Why do we need overhead memory?**
# MAGIC
# MAGIC Overhead memory is extra memory allocated on top of the executor's JVM heap. It is required because not all memory usage in Spark happens inside the JVM. Some operations, especially in PySpark or when using native libraries, require memory outside the JVM heap.
# MAGIC
# MAGIC - **Executor container memory = executor-memory + overhead.**
# MAGIC   ```
# MAGIC   spark.executor.memory = 10GB
# MAGIC   spark.executor.memoryOverhead = 10% = 1GB
# MAGIC   Total container = 11GB
# MAGIC   ```
# MAGIC   
# MAGIC - **What is included in overhead memory?**
# MAGIC   - **Non-JVM processes:**  
# MAGIC     - Python worker processes in PySpark (each task may launch a separate Python process)
# MAGIC     - Native libraries (e.g., BLAS, Arrow, Pandas UDFs)
# MAGIC     - OS-level processes and system calls
# MAGIC     - Serialization/deserialization buffers
# MAGIC     - Network communication buffers
# MAGIC     - Off-heap memory allocations (e.g., Tungsten, shuffle, broadcast)
# MAGIC - **Why is it important?**
# MAGIC   - If overhead memory is too low, the container can run out of memory even if the JVM heap is not full, causing the executor to be killed by YARN/Kubernetes.
# MAGIC   - Overhead memory ensures stability for workloads that use native code, large shuffles, or PySpark UDFs.
# MAGIC   - Spark defaults to 10% of executor memory or at least 384MB, but you may need to increase it for heavy PySpark or native workloads.
# MAGIC
# MAGIC **Summary:**  
# MAGIC Overhead memory is a safety buffer for all memory used outside the JVM heap, preventing OOM errors from non-JVM processes and ensuring Spark executors run reliably.
# MAGIC
# MAGIC **When do we get executor OOM?**
# MAGIC 1. **JVM execution memory exceeds limit:**  
# MAGIC    Execution memory (hash joins, groupBy, sort) exceeds its limit → OOM.
# MAGIC
# MAGIC 2. **Overhead memory exceeds limit:**  
# MAGIC    If container uses more than `executor-memory-overhead` → container kills executor.
# MAGIC
# MAGIC 3. **User memory full:**  
# MAGIC    Large UDF or RDD operations consume user memory.
# MAGIC
# MAGIC 4. **Storage memory full (cache):**  
# MAGIC    Storage memory occupies too much, execution memory cannot get space even after eviction.
# MAGIC
# MAGIC 5. **Join keys too large (spill‑unsafe data):**  
# MAGIC    When a single key group > execution memory  
# MAGIC    - cannot spill  
# MAGIC    - OOM
# MAGIC
# MAGIC 6. **Total container size exceeded:**  
# MAGIC    If executor uses > (memory + overhead)  
# MAGIC    - container OOM  
# MAGIC    - executor dies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Practice

# COMMAND ----------

transaction_df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/transaction_skew"
)

customer_df = spark.read.format("parquet").load(
    "abfss://curated@datasvcdevadls.dfs.core.windows.net/business_intelligence/mo/customer_skew"
)

# COMMAND ----------

from pyspark.sql import functions as F

joined_df = transaction_df.alias("t").join(
    customer_df.alias("c"), F.col("t.cust_id") == F.col("c.cust_id"), "inner"
)
joined_df.display()