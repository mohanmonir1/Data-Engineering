# Databricks notebook source
# MAGIC %md
# MAGIC ### What is Streaming?  
# MAGIC Streaming refers to the continuous processing of incoming data in real-time or near-real-time. Unlike batch processing, which works on a fixed dataset, streaming deals with infinite or unbounded data (e.g., logs, sensor data, or user clicks) that keeps arriving.
# MAGIC
# MAGIC ### Streaming before Spark
# MAGIC - Data flows through a graph of operators (nodes).
# MAGIC - Each node processes one record at a time and forwards the output.
# MAGIC
# MAGIC ### Spark Streaming
# MAGIC Instead of processing one record at a time, Spark groups the incoming data into small time intervals (e.g., every 1 second) and treats each as a mini batch job.
# MAGIC
# MAGIC **Key Concepts in DStreams:**
# MAGIC - Uses Spark's batch engine under the hood.
# MAGIC - Easy to implement and scale.
# MAGIC - Better fault tolerance (due to batch lineage).
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Batch vs Stream Processing
# MAGIC
# MAGIC ### Batch Processing
# MAGIC
# MAGIC *   Processes **large volumes of data together**.
# MAGIC *   Runs at **scheduled intervals** (hourly, daily, weekly, monthly).
# MAGIC *   Output is **delayed** → high latency.
# MAGIC *   Example:  
# MAGIC     Amazon collects orders during the day → sends to OLAP system in a **nightly batch job**.
# MAGIC
# MAGIC ### Stream Processing
# MAGIC
# MAGIC *   Processes **small chunks of data continuously**.
# MAGIC *   Real‑time or near real-time → **low latency**.
# MAGIC *   Continuous input + continuous output.
# MAGIC *   Examples:
# MAGIC     *   **Fraud detection** → card transaction checked instantly.
# MAGIC     *   **Medical monitoring** → real‑time machine data sent to doctors.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 2. How Spark Structured Streaming Works
# MAGIC
# MAGIC **Overall Flow**
# MAGIC
# MAGIC 1.  Streaming input arrives (Kafka, files, sockets, etc.)
# MAGIC 2.  Spark **breaks incoming data into micro-batches**.
# MAGIC 3.  Spark runs **the same DataFrame code** on each micro-batch.
# MAGIC 4.  Processed results are written to a sink (console, files, Kafka).
# MAGIC
# MAGIC ### Why Micro-batches?
# MAGIC
# MAGIC *   Spark's execution engine is optimized for **batch-like processing**.
# MAGIC *   Structured Streaming reuses the same **DataFrame API** and execution model.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 3. Unbounded Table (Unbounded DataFrame)
# MAGIC
# MAGIC *   Spark treats incoming streaming data as an **ever-growing table**.
# MAGIC *   New data = appended to the bottom of this table.
# MAGIC *   Your DataFrame transformations run **incrementally** on the new data.
# MAGIC *   This is why:
# MAGIC     > Batch code → can easily be reused for streaming.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 4. Example Explained: Word Count Streaming
# MAGIC
# MAGIC User types words in nc (netcat) terminal → Spark counts.
# MAGIC
# MAGIC #### At 1st second:
# MAGIC
# MAGIC     cat
# MAGIC     dog
# MAGIC     dog
# MAGIC     dog
# MAGIC
# MAGIC Output:
# MAGIC
# MAGIC     cat → 1
# MAGIC     dog → 3
# MAGIC
# MAGIC #### At 2nd second:
# MAGIC
# MAGIC     owl
# MAGIC     cat
# MAGIC
# MAGIC Appended → Spark recalculates.
# MAGIC
# MAGIC #### At 3rd second:
# MAGIC
# MAGIC     dog
# MAGIC     owl
# MAGIC
# MAGIC Appended → Spark recalculates again.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 5. The Four Core Concepts (WHAT, WHEN, HOW, WHERE)
# MAGIC
# MAGIC ### WHAT → Input Source
# MAGIC
# MAGIC *   What data are we ingesting?
# MAGIC *   Examples:
# MAGIC     *   Kafka topic
# MAGIC     *   New files in a folder
# MAGIC     *   nc socket input
# MAGIC
# MAGIC In the example → input comes from `ncat` terminal.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### WHEN → Trigger Interval
# MAGIC
# MAGIC *   How often Spark reads and processes new data.
# MAGIC *   In example → streaming processed **every second**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### HOW → Processing Logic
# MAGIC
# MAGIC *   DataFrame code + Output Mode.
# MAGIC
# MAGIC Output Modes:
# MAGIC
# MAGIC *   **Complete Mode:** entire result table printed every time.
# MAGIC *   **Append Mode:** only new rows printed.
# MAGIC *   **Update Mode:** only updated rows printed.
# MAGIC
# MAGIC Example used **Complete Mode**.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ### WHERE → Output Sink
# MAGIC
# MAGIC *   Where Spark writes the processed output.
# MAGIC *   Examples:
# MAGIC     *   Console
# MAGIC     *   File (CSV/Parquet/Delta)
# MAGIC     *   Kafka
# MAGIC     *   Memory table
# MAGIC
# MAGIC In example → output printed on terminal.
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC ## 6. Summary: 4-Step Streaming Design Pattern
# MAGIC
# MAGIC | Step      | Meaning                | Example                  |
# MAGIC | --------- | ---------------------- | ------------------------ |
# MAGIC | **WHAT**  | Input source           | nc terminal              |
# MAGIC | **WHEN**  | Trigger frequency      | every 1 second           |
# MAGIC | **HOW**   | Transformations + mode | complete mode word count |
# MAGIC | **WHERE** | Output sink            | console                  |
# MAGIC
# MAGIC This pattern applies to **every Spark streaming job** you will ever write.

# COMMAND ----------

# MAGIC %md
# MAGIC ![image_1773401085333.png](./image_1773401085333.png "image_1773401085333.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ![image_1773684625273.png](./image_1773684625273.png "image_1773684625273.png")
# MAGIC ![image_1773684712558.png](./image_1773684712558.png "image_1773684712558.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Stateless and Stateful Transformation
# MAGIC
# MAGIC - **Stateless Transformations:**  
# MAGIC   Each micro-batch is processed independently. Examples: `select`, `filter`, `map`, `withColumn`.
# MAGIC   - No information is retained between batches.
# MAGIC   - Suitable for simple operations like filtering or column manipulation.
# MAGIC
# MAGIC - **Stateful Transformations:**  
# MAGIC   Operations require information from previous batches. Examples: `groupBy`, `count`, `agg`, `dropDuplicates`, `window`.
# MAGIC   - Maintains state across micro-batches (e.g., running counts, aggregations).
# MAGIC   - Used for tasks like sessionization, running totals, or deduplication.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Flatten the JSON file

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME bi_dev.mo.stream

# COMMAND ----------

dbutils.fs.mkdirs("/Volumes/bi_dev/mo/stream/source_stream")

# COMMAND ----------

# Enable automatic schema inference for streaming files
spark.conf.set("spark.sql.streaming.schemaInference", True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Read Options
# MAGIC - **maxFilesPerTrigger**: Controls how many new files Spark consumes per micro-batch.
# MAGIC   ```py
# MAGIC   .option("maxFilesPerTrigger", num)
# MAGIC   ```
# MAGIC - **latestFirst**: Process newer files first instead of older ones.
# MAGIC   ```py
# MAGIC   .option("latestFirst", "true")
# MAGIC   ```
# MAGIC - **recursiveFileLookup**: Allows Spark to read files from all nested subfolders.
# MAGIC   ```py
# MAGIC   .option("recursiveFileLookup", "true")
# MAGIC   ```
# MAGIC - **cleanSource**: cleanSource is an option that tells Spark **what to do with the input files after Spark has processed them** in a streaming job.
# MAGIC
# MAGIC | Value         | Meaning                                   |
# MAGIC | ------------- | ----------------------------------------- |
# MAGIC | **"archive"** | Move processed files to another directory |
# MAGIC | **"delete"**  | Delete processed files permanently        |
# MAGIC | **sourceArchiveDir**        | Required if using archive mode         |
# MAGIC
# MAGIC ```py
# MAGIC .option("cleanSource", "archive")
# MAGIC .option("sourceArchiveDir", "/mnt/archive/processed/")
# MAGIC ```
# MAGIC -------------------------------------------------------------
# MAGIC ```py
# MAGIC .option("cleanSource", "delete")
# MAGIC ```

# COMMAND ----------

input_df = (
    spark.readStream.format("json")
    .option("multiline", True)
    .option("maxFilesPerTrigger", 1)
    .option("cleanSource", "archive")
    .option("sourceArchiveDir", "/Volumes/bi_dev/mo/stream/archive/devices")
    .load("/Volumes/bi_dev/mo/stream/source_stream")
)

# COMMAND ----------

from pyspark.sql import functions as F

sink_df = input_df.withColumn("devices", F.explode("data.devices")).select(
    "eventId", "customerId", "devices.*"
)

# COMMAND ----------

sink_df.writeStream.format("delta").outputMode("append").option(
    "path", "/Volumes/bi_dev/mo/stream/sink_stream/devices"
).option(
    "checkpointLocation",
    "/Volumes/bi_dev/mo/stream/sink_stream/checkpointdirectory/devices",
).trigger(
    once=True
).start()

# COMMAND ----------

df = spark.read.load("/Volumes/bi_dev/mo/stream/sink_stream/devices")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Checkpoint Directory
# MAGIC A checkpoint directory is a folder where Spark stores metadata so that a streaming query can:
# MAGIC - Recover from failures
# MAGIC - Avoid duplicate processing
# MAGIC - Track what data has already been processed
# MAGIC - Maintain state for aggregations, joins, and exactly-once guarantees
# MAGIC
# MAGIC ### Metadata file
# MAGIC *   A small JSON file created inside the checkpoint directory of a streaming query.
# MAGIC *   Stores the **identity** and **initial configuration** of the streaming job.
# MAGIC *   Acts like the *ID card* of the streaming pipeline.
# MAGIC
# MAGIC
# MAGIC #### What does the metadata file contain?
# MAGIC
# MAGIC It contains:
# MAGIC
# MAGIC 1.  **queryId**
# MAGIC     *   A unique ID for the streaming query.
# MAGIC     *   This ID stays the same across restarts.
# MAGIC 2.  **runId**
# MAGIC     *   A unique ID for each *run* of the query.
# MAGIC     *   Changes every time the stream restarts.
# MAGIC 3.  **version**
# MAGIC     *   Specifies the Spark checkpointing format version.
# MAGIC
# MAGIC Example content:
# MAGIC
# MAGIC ```json
# MAGIC {
# MAGIC   "queryId": "e3d57fb6-25b8-459d-9e7f-35ce7a77c833",
# MAGIC   "runId": "d729a8f3-7fac-492c-8e0d-01987c879790",
# MAGIC   "version": 2
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC #### Purpose of the metadata file
# MAGIC
# MAGIC *   Helps Spark recognize that a streaming query has been run before.
# MAGIC *   Ensures the streaming job resumes correctly after failures.
# MAGIC *   Prevents Spark from treating the checkpoint as a new stream.
# MAGIC *   Essential for **exactly-once processing**.
# MAGIC
# MAGIC
# MAGIC ### Offsets
# MAGIC
# MAGIC *   A subdirectory inside the checkpoint folder.
# MAGIC *   Stores the **input progress** of the streaming query.
# MAGIC *   Contains one **offset file per micro-batch**.
# MAGIC *   Helps Spark know *what data was already read* so it does NOT reprocess it.
# MAGIC
# MAGIC **Why does Spark store offsets?**
# MAGIC
# MAGIC Offsets ensure:
# MAGIC
# MAGIC - Exactly-once processing 
# MAGIC - Fault tolerance 
# MAGIC - Safe restarts
# MAGIC - No duplicate reads** even if the streaming job crashes
# MAGIC
# MAGIC Offsets = Spark's memory of how far it progressed in the input source.
# MAGIC
# MAGIC ### Sources
# MAGIC - The **sources** subdirectory in the checkpoint folder tracks the input sources for the streaming query.
# MAGIC - Stores information about which files, Kafka offsets, or other data sources have been processed.
# MAGIC - Helps Spark avoid re-reading the same input data after a restart.
# MAGIC
# MAGIC ### Commit
# MAGIC - The **commit** subdirectory records successful micro-batch executions.
# MAGIC - Each file marks a batch as "committed," ensuring Spark does not reprocess it.
# MAGIC - Guarantees exactly-once semantics by tracking which batches have been fully processed and written to the sink.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Output Modes
# MAGIC
# MAGIC Spark Structured Streaming supports three output modes for writing results:
# MAGIC
# MAGIC 1. **Append**  
# MAGIC    Only new rows added to the result table since the last trigger are written to the sink.  
# MAGIC    *Use when you only want to output new data.*
# MAGIC
# MAGIC 2. **Update**  
# MAGIC    Only rows that have changed since the last trigger are written to the sink.  
# MAGIC    *Use for aggregations or when you want to see updated results.*
# MAGIC
# MAGIC 3. **Complete**  
# MAGIC    The entire result table is written to the sink every time.  
# MAGIC    *Use for full table outputs, such as total counts or full aggregations.*

# COMMAND ----------

# MAGIC %md
# MAGIC ## Triggers
# MAGIC
# MAGIC Triggers control when Spark processes new data in streaming jobs:
# MAGIC
# MAGIC 1. **Default**  
# MAGIC    Processes data as soon as it arrives, with no specific interval.
# MAGIC
# MAGIC 2. **ProcessingTime**  
# MAGIC    Runs a micro-batch every fixed interval (e.g., every 1 minute).
# MAGIC
# MAGIC 3. **Once**  
# MAGIC    Processes all available data in a single batch, then stops.
# MAGIC
# MAGIC 4. **AvailableNow**  
# MAGIC    Processes all available data in multiple batches until the input is fully consumed, then stops.
# MAGIC
# MAGIC 5. **Continuous**  
# MAGIC    Processes data continuously with very low latency (experimental).

# COMMAND ----------

# MAGIC %md
# MAGIC ###