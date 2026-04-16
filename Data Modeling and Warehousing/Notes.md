<img width="1683" height="504" alt="image" src="https://github.com/user-attachments/assets/2dd131c4-ee25-4160-ac8a-55b4d51d8a00" />

### Difference between OLTP and OLAP

### Explain the following terms
1. **Data Redundancy**
2. **Data Inconsistency**:
3. **Data Integration**:
4. **Data Normalisation**:

### Keys:
1. **Primary Key**:
2. **Foreign Key**:
3. **Surrogate Key**:

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
