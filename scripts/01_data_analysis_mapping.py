import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Configuration des chemins
RAW_DATA_PATH = "data/raw/PS_20174392719_1491204439457_log.csv"
PROCESSED_DATA_PATH = "data/processed/"

def analyze_and_map_data(file_path):
    print(f"Démarrage de l'échantillonnage temporel (Scanning du fichier complet)...")
    
    dtypes = {
        'step': 'int32',
        'type': 'category',
        'amount': 'float64',
        'nameOrig': 'object',
        'oldbalanceOrg': 'float64',
        'newbalanceOrig': 'float64'
    }
    
    # Stratégie : On lit le fichier par morceaux (chunks) et on garde 5% de chaque morceau
    # Cela nous permet de couvrir TOUTE la période du dataset (31 jours)
    chunk_list = []
    chunk_size = 200000
    
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, dtype=dtypes, usecols=list(dtypes.keys())):
            # On échantillonne 2% de chaque morceau pour avoir un dataset final maniable (~120k lignes)
            sampled_chunk = chunk.sample(frac=0.02)
            chunk_list.append(sampled_chunk)
            if len(chunk_list) % 5 == 0:
                print(f"Progression : {len(chunk_list) * chunk_size / 1000000:.1f}M de lignes analysées...")

        df = pd.concat(chunk_list)
        print(f"Échantillonnage terminé : {len(df)} transactions récupérées sur tout le mois.")
        
        # 1. Conversion du 'step' en Timeline (1 step = 1 heure)
        start_date = datetime(2026, 1, 1)
        df['transaction_timestamp'] = df['step'].apply(lambda x: start_date + timedelta(hours=x))
        df['transaction_date'] = df['transaction_timestamp'].dt.date
        
        # 2. Mapping Métier
        billing_map = {
            'PAYMENT': 'Service_Standard',
            'TRANSFER': 'Virement_International',
            'CASH_OUT': 'Retrait_Fonds',
            'DEBIT': 'Frais_Gestion',
            'CASH_IN': 'Depot_Flux'
        }
        df['billing_category'] = df['type'].map(billing_map)
        
        # Sauvegarde
        sample_filename = os.path.join(PROCESSED_DATA_PATH, "cib_data_sample.csv")
        df.to_csv(sample_filename, index=False)
        print(f"Nouveau dataset 'Full Month' sauvegardé : {sample_filename}")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    analyze_and_map_data(RAW_DATA_PATH)
