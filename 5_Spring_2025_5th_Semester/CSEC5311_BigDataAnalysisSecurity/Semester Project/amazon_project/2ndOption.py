# amazon_data_analysis.py

import pandas as pd
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from datetime import datetime
from collections import defaultdict

# -----------------------------
# Utility Functions
# -----------------------------
def parse_amazon_meta(file_path):
    """Parses amazon-meta.txt and returns product metadata."""
    data = []
    with open(file_path, encoding='latin1') as f:
        product = {}
        for line in f:
            line = line.strip()
            if line.startswith("Id: "):
                if product:
                    data.append(product)
                product = {'Id': int(line.split('Id: ')[1])}
            elif line.startswith("ASIN: "):
                product['ASIN'] = line.split('ASIN: ')[1]
            elif line.startswith("  title: "):
                product['title'] = line.split('  title: ')[1]
            elif line.startswith("  group: "):
                product['group'] = line.split('  group: ')[1]
            elif line.startswith("  salesrank: "):
                try:
                    product['salesrank'] = int(line.split('  salesrank: ')[1])
                except:
                    product['salesrank'] = None
            elif line.startswith("  similar: "):
                product['similar'] = line.split('  similar: ')[1].split()[1:]
            elif line.startswith("  reviews: "):
                product['reviews'] = []
            elif re.match(r"^\d{4}-\d{1,2}-\d{1,2}", line):
                parts = line.split()
                if 'reviews' in product:
                    product['reviews'].append({
                        'date': parts[0],
                        'rating': int(parts[2])
                    })
        if product:
            data.append(product)
    return data

# -----------------------------
# Option 1: KNN-Based Recommendation
# -----------------------------
def build_knn_recommender(products):
    asin_to_idx = {p['ASIN']: idx for idx, p in enumerate(products)}
    n = len(products)
    matrix = np.zeros((n, n))
    for p in products:
        i = asin_to_idx[p['ASIN']]
        for sim in p.get('similar', []):
            if sim in asin_to_idx:
                j = asin_to_idx[sim]
                matrix[i][j] = 1
                matrix[j][i] = 1
    knn = NearestNeighbors(metric='cosine')
    knn.fit(matrix)
    return knn, asin_to_idx, products

# -----------------------------
# Option 2: Sales Rank Prediction (XGBoost)
# -----------------------------
def build_salesrank_model(products):
    rows = []
    for p in products:
        if p.get('salesrank') and p.get('reviews'):
            rows.append({
                'avg_rating': np.mean([r['rating'] for r in p['reviews']]),
                'review_count': len(p['reviews']),
                'similar_count': len(p.get('similar', [])),
                'salesrank': p['salesrank']
            })
    df = pd.DataFrame(rows)
    X = df[['avg_rating', 'review_count', 'similar_count']]
    y = df['salesrank']
    model = XGBRegressor()
    model.fit(X, y)
    preds = model.predict(X)
    rmse = mean_squared_error(y, preds, squared=False)
    return model, rmse

# -----------------------------
# Option 3: Co-purchase Graph Analysis
# -----------------------------
def build_graph(products):
    G = nx.Graph()
    for p in products:
        G.add_node(p['ASIN'])
        for sim in p.get('similar', []):
            G.add_edge(p['ASIN'], sim)
    return G

# -----------------------------
# Option 4: Review Time Series Analysis
# -----------------------------
def build_review_timeseries(products):
    timeline = defaultdict(list)
    for p in products:
        for review in p.get('reviews', []):
            date = pd.to_datetime(review['date'], errors='coerce')
            if not pd.isnull(date):
                key = date.strftime('%Y-%m')
                timeline[key].append(review['rating'])
    df = pd.DataFrame({
        'month': sorted(timeline.keys()),
        'avg_rating': [np.mean(timeline[m]) for m in sorted(timeline.keys())],
        'count': [len(timeline[m]) for m in sorted(timeline.keys())]
    })
    df.set_index('month', inplace=True)
    return df

# -----------------------------
# Main Driver
# -----------------------------
def main():
    file_path = 'amazon-meta.txt'  # Update this path as needed
    products = parse_amazon_meta(file_path)

    print("[INFO] Parsed products:", len(products))

    print("\n[OPTION 1] KNN Recommendation Example")
    knn, asin_to_idx, products = build_knn_recommender(products)
    sample_asin = next(iter(asin_to_idx))
    distances, indices = knn.kneighbors([knn._fit_X[asin_to_idx[sample_asin]]], n_neighbors=5)
    print("Top 5 similar ASINs for", sample_asin, ":", [products[i]['ASIN'] for i in indices[0]])

    print("\n[OPTION 2] Sales Rank Prediction")
    model, rmse = build_salesrank_model(products)
    print("XGBoost RMSE:", rmse)

    print("\n[OPTION 3] Graph Analysis")
    G = build_graph(products)
    print("Nodes:", len(G.nodes), ", Edges:", len(G.edges))
    print("Top 5 most connected products:", sorted(G.degree, key=lambda x: -x[1])[:5])

    print("\n[OPTION 4] Review Time Series")
    ts_df = build_review_timeseries(products)
    ts_df[['avg_rating', 'count']].plot(title='Review Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
