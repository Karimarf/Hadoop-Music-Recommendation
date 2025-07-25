# 🎵 Hadoop Music Recommendation System

Ce projet déploie un pipeline d’analyse de données et de recommandation musicale à grande échelle en combinant **Apache Hadoop (HDFS)**, **Apache Spark** et **Docker**. Les données proviennent d’un dataset Spotify (fichier CSV) et sont traitées via PySpark, puis modélisées sur GPU avec RAPIDS (cuDF, cuML).

## 🚀 Prérequis

- **Docker** et **Docker Compose** installés sur votre machine
- Python 3.8+ (pour exécuter l’application Streamlit)

## 📦 Architecture

- **HDFS** : stockage distribué des fichiers (CSV, Parquet)
- **Spark** : traitement distribué (DataFrame, MLlib)
- **RAPIDS** (cuDF, cuML) : accélération GPU pour le clustering
- **Streamlit** : interface web de recommandations musicales

## 📁 Structure du projet

```text
├── data/                         # Données brutes
│   └── data.csv                  # Dataset Spotify initial
├── notebooks/                    # Notebooks PySpark & RAPIDS
│   ├── data_preparation.ipynb    # Nettoyage, vectorisation, PCA, export Parquet
│   └── model_training.ipynb      # Clustering GPU, choix de k, export CSV/Joblib
├── app.py                        # Application Streamlit
├── data_for_clustering.parquet   # Fichier Parquet pour entraînement GPU
├── spotify_clustered.csv         # Résultat du clustering K-Means
├── nn_model.joblib               # Modèle KNN des plus proches voisins
├── docker-compose.yml            # Déploiement Hadoop + Spark (x86)
├── docker-compose-arm.yml        # Déploiement Hadoop + Spark (ARM)
└── README.md                     # Documentation du projet
```

## 🚀 Démarrage de l’environnement Hadoop + Spark

1. Lancer les conteneurs :

   ```bash
   docker-compose up -d
   ```

2. Copier les données dans HDFS :

   ```bash
   docker cp data/data.csv hadoop-namenode-1:/tmp/
   docker exec -it hadoop-namenode-1 bash
   hdfs dfs -mkdir -p /data
   hdfs dfs -put /tmp/data/data.csv /data/
   ```

3. Accéder à Spark UI (http://localhost:8080) et Jupyter (http://localhost:8888, token dans les logs).

## 📝 Notebooks PySpark

### data_preparation.ipynb

1. Lecture du CSV depuis HDFS  
2. Nettoyage et conversion des colonnes  
3. Imputation des valeurs manquantes (moyenne)  
4. Assemblage des features et normalisation (StandardScaler)  
5. Réduction de dimension (PCA)  
6. Export Parquet (`data_for_clustering.parquet`)

### training.ipynb

1. Chargement du Parquet avec cuDF  
2. Recherche du nombre optimal de clusters (Elbow + Silhouette)  
3. Entraînement final de K-Means (k=9)  
4. Sérialisation du résultat (`spotify_clustered.csv`)  
5. Entraînement du modèle KNN (NearestNeighbors) et export Joblib (`nn_model.joblib`)

## 🎧 Application de recommandation (Streamlit)

1. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

2. Lancer l’app :

   ```bash
   streamlit run app.py
   ```

3. Sélectionner un titre et une méthode (KNN ou K-Means) pour obtenir des recommandations.

## 🔧 Personnalisation

- Ajuster le nombre de composantes PCA (`k`) dans `data_preparation.ipynb`
- Modifier `n_clusters` ou `n_init` dans `model_training.ipynb`
- Adapter la pondération par `popularity` dans `app.py`
