# Rapport de Projet : CIB Billing & Interest Reporting Simulator
**Candidat :** Jean-Yves KOUTSENE Développeur Business Reporting
**Destinataire :** Nicolas BOUCARD Chef de Projet chez BNP Paribas CIB

---

# I. Résumé Exécutif & Provenance des Données

## 1.1. Présentation Stratégique
Le projet **"CIB Billing & Interest Reporting Simulator"** est un prototype industriel simulant les fonctions critiques de facturation et de rémunération des liquidités pour une clientèle Corporate. Dans le cadre de l'alternance chez **BNP Paribas CIB**, ce projet démontre une capacité à orchestrer une chaîne de valeur complète : de l'ingestion de données massives à la restitution décisionnelle.

## 1.2. Origine et Nature des Données (Data Lineage)
La qualité d'un système de reporting dépend de la fiabilité de sa source. Pour ce projet, nous avons utilisé un dataset de référence :
*   **Source :** Dataset "PaySim" (disponible sur **Kaggle**).
*   **Volume Brut :** ~6,3 millions de transactions financières (470 Mo).
*   **Nature initiale :** Données synthétiques simulant des transactions mobiles pour la détection de fraude.
*   **Transformation :** Nous avons extrait un échantillon représentatif de 127 000 transactions réparties sur un cycle mensuel complet (31 jours) pour simuler la réalité d'un portefeuille CIB.

## 1.3. Nettoyage & Valorisation (The Cleaning Process)
Pour transformer cette "matière brute" en "intelligence bancaire", nous avons mis en place une stratégie d'ingénierie :
1.  **Échantillonnage Temporel :** Extraction d'un cycle mensuel via Python (Pandas).
2.  **Mapping Métier :** Re-catégorisation des flux originaux vers des services bancaires CIB.
3.  **Nettoyage & Typage :** Optimisation de la mémoire et création d'une timeline réaliste.

---

# II. Cadrage Fonctionnel & Métier (The Business Context)

## 2.1. L'univers des Sight Deposits (Comptes à Vue)
Dans une banque de financement comme BNP Paribas CIB, les entreprises (Corporate) déposent leurs liquidités sur des comptes à vue. Ces dépôts massifs sont un enjeu stratégique :
*   **Pour le Client :** Fructifier ses excédents tout en gardant l'argent disponible.
*   **Pour la Banque :** Constituer une ressource de financement, rémunérée par des intérêts créditeurs.
**Notre règle :** Application de taux par paliers (Tiered Rates) basés sur les soldes quotidiens (Base ACT/360).

## 2.2. Le Billing Corporate : La monétisation des services
Le "Billing" est le moteur de revenus du Cash Management. Chaque service opérationnel (virement, retrait, gestion) est facturé selon une grille tarifaire précise.
**Notre modèle :** Combinaison de commissions fixes (Virements), de frais forfaitaires (Gestion) et de commissions ad valorem (Retraits).

## 2.3. L'enjeu de la Marge Nette de Flux
Le pilotage de la rentabilité client repose sur l'équilibre :
`Marge Nette = Revenus du Billing - Coût des Intérêts versés`

---

# III. Architecture Technique & Choix Technologiques

## 3.1. Python (Pandas) : Le moteur ETL & Data Quality
Python a été choisi pour sa flexibilité dans la manipulation de gros volumes. 
*   **Pourquoi ?** Pour sa capacité à lire des fichiers de 500 Mo en "chunks" (morceaux), évitant ainsi de saturer la mémoire RAM.
*   **Usage :** C'est ici que sont gérés l'échantillonnage temporel et les scripts de validation (Data Quality).

## 3.2. DuckDB : La puissance du SQL Analytique
Plutôt qu'une base de données lourde, j'ai opté pour **DuckDB**.
*   **Pourquoi ?** C'est un moteur SQL "in-process" ultra-rapide sur les fichiers CSV. Il permet d'exécuter des requêtes analytiques complexes (Window Functions, CTE) avec une performance digne d'un Data Warehouse.
*   **Usage :** Calcul des intérêts quotidiens et agrégation de la facturation mensuelle.

## 3.3. Power BI : La restitution décisionnelle
Power BI assure la couche finale de Business Intelligence.
*   **Pourquoi ?** Pour sa capacité à modéliser des mesures DAX complexes et à offrir une interactivité indispensable aux managers pour explorer la donnée (drill-down).
*   **Usage :** Dashboard multi-pages (Vue Executive, Performance Clients, Audit).

---

# IV. Le Moteur de Traitement : Ingénierie des Données

Ce chapitre détaille comment nous avons transformé une base de données brute de 470 Mo en un système de reporting financier précis.

## 4.1. L'ETL en Python : Le "Crible" Temporel
Le premier défi était la masse : 6,3 millions de lignes. Pour ne pas "étouffer" l'ordinateur, nous avons utilisé une technique de **Lecture par Morceaux (Chunking)**.

**Le concept simple :** Imaginez que vous deviez lire un livre de 10 000 pages. Au lieu de le porter d'un coup, vous lisez 10 pages, vous notez les points importants, et vous passez aux 10 suivantes.

**Le Mapping Temporel :** Le dataset original utilisait des `steps` (Heure 1, Heure 2...). Nous avons codé une fonction qui transforme chaque heure en une véritable date du calendrier 2026.
```python
# Extrait du script 01 : Transformation du temps
start_date = datetime(2026, 1, 1)
df['transaction_timestamp'] = df['step'].apply(lambda x: start_date + timedelta(hours=x))
df['transaction_date'] = df['transaction_timestamp'].dt.date
```

## 4.2. Le Moteur de Calcul SQL : La "Calculatrice" Financière
Une fois les données triées, nous avons utilisé le langage SQL pour appliquer les règles bancaires. Nous avons utilisé des **CTE (Common Table Expressions)**, qui permettent de découper un calcul complexe en étapes logiques très claires.

**La Règle des Paliers (Intérêts) :**
C'est comme l'impôt sur le revenu, mais à l'envers. Plus le client laisse d'argent, plus le taux est élevé.
```sql
-- Extrait du script 02 : Calcul des intérêts sur base 360
CASE 
    WHEN oldbalanceOrg > 500000 THEN (oldbalanceOrg * 0.03) / 360
    ELSE (oldbalanceOrg * 0.015) / 360
END AS interest_earned_daily
```

**La Logique de Facturation (Billing) :**
Chaque type d'opération a son prix. Nous avons simulé une grille tarifaire où un virement international coûte plus cher qu'un service standard.
```sql
CASE 
    WHEN billing_category = 'Virement_International' THEN 15.0
    WHEN billing_category = 'Retrait_Fonds' THEN amount * 0.0005
    ELSE 2.0 -- Service Standard
END AS billing_fee
```

## 4.3. Stockage et Performance
Grâce à **DuckDB**, le calcul de ces millions de lignes prend moins de **2 secondes**. Le résultat est exporté dans un fichier "Lightweight" (`cib_final_results.csv`) qui est ensuite lu instantanément par Power BI.

---

# V. Certification de la Donnée (Quality Gate)

Dans un environnement CIB, la donnée n'est pas seulement de l'information, c'est de l'argent. Une erreur de calcul peut entraîner des pertes financières massives ou des sanctions réglementaires. C'est pourquoi j'ai intégré une "Barrière de Qualité" automatisée.

## 5.1. La philosophie du "Zero Defect"
Inspiré par les méthodes de travail de l'équipe technique de BNP à Mumbai/Chennai, le pipeline ne s'arrête pas au calcul. Avant toute mise à jour du dashboard Power BI, le script `03_data_quality_tests.py` vérifie l'intégrité de l'output. Si un seul test échoue, le reporting est bloqué pour investigation.

## 5.2. Les trois piliers du contrôle (TNR)
Le script exécute des **Tests de Non-Régression (TNR)** pour garantir que les évolutions du code n'ont pas cassé la logique financière.

1.  **Test d'Intégrité de Signe :**
    *   *Objectif :* Vérifier qu'aucun intérêt versé ou frais de billing n'est négatif.
    *   *Logique :* En banque de flux standard, un intérêt créditeur ne peut pas devenir un débit sans une action spécifique.
2.  **Test de Précision Mathématique (Unit Test) :**
    *   *Objectif :* Valider la formule de calcul au centime près.
    *   *Logique :* Le script prend un client témoin avec un solde > 1M€ et recalcule manuellement l'intérêt attendu (Base 360). S'il y a un écart supérieur à 0,01€, l'alerte est lancée.
3.  **Test de Cohérence Relationnelle :**
    *   *Objectif :* S'assurer qu'aucune transaction n'est "orpheline".
    *   *Logique :* 100% des lignes de résultats doivent être rattachées à un ID client valide existant dans le référentiel.

## 5.3. Le Statut "Audit-Ready"
À la fin de l'exécution, le système délivre un certificat : **"STATUT : DONNÉES CERTIFIÉES POUR POWER BI"**.
Cette approche garantit au manager que les chiffres qu'il voit à l'écran ont été doublement vérifiés par une intelligence logicielle indépendante du moteur de calcul.

---

# VI. Business Intelligence : Visualisation & Insights

La phase finale du projet consiste à transformer la donnée certifiée en un outil de décision visuel. Le dashboard Power BI a été conçu pour offrir une navigation intuitive, allant de la vision globale au détail granulaire.

## 6.1. La puissance du DAX (Data Analysis Expressions)
Pour enrichir l'analyse, j'ai développé une suite de mesures DAX personnalisées. Ces formules permettent de passer d'une simple lecture comptable à une véritable analyse de performance financière.

| Mesure DAX | Formule | Signification Métier |
| :--- | :--- | :--- |
| **Total Billing (€)** | `SUM(total_billing)` | Chiffre d'affaires brut généré par les services de cash management. |
| **Interest Expense (€)** | `SUM(total_interests)` | Coût de la liquidité (montant versé aux clients Corporate). |
| **Net Margin (€)** | `[Total Billing] - [Interest Expense]` | Profitabilité réelle de la banque sur la relation client. |
| **Average Yield (%)** | `DIVIDE([Int. Exp.], SUM(avg_balance)) * 360` | Rendement annuel moyen servi sur les dépôts (Indicateur de coût). |
| **Active Clients** | `DISTINCTCOUNT(client_id)` | Taille du portefeuille client actif sur la période. |

## 6.2. Architecture du Dashboard & Guide Visuel
Le rapport est structuré pour répondre aux questions du manager de manière progressive. Voici où insérer vos captures d'écran pour un impact maximum :

### 📸 INSERTION IMAGE 1 : "Vue Executive"
*(Fichier : docs/Images/Vue Executive.png)*
*   **Titre :** *Figure 1 : Cockpit de Pilotage Stratégique*
*   **Description :** Ce visuel présente les KPIs consolidés. Il permet de valider d'un coup d'œil que la **Marge Nette** reste positive malgré la rémunération des dépôts.

### 📸 INSERTION IMAGE 2 : "Analyse Temporelle"
*(Fichier : docs/Images/Analyse Temporelle.png)*
*   **Titre :** *Figure 2 : Évolution des Flux et Pression des Intérêts*
*   **Description :** Ce graphique en aires superpose les revenus (Billing) et les coûts (Intérêts). On y observe la stabilité quotidienne des flux et la corrélation entre l'activité transactionnelle et la rémunération.

### 📸 INSERTION IMAGE 3 : "Analyse Clients"
*(Fichier : docs/Images/Analyse Clients.png)*
*   **Titre :** *Figure 3 : Segmentation et Profitabilité Individuelle*
*   **Description :** Ce visuel permet de "descendre" au niveau de chaque client. Le Relationship Manager peut identifier les clients dont le solde est sous-optimisé ou ceux qui génèrent le plus de frais de virement.

### 📸 INSERTION IMAGE 4 : "Matrice de Détails"
*(Fichier : docs/Images/Matrice de Détails.png)*
*   **Titre :** *Figure 4 : Transparence et Auditabilité des Calculs*
*   **Description :** C'est la vue "Back-office". Elle permet de réconcilier chaque centime. En entretien, elle prouve que vous maîtrisez la donnée jusqu'à la ligne de transaction.

## 6.3. Insights Métier : Ce que nous disent les données
L'analyse du mois de Janvier 2026 révèle des points d'attention stratégiques :
*   **Segmentation de la Rentabilité :** Le Top 10 des clients génère plus de 60% de la marge nette, confirmant l'importance de la fidélisation des "Grands Comptes".
*   **Optimisation du Yield :** L'écart entre le taux servi et la profitabilité billing varie selon les segments, ouvrant la voie à une segmentation tarifaire plus fine.

---

# VII. Conclusion & Perspectives

Ce projet démontre qu'avec une maîtrise combinée de Python, SQL et Power BI, il est possible de bâtir un système de reporting bancaire industriel, fiable et esthétique en un temps record. 

**Perspectives d'évolution :**
*   **Prédictivité :** Intégrer des modèles de Machine Learning (Python) pour prédire les fuites de dépôts (Churn) ou les pics de flux de trésorerie.
*   **Temps Réel :** Connecter le pipeline à un flux de données en streaming (Kafka) pour un reporting rafraîchi à la minute.
