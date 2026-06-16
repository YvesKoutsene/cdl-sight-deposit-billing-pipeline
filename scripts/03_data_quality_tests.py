import pandas as pd
import numpy as np

# Configuration
RESULTS_FILE = "data/processed/cib_final_results.csv"

def run_quality_suite():
    print("Démarrage de la suite de tests de Qualité de Données (DQ)...")
    
    try:
        df = pd.read_csv(RESULTS_FILE)
        errors_found = 0

        # --- TEST 1 : Vérification des montants négatifs ---
        # En banque de flux, un billing ou un intérêt versé ne peut pas être négatif dans ce modèle
        neg_billing = df[df['total_billing'] < 0].shape[0]
        neg_interests = df[df['total_interests'] < 0].shape[0]
        
        if neg_billing == 0 and neg_interests == 0:
            print("TEST 1 Passé : Aucun montant financier négatif détecté.")
        else:
            print(f"TEST 1 Échoué : {neg_billing + neg_interests} anomalies de signe détectées.")
            errors_found += 1

        # --- TEST 2 : Cohérence du calcul d'intérêts (Unit Test) ---
        # Règle : Si solde > 500k, taux = 3%. 
        # Pour 1 000 000 €, intérêt quotidien = (1M * 0.03) / 360 = 83.333...
        # On vérifie sur un échantillon de gros soldes
        high_balances = df[df['avg_daily_balance'] > 1000000].head(10)
        tolerance = 0.01
        
        test_2_fail = False
        for _, row in high_balances.iterrows():
            expected = (row['avg_daily_balance'] * 0.03) / 360
            if abs(row['total_interests'] - expected) > tolerance:
                test_2_fail = True
                break
        
        if not test_2_fail:
            print("TEST 2 Passé : La logique de calcul à 3% est mathématiquement exacte.")
        else:
            print("TEST 2 Échoué : Écart de calcul détecté sur les gros soldes.")
            errors_found += 1

        # --- TEST 3 : Intégrité des IDs Clients ---
        null_clients = df['client_id'].isnull().sum()
        if null_clients == 0:
            print("TEST 3 Passé : 100% des transactions sont rattachées à un client valide.")
        else:
            print(f"TEST 3 Échoué : {null_clients} transactions orphelines.")
            errors_found += 1

        # --- BILAN FINAL ---
        print("\n" + "="*40)
        if errors_found == 0:
            print("STATUT : DONNÉES CERTIFIÉES POUR POWER BI")
            print("Félicitations, le pipeline est robuste.")
        else:
            print(f"STATUT : {errors_found} ERREUR(S) À CORRIGER")
        print("="*40)

    except Exception as e:
        print(f"Erreur lors de l'exécution des tests : {e}")

if __name__ == "__main__":
    run_quality_suite()
