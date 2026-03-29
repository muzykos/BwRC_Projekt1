import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean, chebyshev
from collections import defaultdict

def extract_features(file_path):
    """
    Przetwarza plik CSV i wylicza średni czas trzymania (Hold Time) dla każdego klawisza.
    """
    try:
        df = pd.read_csv(file_path, sep=';', header=None, names=['ts', 'key', 'event'])
    except Exception as e:
        print(f"Błąd odczytu {file_path}: {e}")
        return None

    hold_times = defaultdict(list)
    key_downs = {}

    for _, row in df.iterrows():
        key = str(row['key']).lower()
        event = str(row['event']).strip()
        ts = row['ts']

        if event == 'keydown':
            key_downs[key] = ts
        elif event == 'keyup' and key in key_downs:
            duration = ts - key_downs[key]
            hold_times[key].append(duration)
            del key_downs[key]

    features = {key: np.mean(times) for key, times in hold_times.items()}
    return features

def main():
    base_path = 'biometric_data'
    all_data = []
    labels = []

    # 1. Ładowanie danych
    print("Ładowanie danych...")
    if not os.path.exists(base_path):
        print(f"Folder {base_path} nie istnieje!")
        return

    for user_name in os.listdir(base_path):
        user_dir = os.path.join(base_path, user_name)
        if os.path.isdir(user_dir):
            for file_name in os.listdir(user_dir):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(user_dir, file_name)
                    features = extract_features(file_path)
                    if features:
                        features['user'] = user_name
                        all_data.append(features)

    df_features = pd.DataFrame(all_data).fillna(0)  # Uzupełnienie brakujących klawiszy zerami
    X = df_features.drop('user', axis=1)
    y = df_features['user']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- ANALIZA 1: Podobieństwo ---
    print("\n--- Analiza podobieństwa (odległości między średnimi profilami osób) ---")
    user_means = df_features.groupby('user').mean()
    users = user_means.index.tolist()
    
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            u1, u2 = users[i], users[j]
            dist_e = euclidean(user_means.loc[u1], user_means.loc[u2])
            dist_c = chebyshev(user_means.loc[u1], user_means.loc[u2])
            print(f"{u1} vs {u2} -> Euklides: {dist_e:.4f}, Czebyszew: {dist_c:.4f}")

    # --- ANALIZA 2: PCA ---
    print("\n--- Analiza istotności cech (PCA) ---")
    pca = PCA(n_components=2)
    pca.fit(X_scaled)
    
    loadings = pd.DataFrame(
        np.abs(pca.components_[0]), 
        index=X.columns, 
        columns=['Importance']
    ).sort_values(by='Importance', ascending=False)
    
    print("Top 5 najbardziej istotnych klawiszy wg PCA:")
    print(loadings.head(5))

    # --- ANALIZA 3: k-Means ---
    print("\n--- Weryfikacja jednolitości (k-Means, k=15) ---")
    k = 15
    n_clusters = min(k, len(df_features))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    analysis_df = pd.DataFrame({'User': y, 'Cluster': clusters})
    
    for user in users:
        user_clusters = analysis_df[analysis_df['User'] == user]['Cluster'].unique()
        n_user_clusters = len(user_clusters)
        samples_count = len(analysis_df[analysis_df['User'] == user])
        print(f"Użytkownik {user}: próbki ({samples_count}) rozrzucone w {n_user_clusters} klastrach.")

if __name__ == "__main__":
    main()