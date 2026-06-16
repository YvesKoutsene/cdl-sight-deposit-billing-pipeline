# CIB Billing & Interest Reporting Simulator

## Présentation du Projet
Ce projet simule un moteur de **Billing (facturation)** et de **Calcul d'Intérêts sur Comptes à Vue (Sight Deposits)** au sein d'une banque de financement et d'investissement (CIB). 

L'objectif est de démontrer une maîtrise technique complète appliquée à des problématiques métier réelles de gestion de flux bancaires Corporate chez **BNP Paribas**.

## Résultats du Prototype (Janvier 2026)
- **Volume traité :** ~6,3 Millions de transactions analysées.
- **Revenu Billing généré :** ~4,25 M€.
- **Intérêts versés (Expense) :** ~8,75 M€.
- **Nombre de clients Corporate :** Portefeuille diversifié avec solde moyen de 900k€.

## Aperçu du Dashboard Power BI

### 1. Vue Executive (Profitabilité Globale)
![Vue Executive](docs/Images/Vue%20Executive.png)

### 2. Analyse Clients & Segmentation
![Analyse Clients](docs/Images/Analyse%20Clients.png)

### 3. Suivi Temporel des Flux
![Analyse Temporelle](docs/Images/Analyse%20Temporelle.png)

## Stack Technique
- **Python (Pandas)** : ETL, échantillonnage temporel et tests de non-régression.
- **SQL (DuckDB)** : Moteur de calcul financier haute performance (Base ACT/360).
- **Power BI** : Dashboard décisionnel multi-pages (Vue Executive, Analyse Clients, Audit).
- **Git** : Gestion de version et documentation technique.

## Structure du Dépôt
- `scripts/` : Logiciels d'extraction et de calcul.
- `sql/` : Requêtes de modélisation financière.
- `powerbi/` : Fichier `.pbix` prêt à l'emploi.
- `docs/` : Dictionnaire de données et spécifications fonctionnelles.

## Certification Qualité
Le pipeline inclut une suite de tests automatisés (`scripts/03_data_quality_tests.py`) garantissant l'exactitude des calculs financiers avant l'importation dans Power BI.

---
*Projet réalisé pour la préparation à l'alternance Développeur Business Reporting*
