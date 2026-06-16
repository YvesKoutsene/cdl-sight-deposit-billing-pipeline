# Dictionnaire de Données & Règles Métier

Ce document détaille les spécifications fonctionnelles et techniques utilisées pour le simulateur de Billing et d'Intérêts CIB.

## 1. Modèle de Données (Output Final)

| Colonne | Description | Type |
| :--- | :--- | :--- |
| `client_id` | Identifiant unique du client Corporate (Source: nameOrig) | Texte |
| `transaction_date` | Date de l'agrégation (Format: YYYY-MM-DD) | Date |
| `total_volume` | Somme des flux financiers traités sur la journée | Nombre |
| `total_billing` | Total des commissions de service facturées | Nombre |
| `total_interests` | Total des intérêts créditeurs calculés (Sight Deposit) | Nombre |
| `avg_daily_balance` | Solde moyen quotidien utilisé pour le calcul d'intérêts | Nombre |

## 2. Règles de Facturation (Billing)

La logique de facturation simule les frais de Cash Management de BNP Paribas :

*   **Virements Internationaux (TRANSFER) :** 15,00 € par transaction.
*   **Retrait de Fonds (CASH_OUT) :** Commission proportionnelle de 0,05% du montant.
*   **Frais de Gestion (DEBIT) :** Forfait fixe de 50,00 € par mois (appliqué par transaction de type débit).
*   **Services Standards (PAYMENT) :** 2,00 € par transaction.

## 3. Calcul des Intérêts (CDL Sight Deposit)

Le calcul suit les normes bancaires européennes (Base de calcul : **ACT/360**) :

| Palier de Solde | Taux Annuel Appliqué |
| :--- | :--- |
| Solde > 500 000 € | **3,00 %** |
| Solde <= 500 000 € | **1,50 %** |

**Formule utilisée :** `(Solde * Taux) / 360`

---
## 4. Certification Qualité (Tests de Non-Régression)

Trois points de contrôle automatisés sont exécutés avant chaque mise à jour du reporting :
1. **Intégrité Signe :** Absence de montants négatifs sur les frais et intérêts.
2. **Précision Mathématique :** Vérification unitaire sur un échantillon de comptes > 1M€.
3. **Réconciliation :** 100% des lignes rattachées à une `dim_client` valide.
