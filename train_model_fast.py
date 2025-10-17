"""
Anomalyze Fast Model Training Script
"""

from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, f1_score, accuracy_score, precision_score, recall_score
from sklearn.feature_selection import VarianceThreshold
import numpy as np
import os
from utils.preprocessing import load_and_preprocess_data
import joblib

# Configure folders
MODELS_FOLDER = 'models'
if not os.path.exists(MODELS_FOLDER):
    os.makedirs(MODELS_FOLDER)

# Paths for saved model files
MODEL_PATH = os.path.join(MODELS_FOLDER, 'ensemble_models.joblib')
SCALER_PATH = os.path.join(MODELS_FOLDER, 'scaler.joblib')
COLUMNS_PATH = os.path.join(MODELS_FOLDER, 'data_columns.joblib')
THRESHOLD_PATH = os.path.join(MODELS_FOLDER, 'optimal_threshold.joblib')
SILHOUETTE_SCORES_PATH = os.path.join(MODELS_FOLDER, 'silhouette_scores.joblib')

def create_optimized_ensemble():
    """Create an optimized ensemble with improved cluster quality and accuracy."""
    print("Creating OPTIMIZED ensemble models (5 models)...")
    print("Improvements: Better scaling, optimal cluster counts, more iterations\n")
    
    train_data_path = 'data/KDDTrain+.txt'
    df_train = load_and_preprocess_data(train_data_path)
    df_normal = df_train[df_train['label'] == 'normal']
    df_normal = df_normal.drop('label', axis=1)
    
    print(f"Training on {len(df_normal)} normal samples with {len(df_normal.columns)} features")
    
    data_columns = df_normal.columns
    
    # OPTIMIZATION 1: Use RobustScaler for better handling of outliers
    # This often leads to better clustering quality
    print("Applying RobustScaler (better outlier handling)...")
    scaler = RobustScaler()
    df_normal_scaled = scaler.fit_transform(df_normal)
    
    # OPTIMIZATION 2: More models with diverse, optimal cluster counts
    # Research shows 5-15 clusters work well for network traffic
    models = []
    silhouette_scores = []
    cluster_configs = [
        {'n_clusters': 6, 'random_state': 42},   # Smaller clusters for tight grouping
        {'n_clusters': 8, 'random_state': 123},  # Medium clusters
        {'n_clusters': 10, 'random_state': 456}, # Larger clusters for variety
        {'n_clusters': 12, 'random_state': 789}, # Capture fine-grained patterns
        {'n_clusters': 8, 'random_state': 999}   # Another medium for ensemble diversity
    ]
    
    for i, config in enumerate(cluster_configs):
        print(f"\nTraining optimized model {i+1}/{len(cluster_configs)}...")
        print(f"  Config: {config['n_clusters']} clusters")
        
        # OPTIMIZATION 3: Better KMeans parameters
        # - More initializations (n_init=20 instead of 10)
        # - More iterations (max_iter=500 instead of 300)
        # - k-means++ initialization (default, better starting points)
        model = KMeans(
            n_init=20,           # More initializations for better convergence
            max_iter=500,        # More iterations to find optimal clusters
            tol=1e-5,            # Tighter convergence tolerance
            algorithm='lloyd',   # More stable algorithm
            **config
        )
        model.fit(df_normal_scaled)
        
        # Calculate silhouette score for cluster quality
        cluster_labels = model.predict(df_normal_scaled)
        silhouette = silhouette_score(df_normal_scaled, cluster_labels)
        silhouette_scores.append(silhouette)
        
        print(f"  ✓ Silhouette Score: {silhouette:.4f}")
        print(f"  ✓ Inertia: {model.inertia_:.2f}")
        
        models.append(model)
    
    avg_silhouette = np.mean(silhouette_scores)
    print(f"\n{'='*60}")
    print(f"Average Silhouette Score: {avg_silhouette:.4f}")
    print(f"Min: {np.min(silhouette_scores):.4f} | Max: {np.max(silhouette_scores):.4f}")
    print(f"{'='*60}")
    
    return models, scaler, data_columns, silhouette_scores

def find_optimal_threshold_refined(models, scaler, data_columns):
    """Find optimal threshold with refined search for better accuracy."""
    print("\nFinding optimal threshold (refined search)...")
    
    train_data_path = 'data/KDDTrain+.txt'
    df_train = load_and_preprocess_data(train_data_path)
    
    true_labels = (df_train['label'] != 'normal').astype(int)
    df_train_features = df_train.drop('label', axis=1)
    df_train_features = df_train_features.reindex(columns=data_columns, fill_value=0)
    df_train_scaled = scaler.transform(df_train_features)
    
    print(f"Evaluating on {len(df_train)} samples ({true_labels.sum()} attacks, {(~true_labels.astype(bool)).sum()} normal)")
    
    # Calculate ensemble distances
    all_distances = []
    for model in models:
        distances = model.transform(df_train_scaled).min(axis=1)
        all_distances.append(distances)
    
    avg_distances = np.mean(all_distances, axis=0)
    
    # OPTIMIZATION 4: Two-stage threshold search with balanced metric
    # Stage 1: Coarse search focusing on balanced F1 and Accuracy
    print("Stage 1: Coarse search...")
    best_threshold = None
    best_score = 0
    best_metrics = {}
    
    percentiles_coarse = np.arange(75, 96, 1.0)  # Wider range for better balance
    
    for percentile in percentiles_coarse:
        threshold = np.percentile(avg_distances, percentile)
        predicted_labels = (avg_distances > threshold).astype(int)
        
        acc = accuracy_score(true_labels, predicted_labels)
        f1 = f1_score(true_labels, predicted_labels, zero_division=0)
        prec = precision_score(true_labels, predicted_labels, zero_division=0)
        rec = recall_score(true_labels, predicted_labels, zero_division=0)
        
        # Balanced score: prioritize F1 but also consider accuracy
        balanced_score = (0.7 * f1) + (0.3 * acc)
        
        if balanced_score > best_score:
            best_score = balanced_score
            best_threshold = threshold
            best_metrics = {
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1': f1,
                'percentile': percentile,
                'balanced_score': balanced_score
            }
    
    # Stage 2: Fine-tune around best threshold
    print(f"Stage 2: Fine-tuning around {best_metrics['percentile']:.1f}th percentile...")
    
    percentiles_fine = np.linspace(
        max(70, best_metrics['percentile'] - 2.0),
        min(98, best_metrics['percentile'] + 2.0),
        40  # More granular search
    )
    
    for percentile in percentiles_fine:
        threshold = np.percentile(avg_distances, percentile)
        predicted_labels = (avg_distances > threshold).astype(int)
        
        acc = accuracy_score(true_labels, predicted_labels)
        f1 = f1_score(true_labels, predicted_labels, zero_division=0)
        prec = precision_score(true_labels, predicted_labels, zero_division=0)
        rec = recall_score(true_labels, predicted_labels, zero_division=0)
        
        # Balanced score
        balanced_score = (0.7 * f1) + (0.3 * acc)
        
        if balanced_score > best_score:
            best_score = balanced_score
            best_threshold = threshold
            best_metrics = {
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1': f1,
                'percentile': percentile,
                'balanced_score': balanced_score
            }
    
    print(f"\n{'='*60}")
    print(f"Optimal Threshold Found: {best_threshold:.6f}")
    print(f"Percentile: {best_metrics['percentile']:.2f}th")
    print(f"\nPerformance Metrics:")
    print(f"  Accuracy:  {best_metrics['accuracy']:.4f} ({best_metrics['accuracy']*100:.2f}%)")
    print(f"  Precision: {best_metrics['precision']:.4f} ({best_metrics['precision']*100:.2f}%)")
    print(f"  Recall:    {best_metrics['recall']:.4f} ({best_metrics['recall']*100:.2f}%)")
    print(f"  F1-Score:  {best_metrics['f1']:.4f} ({best_metrics['f1']*100:.2f}%)")
    print(f"{'='*60}")
    
    return best_threshold

def main():
    print("=" * 60)
    print("Anomalyze OPTIMIZED Model Training")
    print("Enhanced for QUALITY: Better Silhouette & Accuracy")
    print("=" * 60)
    print()
    
    import time
    start_time = time.time()
    
    # Create optimized ensemble
    models, scaler, data_columns, silhouette_scores = create_optimized_ensemble()
    
    # Find optimal threshold with refined search
    optimal_threshold = find_optimal_threshold_refined(models, scaler, data_columns)
    
    # Save all components
    print("\nSaving models...")
    joblib.dump(models, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(data_columns, COLUMNS_PATH)
    joblib.dump(optimal_threshold, THRESHOLD_PATH)
    joblib.dump(silhouette_scores, SILHOUETTE_SCORES_PATH)
    print("✓ All models saved successfully!")
    
    training_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("✅ OPTIMIZED Training Complete!")
    print("=" * 60)
    print(f"Models saved to: {MODELS_FOLDER}")
    print(f"Number of models: {len(models)} (ensemble for robustness)")
    print(f"Training time: {training_time:.2f} seconds")
    print(f"\n📊 Clustering Quality (Silhouette Scores):")
    for i, score in enumerate(silhouette_scores):
        print(f"  Model {i+1}: {score:.4f} ({score*100:.2f}%)")
    print(f"  Average:  {np.mean(silhouette_scores):.4f} ({np.mean(silhouette_scores)*100:.2f}%)")
    print(f"\n🎯 Optimal Threshold: {optimal_threshold:.6f}")
    print("\n💡 Improvements Applied:")
    print("  ✓ RobustScaler for better outlier handling")
    print("  ✓ 5 diverse models with optimal cluster counts (6-12)")
    print("  ✓ Enhanced KMeans: 20 initializations, 500 iterations")
    print("  ✓ Two-stage threshold optimization")
    print("  ✓ Higher silhouette scores = better clustering")
    print("  ✓ Higher accuracy/F1 = better anomaly detection")
    print("=" * 60)

if __name__ == '__main__':
    main()
