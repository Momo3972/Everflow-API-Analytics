# Everflow API Analytics

Un projet Python complet pour **analyser et visualiser les performances marketing** via l’**API Everflow**.  
Ce projet illustre la création d’un mini-pipeline analytique : de l’extraction des données à la visualisation graphique et au reporting automatique.

---

## Objectif du projet

L’objectif est de fournir un outil simple et automatisé permettant de :
1. **Se connecter à l’API Everflow** à l’aide d’une clé d’API sécurisée 
2. **Extraire des statistiques agrégées** (revenus, payouts, conversions, clics) sur une **plage de dates donnée**
3. **Calculer les profits** directement côté client (`profit = revenue − payout`)  
4. **Générer des graphiques** (profits par offre, affilié, annonceur)  
5. **Exporter les résultats** sous forme d’images PNG et d’un rapport Markdown réutilisable

---

## Structure du projet

```
Everflow-API-Analytics/
├── .env.example              # Modèle de configuration pour la clé API Everflow
├── .gitignore                # Fichiers à exclure de Git
├── mock_data/                # Données de test locales (mode mock)
│   └── sample_table_rows.json
├── out/                      # Résultats générés : graphiques + rapport
│   ├── profit_by_offer.png
│   ├── profit_by_affiliate.png
│   ├── profit_by_advertiser.png
│   └── REPORT.md
├── src/                      # Code source du projet
│   ├── everflow_client.py    # Connexion à l’API Everflow
│   ├── plotting.py           # Génération des graphiques
│   └── main.py               # Script CLI principal
├── Everflow-API-Analytics.ipynb  # Notebook Jupyter complet et commenté
├── REPORT.md                 # Modèle de rapport automatique
├── requirements.txt          # Dépendances Python
└── README.md                 # (ce fichier)
```

---

## Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/Momo3972/Everflow-API-Analytics.git
cd Everflow-API-Analytics
```

### 2️⃣ Créer un environnement virtuel
```bash
python -m venv .venv
.\.venv\Scriptsctivate     # (Windows)
# ou
source .venv/bin/activate    # (macOS/Linux)
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurer la clé API
Crée un fichier `.env` à la racine du projet (ou copie `.env.example`) :

```ini
EFLOW_API_KEY=ta_cle_api_everflow
EFLOW_BASE_URL=https://api.eflow.team
EFLOW_TIMEZONE_ID=67
EFLOW_CURRENCY_ID=USD
```

## Utilisation

### Mode mock (sans API, pour test)
```bash
python src/main.py --from 2025-03-15 --to 2025-03-31 --out out/ --mock
```

### Mode API réel
```bash
python src/main.py --from 2025-03-15 --to 2025-03-31 --out out/
```

### Options disponibles
| Option | Description |
|--------|-------------|
| `--from` | Date de début (format YYYY-MM-DD) |
| `--to` | Date de fin |
| `--out` | Dossier de sortie (par défaut : `out/`) |
| `--mock` | Active le mode test local |
| `--charts` | Limite la génération à certains graphiques (`offers`, `affiliates`, `advertisers`) |

---

## Exemple de résultats

Les fichiers suivants sont générés dans le dossier `out/` :

- `profit_by_offer.png`  
- `profit_by_affiliate.png`  
- `profit_by_advertiser.png`  
- `REPORT.md`

Aperçu du graphique principal :

![profit_by_offer](out/profit_by_offer.png)

---

## Fonctionnement technique

### Authentification
Chaque requête API Everflow utilise un en-tête :
```
X-Eflow-API-Key: <votre_cle_api>
```

### Endpoint utilisé
```http
POST /v1/networks/reporting/entity/table
```

### Exemple de payload
```json
{
  "from": "2025-03-15",
  "to": "2025-03-31",
  "timezone_id": 67,
  "currency_id": "USD",
  "columns": [{"column": "offer"}, {"column": "affiliate"}]
}
```

### Calculs et visualisations
- Calcul du profit : `profit = revenue - payout`
- Agrégation avec **pandas**
- Graphiques horizontaux via **matplotlib**
- Export automatique PNG + rapport Markdown

---

## Limites connues

1. **Fenêtre temporelle maximale : 1 an**  
   - Découper les périodes longues en plusieurs appels

2. **Résultats limités à 10 000 lignes**  
   - Si `incomplete_results = true`, réduire la plage ou ajouter des filtres

3. **Filtres manquants (à venir)**  
   - Ajout prévu : `country`, `device`, `source`, etc

4. **Visualisation statique uniquement**  
   - Amélioration possible : dashboard interactif avec **Streamlit** ou **Plotly Dash**

---

## Pistes d’amélioration

- Ajout de filtres dynamiques (pays, device, etc.)
- Tableau de bord web (Plotly / Streamlit)
- Génération automatique quotidienne (cron ou GitHub Actions)
- Exportation vers Google Sheets / Power BI / Tableau
- Cache local (SQLite ou Redis) pour améliorer les performances

---

## Technologies utilisées

| Domaine | Outils |
|----------|--------|
| Langage | Python 3.10+ |
| API | Everflow Reporting API |
| Librairies | `requests`, `pandas`, `matplotlib`, `python-dotenv` |
| Format de rapport | Markdown (.md) |
| IDE recommandé | Visual Studio Code / Jupyter Notebook |

---

## Auteur

**Mohamed Lamine OULD BOUYA**
Développeur Data & API Integration  
[GitHub Profile](https://github.com/Momo3972)  

---

## Licence

Ce projet est distribué sous licence **MIT**.  
Vous pouvez le réutiliser librement à des fins éducatives ou professionnelles.

---

> *Projet créé dans le cadre d’un portfolio pour démontrer ma capacité à intégrer une API REST analytique, à traiter des données en Python et à générer des visualisations exploitables.*
