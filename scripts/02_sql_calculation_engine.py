import duckdb
import pandas as pd
import os

# Configuration
INPUT_CSV = "data/processed/cib_data_sample.csv"
OUTPUT_FINAL = "data/processed/cib_final_results.csv"

def run_sql_engine():
    print(f"Initialisation du moteur SQL DuckDB...")
    
    # Connexion à DuckDB (en mémoire pour la rapidité)
    con = duckdb.connect(database=':memory:')
    
    # Chargement du CSV dans une table DuckDB
    con.execute(f"CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('{INPUT_CSV}')")
    
    print("Calcul du Billing et des Intérêts en cours...")
    
    # Requête SQL Maîtresse : CTE pour organiser la logique
    # 1. On calcule le Billing par transaction
    # 2. On calcule les intérêts quotidiens (Pratice CIB : Base 360 jours)
    query = """
    WITH base_calculations AS (
        SELECT 
            nameOrig AS client_id,
            transaction_date,
            billing_category,
            amount,
            oldbalanceOrg AS daily_balance,
            -- Logique de Billing (Facturation)
            CASE 
                WHEN billing_category = 'Virement_International' THEN 15.0
                WHEN billing_category = 'Retrait_Fonds' THEN amount * 0.0005
                WHEN billing_category = 'Frais_Gestion' THEN 50.0
                ELSE 2.0 -- Frais de service standard
            END AS billing_fee,
            -- Logique d'Intérêts par Paliers (Sight Deposit)
            -- Si solde > 500k€ : 3% annuel, sinon 1.5%
            CASE 
                WHEN oldbalanceOrg > 500000 THEN (oldbalanceOrg * 0.03) / 360
                ELSE (oldbalanceOrg * 0.015) / 360
            END AS interest_earned_daily
        FROM raw_data
    )
    SELECT 
        client_id,
        transaction_date,
        SUM(amount) as total_volume,
        SUM(billing_fee) as total_billing,
        SUM(interest_earned_daily) as total_interests,
        AVG(daily_balance) as avg_daily_balance
    FROM base_calculations
    GROUP BY client_id, transaction_date
    ORDER BY transaction_date, client_id
    """
    
    # Exécution et conversion en DataFrame
    df_results = con.execute(query).df()
    
    # Sauvegarde des résultats finaux
    df_results.to_csv(OUTPUT_FINAL, index=False)
    
    print(f"Calculs terminés. Résultats sauvegardés dans : {OUTPUT_FINAL}")
    print("\n--- Aperçu des 5 premières lignes du reporting financier ---")
    print(df_results.head())
    
    # Petite stat pour l'entretien
    total_rev = df_results['total_billing'].sum()
    total_int = df_results['total_interests'].sum()
    print(f"\nRevenu Billing Total : {total_rev:,.2f} EUR")
    print(f"Intérêts Totaux versés aux clients : {total_int:,.2f} EUR")

if __name__ == "__main__":
    # Installation de duckdb si nécessaire
    try:
        import duckdb
    except ImportError:
        os.system('pip install duckdb --quiet')
        import duckdb
        
    run_sql_engine()
