from sklearn.metrics import ndcg_score, dcg_score
import os
import numpy as np
import pandas as pd
data_dir = "Data/"
rec_dir = "Data/Recommendations/"
exp_dir = "Data/Explanation/"


def get_recommendations(uid):
    result = rec_df.query("uid==" + str(uid))
    result = result.reset_index()
    items = result["iid"].tolist()
    return items


def get_real_items(uid):
    result = test_df.query("user_id==" + str(uid))
    items = result["movie_id"].tolist()
    return items


def fidelity(K, persuade):
    df = pd.read_csv(exp_dir + "kgin2.csv", header=None, index_col=False)
    df.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]
    df = df.replace(-1.0, 0.0)
    persuasive_scores = df["persuade_degree"].tolist()
    if K == 10:
        if persuade == 0:
            persuasive_scores = [1 if float(i) != 0 else i for i in persuasive_scores]
            return sum(persuasive_scores) / len(persuasive_scores)
        else:
            max_value = max(persuasive_scores)
            persuasive_scores = [float(i) / (max_value) for i in persuasive_scores]
            return sum(persuasive_scores) / len(persuasive_scores)

    top_scores = []
    for i in range(int(len(persuasive_scores)/10)):
        j = i * 10
        top_scores.append(persuasive_scores[j])
        top_scores.append(persuasive_scores[j + 1])
        top_scores.append(persuasive_scores[j + 2])
        if K == 5:
            top_scores.append(persuasive_scores[j+3])
            top_scores.append(persuasive_scores[j + 4])

    if persuade == 0:
        top_scores = [1 if float(i) != 0 else i for i in top_scores]
        return sum(top_scores) / len(top_scores)
    else:
        max_value = max(top_scores)
        top_scores = [float(i) / (max_value) for i in top_scores]
        return sum(top_scores) / len(top_scores)


def persuade_per_user_fidelity(K):
    df = pd.read_csv(exp_dir + "evaluate_info_kgin_baseline2.csv", header=None, index_col=False)
    df.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]
    df = df.replace(-1.0, 0.0)
    persuasive_scores = df["persuade_degree"].tolist()
    fidelity = 0
    for i in range(int(len(persuasive_scores)/10)):
        scores = persuasive_scores[10*i:K+(10*i)]
        # max_value = max(scores)
        uid = df.loc[i*10, "user_id"]
        max_value = get_max_persuasive_score(uid)
        if max_value != 0:
            scores = [float(x) / max_value for x in scores]
            fidelity += sum(scores) / len(scores)
        else:
            print(i)
    return fidelity/int(len(persuasive_scores)/10)


def get_max_persuasive_score(uid):
    social_score, commitment_score, authority_score = get_persuasion_profile(uid)
    return max(social_score, commitment_score, authority_score)


