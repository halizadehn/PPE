from sklearn.metrics import ndcg_score, dcg_score
import os
import numpy as np
import pandas as pd
data_dir = "Data/"
rec_dir = "Data/Recommendations/"
exp_dir = "Data/Explanation/"


def get_top_recommendations(uid):
    result = rec_df.query("uid==" + str(uid))
    result = result.reset_index()
    items = result["iid"].tolist()
    return items


def get_real_items(uid):
    result = test_df.query("user_id==" + str(uid))
    items = result["movie_id"].tolist()
    return items


def evaluate_info():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df = pd.DataFrame()
    for i in range(len(users)):
        uid = users[i]
        recommendations = get_top_recommendations(uid)
        real_items = get_real_items(uid)

        for r in recommendations:
            if r in real_items:
                true_relevance = get_real_rate(uid, r)
            else:
                true_relevance = 0
            score = float(get_estimate_rate(uid, r))
            persuade_degree = get_persuade_degree(uid, r)

            df.loc[0, "user_id"] = str(uid)
            df.loc[0, "movie_id"] = str(r)
            df.loc[0, "true_relevance"] = str(true_relevance)
            df.loc[0, "prediction_rate"] = str(score)
            df.loc[0, "persuade_degree"] = str(persuade_degree)
            df.to_csv(os.path.join(exp_dir + 'evaluate_info_cke_baseline3.csv'), mode='a', header=None, index=False)


def get_real_rate(uid, iid):
    result = test_df.query("user_id==" + str(uid) + "& movie_id==" + str(iid))
    return result["rating"].tolist()[0]


def get_estimate_rate(uid, iid):
    result = rec_df.query("uid==" + str(uid) + "& iid=="+ str(iid))
    result = result.reset_index()
    return result["rate"].tolist()[0]


def get_persuade_degree(uid, iid):
    result = exp_df.query("uid==" + str(uid) + "& iid==" + str(iid))
    if not result.empty:
        return result["persuade_degree"].values[0]
    else:
        return -1


def ndcg_post_processing():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_nfm.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    ndcgs = []
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()

            for j in range(len(true_relevance)):
                if true_relevance[j] > 0:
                    true_relevance[j] = 1

            true_relevance_sorted = [x for _, x in sorted(zip(true_relevance, true_relevance), reverse=True)]
            ideal_dcg = sum([true_relevance_sorted[i] / np.log2(i + 2) for i in range(10)])
            dcg = sum([true_relevance[i] / np.log2(i + 2) for i in range(10)])
            if ideal_dcg == 0:
                ndcg = 0
            else:
                ndcg = dcg / ideal_dcg
            # print(ndcg)
            ndcgs.append(ndcg)

    sum1 = 0
    count1 = 0
    for p in ndcgs:
        sum1 += p
        if p != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(ndcgs)


def ndcg_recommender():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_kgin.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    ndcgs = []
    # scores = np.asarray([[1,1,1,1,1,1,1,1,1,1]])
    # scores = np.asarray([[10,9,8,7,6,5,4,3,2,1]])
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            # result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()
            for j in range(len(true_relevance)):
                if true_relevance[j] > 0:
                    true_relevance[j] = 1
            # true_relevance = [true_relevance]
            # true_relevance = np.asarray(true_relevance)
            # ndcg = ndcg_score(true_relevance,scores,k=10)
            # print(ndcg)
            true_relevance_sorted = [x for _, x in sorted(zip(true_relevance, true_relevance), reverse=True)]
            ideal_dcg = sum([true_relevance_sorted[i] / np.log2(i + 2) for i in range(10)])
            dcg = sum([true_relevance[i] / np.log2(i + 2) for i in range(10)])
            if ideal_dcg == 0:
                ndcg = 0
            else:
                ndcg = dcg / ideal_dcg
            # print(ndcg)
            ndcgs.append(ndcg)

    sum1 = 0
    count1 = 0
    for p in ndcgs:
        sum1 += p
        if p != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(ndcgs)


def mean_reciprocal_rank():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_kgin.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    mrrs = []
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            # result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()

            mrr = 0
            for j in range(len(true_relevance)):
                relevance = true_relevance[j]
                if relevance != 0:
                    mrr = 1 / (j+1)
                    break
            # print(mrr)
            mrrs.append(mrr)

    sum1 = 0
    count1 = 0
    for m in mrrs:
        sum1 += m
        if m != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(mrrs)


def mean_reciprocal_rank_post():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_nfm.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    mrrs = []
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()

            mrr = 0
            for j in range(len(true_relevance)):
                relevance = true_relevance[j]
                if relevance != 0:
                    mrr = 1 / (j+1)
                    break
            # print(mrr)
            mrrs.append(mrr)

    sum1 = 0
    count1 = 0
    for m in mrrs:
        sum1 += m
        if m != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(mrrs)


def diversity_calculation(explanations):
    explanations = [value for value in explanations if value != "-1"]
    if not explanations:
        return 0
    if len(explanations) == 1:
        return 1
    sum = 0
    for i in range(len(explanations)):
        for j in range(i, len(explanations)):
            sum += dissimilarity(explanations[i], explanations[j])
    n = len(explanations)
    return sum / (n/2 * (n-1))


def dissimilarity(exp1, exp2):
    if exp1 == exp2:
        return 0
    else:
        return 1


def get_diversity():
    exp_df = pd.read_csv(exp_dir + 'explanation_nfm.csv', header=None, index_col=False)
    exp_df.columns = ["uid", "iid", "pred_rate", "exp", "exp_type", "persuade_degree"]
    diversity = []
    for i in range(int(len(exp_df)/10)):
        explanations = exp_df[i*10: (i+1)*10]["exp_type"].tolist()
        diversity.append(diversity_calculation(explanations))
    print(len(diversity))
    print(diversity)
    print(sum(diversity)/len(diversity))


def fidelity(K, persuade):
    df = pd.read_csv(exp_dir + "evaluate_info_kgin_baseline2.csv", header=None, index_col=False)
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
    social, commit, authority = get_persuasion_profile(uid)
    return max(social, commit, authority)


def get_user_personality(user_id):
    result = personality_df.query("user_id==" + str(user_id))
    personality = result.iloc[0].tolist()[1:]
    return personality


def get_persuasion_profile(user_id):
    personality = get_user_personality(user_id)
    social = commit = authority = 0
    count = 0
    if personality[0] == 1: #high_EXT
        social += 4
        commit += 3
        authority += 1
        count += 1
    if personality[0] == -1: #low_EXT
        social += 5
        commit += 3
        authority += 1
        count += 1
    if personality[1] == 1: #high_AGR
        social += 4
        commit += 3
        authority += 2
        count += 1
    if personality[1] == -1: #low_AGR
        social += 3
        commit += 4
        authority += 1
        count += 1
    if personality[2] == 1: #high_CON
        social += 3
        commit += 5
        authority += 2
        count += 1
    if personality[2] == -1: #low_CON
        social += 3
        commit += 4
        authority += 1
        count += 1
    if personality[3] == 1: #high_NEU
        social += 4
        commit += 3
        authority += 1
        count += 1
    if personality[3] == -1: #low_NEU
        social += 4
        commit += 1
        authority += 3
        count += 1
    if personality[4] == 1: #high_OPN
        social += 4
        commit += 3
        authority += 2
        count += 1
    if personality[4] == -1: #low_OPN
        social += 5
        commit += 3
        authority += 1
        count += 1

    if count != 0:
        social = float("{:.2f}".format(social/count))
        commit = float("{:.2f}".format(commit / count))
        authority = float("{:.2f}".format(authority / count))
        return social, commit, authority
    return 0, 0, 0


def ndcg_recommender_v2():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_bprmf.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    ndcgs = []
    # scores = np.asarray([[1,1,1,1,1,1,1,1,1,1]])
    # scores = np.asarray([[10,9,8,7,6,5,4,3,2,1]])
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            # result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()[:10]
            for j in range(len(true_relevance)):
                if true_relevance[j] > 0:
                    true_relevance[j] = 1
            # true_relevance = [true_relevance]
            # true_relevance = np.asarray(true_relevance)
            # ndcg = ndcg_score(true_relevance,scores,k=10)
            # print(ndcg)
            true_relevance_sorted = [x for _, x in sorted(zip(true_relevance, true_relevance), reverse=True)]
            ideal_dcg = sum([true_relevance_sorted[i] / np.log2(i + 2) for i in range(10)])
            dcg = sum([true_relevance[i] / np.log2(i + 2) for i in range(10)])
            if ideal_dcg == 0:
                ndcg = 0
            else:
                ndcg = dcg / ideal_dcg
            # print(ndcg)
            ndcgs.append(ndcg)

    print(ndcgs)
    sum1 = 0
    count1 = 0
    for p in ndcgs:
        sum1 += p
        if p != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(ndcgs)


def ndcg_post_processing_v2():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_bprmf.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    ndcgs = []
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()[:10]

            for j in range(len(true_relevance)):
                if true_relevance[j] > 0:
                    true_relevance[j] = 1

            true_relevance_sorted = [x for _, x in sorted(zip(true_relevance, true_relevance), reverse=True)]
            ideal_dcg = sum([true_relevance_sorted[i] / np.log2(i + 2) for i in range(10)])
            dcg = sum([true_relevance[i] / np.log2(i + 2) for i in range(10)])
            if ideal_dcg == 0:
                ndcg = 0
            else:
                ndcg = dcg / ideal_dcg
            # print(ndcg)
            ndcgs.append(ndcg)
    print(ndcgs)
    sum1 = 0
    count1 = 0
    for p in ndcgs:
        sum1 += p
        if p != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(ndcgs)


def mean_reciprocal_rank_v2():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_kgin.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    mrrs = []
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            # result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()[:10]

            mrr = 0
            for j in range(len(true_relevance)):
                relevance = true_relevance[j]
                if relevance != 0:
                    mrr = 1 / (j+1)
                    break
            # print(mrr)
            mrrs.append(mrr)
    print(mrrs)
    sum1 = 0
    count1 = 0
    for m in mrrs:
        sum1 += m
        if m != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(mrrs)


def mean_reciprocal_rank_post_v2():
    df_users = pd.read_csv(rec_dir + "gold_users.csv", index_col=False)
    users = df_users["user_id"].tolist()
    df_evaluate = pd.read_csv(exp_dir + "evaluate_info_kgin.csv", header=None, index_col=False)
    df_evaluate.columns = ["user_id", "movie_id", "true_relevance", "score", "persuade_degree"]

    mrrs = []
    for i in range(len(users)):
        uid = users[i]
        result = df_evaluate.query("user_id==" + str(uid))
        if not result.empty:
            result = result.sort_values('persuade_degree', ascending=False)
            true_relevance = result["true_relevance"].tolist()[:10]

            mrr = 0
            for j in range(len(true_relevance)):
                relevance = true_relevance[j]
                if relevance != 0:
                    mrr = 1 / (j+1)
                    break
            # print(mrr)
            mrrs.append(mrr)
    print(mrrs)
    sum1 = 0
    count1 = 0
    for m in mrrs:
        sum1 += m
        if m != 0:
            count1 += 1
    # return sum1 / count1
    return sum1 / len(mrrs)





