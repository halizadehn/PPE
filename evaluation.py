import os
import numpy as np
import pandas as pd


def fidelity(K, explanation_file):
    df = pd.read_csv(explanation_file, header=None, index_col=False)
    df.columns = ["user_id", "movie_id", "rating", "prediction_rate", "persuasiveness_degree"]
    
    user_ids = df["user_id"].unique()
    total_fidelity = 0

    for user_id in user_ids:
        user_data = df[df["user_id"] == user_id].head(K)
        persuasive_scores = user_data["persuasiveness_degree"].astype(float)
        persuasive_scores = [1 if score != -1 else score for score in persuasive_scores]
        total_fidelity += sum(persuasive_scores) / K

    return total_fidelity / len(user_ids) 


def persuasion_based_fidelity(K, explanation_file):
    df = pd.read_csv(explanation_file, header=None, index_col=False)
    df.columns = ["user_id", "movie_id", "rating", "prediction_rate", "persuasiveness_degree"]
    
    user_ids = df["user_id"].unique()
    total_fidelity = 0

    for user_id in user_ids:
        user_data = df[df["user_id"] == user_id].head(K)
        persuasive_scores = user_data["persuasiveness_degree"].astype(float)
        max_persuasive_value = max_user_persuasion_score(uid)
        persuasive_scores = [float(score) / max_persuasive_value if score != -1 else 0 for score in persuasive_scores]
        total_fidelity += sum(persuasive_scores) / K

    return total_fidelity / len(user_ids) 
    

def max_user_persuasion_score(uid):
    social_score, commitment_score, authority_score = get_persuasion_profile(uid)
    return max(social_score, commitment_score, authority_score)


