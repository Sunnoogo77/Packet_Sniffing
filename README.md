# 🕵️‍♂️ Packet Sniffing Backend - Mini-Projet

🚀 **Détection et analyse des paquets réseau en temps réel avec Scapy & Supabase**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg) ![Scapy](https://img.shields.io/badge/Scapy-Network%20Analysis-green.svg) ![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-brightgreen.svg)  

---

## 📌 **1. Présentation du projet**

Ce projet permet de **capturer, analyser et stocker** les paquets réseau en temps réel.  
Les informations capturées sont ensuite **stockées dans une base Supabase (PostgreSQL)** pour analyse ultérieure.

✅ **Fonctionnalités** :
- 📡 Capture des paquets réseau en **temps réel** avec **Scapy**.
- 🖥️ Identification des **appareils connectés** (`known_devices`).
- 🌐 Détection des **sites visités** (`visited_sites`).
- 🗄️ Stockage des données dans **Supabase (PostgreSQL)**.
- 🔍 Visualisation et requêtage des données via **une API REST (optionnelle)**.

---

## ⚙️ **2. Installation & Configuration**

### 🛠 **Prérequis**
✔ **Python 3.8+**  
✔ **Pip**  
✔ **Docker** *(si conteneurisation activée)*  
✔ **Compte Supabase** *(gratuit, utilisé comme base de données cloud)*  
✔ **Base de données PostgreSQL** créée sur Supabase  

---

### 🏗 **2.1 Configuration de Supabase**
Ce projet **utilise une base de données PostgreSQL via Supabase**.  
Si vous souhaitez reproduire ce projet, **vous devez créer un compte Supabase** et configurer une base de données.

📌 **Étapes pour créer et configurer Supabase :**  

1️⃣ **Créer un compte Supabase** sur [https://supabase.com](https://supabase.com)  
2️⃣ **Créer un nouveau projet** et noter l'URL du projet (ex: `https://xyzxyz.supabase.co`).  
3️⃣ **Aller dans l'onglet "Database"** et récupérer la clé API (`SUPABASE_KEY`).  
4️⃣ **Créer les tables nécessaires** dans Supabase en exécutant ces commandes SQL :

```sql
CREATE TABLE realtime_traffic (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    src_ip TEXT,
    dst_ip TEXT,
    src_mac TEXT,
    dst_mac TEXT,
    protocol TEXT,
    src_port INT,
    dst_port INT,
    site_visited TEXT,
    data_size INT
);

CREATE TABLE known_devices (
    id SERIAL PRIMARY KEY,
    mac_address TEXT UNIQUE,
    ip_address TEXT,
    hostname TEXT
);

CREATE TABLE visited_sites (
    id SERIAL PRIMARY KEY,
    src_ip TEXT,
    domain TEXT,
    visit_time TIMESTAMP DEFAULT NOW()
);
```

5️⃣ **Créer un fichier `.env` et y mettre les informations suivantes :**  
```ini
SUPABASE_URL=https://xyzxyz.supabase.co
SUPABASE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠ **Sans cette configuration, le projet ne pourra pas stocker les données !**

---

### 📥 **2.2 Installation du projet**

1️⃣ **Cloner le repository**
```bash
git clone https://github.com/ton-utilisateur/packet-sniffing.git
cd packet-sniffing
```

2️⃣ **Créer un environnement virtuel & installer les dépendances**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## 🚀 **3. Lancer le projet**

### 📡 **Démarrer la capture des paquets**
```bash
python src/capture/capture.py
```

### 🔍 **Résultats attendus**
- **Affichage des paquets capturés en temps réel**
- **Stockage des données dans Supabase**
- **Appareils détectés et sites visités enregistrés**

---

## 🏗 **4. Architecture du projet**

```
packet_sniffing_backend/
│── src/
│   ├── capture/               # 📡 Capture et analyse réseau
│   │   ├── capture.py         # 🚀 Capture avec Scapy uniquement
│   ├── storage/               # 🗄️ Gestion de la base de données
│   │   ├── db.py              # 🔗 Connexion à PostgreSQL (Supabase)
│   │   ├── models.py          # 🏛️ Schéma des tables SQL
│   │   ├── insert_data.py     # 📩 Insertion des données Scapy dans la DB
│   ├── api/                   # 🌐 API REST (Préparation pour le futur)
│   │   ├── app.py             # 🚀 Serveur Flask/FastAPI
│   │   ├── routes.py          # 📌 Routes API (GET, POST)
│   ├── utils/                 # 🛠️ Fonctions utilitaires
│   │   ├── helpers.py         # 🤖 Fonctions diverses (détection OS, etc.)
│   ├── config.py              # ⚙️ Variables de config (DB_URL, etc.)
│── tests/                     # 🧪 Dossier des tests unitaires
│── logs/                      # 📝 Logs des captures réseau
│── requirements.txt           # 📜 Liste des dépendances
│── .env                       # 🔐 Variables d’environnement
│── README.md                  # 📖 Documentation du projet
```

---

## 🐳 **5. Conteneurisation avec Docker**

### 📦 **1️⃣ Construire l’image Docker**
```bash
docker build -t packet-sniffing .
```

### 🚀 **2️⃣ Lancer le conteneur**
```bash
docker run --rm -it --network host --env-file .env packet-sniffing
```

---

✨ **Merci d'avoir testé ce projet !**  
🚀 **Happy Sniffing!** 🕵️‍♂️📡  
