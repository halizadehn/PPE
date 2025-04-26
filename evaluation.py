from sklearn.metrics import ndcg_score, dcg_score
import os
import numpy as np
import pandas as pd
data_dir = "Data/"
rec_dir = "Data/Recommendations/"


def fidelity(K, explanation_file):
    df = pd.read_csv(explanation_file, header=None, index_col=False)
    df.columns = ["user_id", "movie_id", "rating", "prediction_rate", "persuasiveness_degree"]
    persuasive_scores = df["persuade_degree"].tolist()
    persuasive_scores = [1 if float(score) != -1 else score for score in persuasive_scores]
    fidelity = sum(persuasive_scores) / len(persuasive_scores)
        
    K_scores = []
    for i in range(int(len(persuasive_scores)/10)):
        j = i * 10
        if K == 3:
            K_scores .append(persuasive_scores[j])
            K_scores .append(persuasive_scores[j + 1])
            K_scores .append(persuasive_scores[j + 2])
        if K == 5:
            K_scores .append(persuasive_scores[j+3])
            K_scores .append(persuasive_scores[j + 4])
        
     K_scores  = [1 if float(i) != 0 else i for i in K_scores ]
     return sum(K_scores) / len(K_scores)
    


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
        max_persuasive_value = get_max_persuasive_score(uid)
        persuasive_scores = [float(score) / max_persuasive_value if score != -1 else 0 for score in persuasive_scores]
        total_fidelity += sum(persuasive_scores) / K

    return total_fidelity / len(user_ids) 
    

def get_max_persuasive_score(uid):
    social_score, commitment_score, authority_score = get_persuasion_profile(uid)
    return max(social_score, commitment_score, authority_score)


