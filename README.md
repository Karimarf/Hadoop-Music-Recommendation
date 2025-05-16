
# 🎵 Music Analysis & Recommendation System with Spark + Hadoop

This project builds a distributed data analysis and recommendation pipeline using **Apache Spark**, **Hadoop HDFS**, and **PySpark notebooks**, based on a Spotify dataset.

---

## 📦 Stack

- Hadoop (HDFS)
- Apache Spark (Master + Worker)
- PySpark (Jupyter client)
- Docker / Docker Compose
- Dataset: [`data.csv`](./data.csv) from [Kaggle Spotify Dataset](https://www.kaggle.com/code/vatsalmavani/music-recommendation-system-using-spotify-dataset/input)

---

## 🚀 Getting Started

### 1. 🐳 Launch the cluster

Start your Hadoop + Spark + Jupyter cluster:

```bash
docker-compose up -d
```

---

### 2. 📁 Copy your dataset to HDFS

#### a. Copy `data.csv` from your local machine to the NameNode container:
```bash
docker cp data.csv hadoop-namenode-1:/tmp/data.csv
```

#### b. Open a shell in the NameNode:
```bash
docker exec -it hadoop-namenode-1 bash
```

#### c. Put the file into HDFS:
```bash
hdfs dfs -mkdir -p /data
hdfs dfs -put /tmp/data.csv /data/
```

---

## 📊 Data Analysis (Jupyter)

1. Access Jupyter Notebook:
   - 👉 http://localhost:8888

2. Open or create a notebook.
3. Use PySpark to:
   - Inspect the data (`df.printSchema()`, `df.show()`)
   - Explore audio features (`valence`, `danceability`, `energy`, etc.)
   - Analyze trends by `year`, `popularity`, `artists`, etc.
   - Prepare for clustering or recommendation models

---

## 🎧 Goal

> **Build a music recommendation system** based on audio features using Spark MLlib.

You’ll cluster similar songs (unsupervised learning) and recommend tracks based on the user’s listening profile.

---

## 🧪 Sample PySpark analysis

```python
df = spark.read.option("header", True).option("inferSchema", True).csv("hdfs://hadoop-namenode-1:8020/data/data.csv")
df.groupBy("year").count().orderBy("year").show()
```

---

## 📁 Project Structure

```text
.
├── data.csv                  # Spotify dataset
├── docker-compose.yml        # Hadoop + Spark cluster  
├── docker-compose-arm.yml    # For Mac and Linux
├── notebooks/                # Your PySpark notebooks
└── README.md
```

