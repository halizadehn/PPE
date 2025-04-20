import os
import statistics
import pandas as pd
data_dir = "Data/"
rec_dir = "Data/recommendations/"

personality_df = pd.read_csv(data_dir + "Personality/users_personality.csv", index_col=False)


def get_user_personality(user_id):
    result = personality_df.query("user_id==" + str(user_id))
    personality = result.iloc[0].tolist()[1:]
    return personality
 

def explanation_generation(user_id, movie_id):
    scores = {
        "socialproof_score": get_persuasion_profile(user_id)[0],
        "commitment_score": get_persuasion_profile(user_id)[1],
        "authority_score": get_persuasion_profile(user_id)[2]
    }

    explanation_funcs = {
        "socialproof": socialproof_explanation_generation,
        "commitment": commitment_explanation_generation,
        "authority": authority_explanation_generation
    }

    sorted_types = sorted(scores, key=scores.get, reverse=True)
    
    for main_type in sorted_types:
        expl, degree = explanation_funcs[main_type](user_id, movie_id, scores[main_type])
        if expl != None:
            return expl, degree, main_type

    return None, 0, None


def socialproof_explanation_generation(user_id, movie_id, persuasiveness_degree):
    mid = id_to_imdb_id(movie_id)
    ratings_df = pd.read_csv(Data_dir + 'IMDB/ratings.csv', index_col=False)
    result = ratings_df.query('tconst == "%s"' % mid)
    if not result.empty:
        avg_rate = result["averageRating"].tolist()[0]
        if avg_rate >= 8:
            return avg_rate, persuasiveness_degree
    return None, 0


def commitment_explanation_generation(user_id, movie_id, persuasiveness_degree):
    movie_genres = get_genres(movie_id)
    user_genres = get_user_interested_genres(user_id)
    num_movie_genres = len(movie_genres)
    num_user_genres = len(user_genres)
    total_overlap_score = 0
    for genre in movie_genres:
        matches = 0
        for user_genre in user_genres:
            if genre in user_genre:
                matches += 1
        total_overlap_score += matches / num_user_genres
    average_score = total_overlap_score / num_movie_genres
    average_score = round(average_score, 2)
    if average_score >= 0.3:
        return average_score, persuasiveness_degree

    director = get_director_movie(movie_id)
    user_directors = get_user_interested_directors(user_id)
    match_count = user_directors.count(director)
    match_ratio = round(match_count / len(user_directors), 2)
    if match_ratio > 0.3:
        return match_ratio, persuasiveness_degree

    actors = get_actors_movie(movie_id)
    user_actors = get_user_interested_actors(user_id)
    actor_counts = [user_actors.count(actor) for actor in actors]
    max_ratio = round(max(actor_counts) / len(user_actors), 2)
    if max_ratio > 0.3:
        return max_ratio, persuade_weight

    return None, 0


def authority_explanation_generation(user_id, movie_id, persuasiveness_degree):
    oscar_df = pd.read_csv(data_dir + 'IMDB/the_oscar_award.csv', index_col=False)
    movie_name = get_movie_name(movie_id)
    result = oscar_df.query('film == "%s"' % movie_name)
    if result.empty:
        return None, 0
    winners = result[result["winner"] == True]
    if winners.empty:
        return None, 0
    return len(winners), persuasiveness_degree


def convert_id_to_imdb_id(id):
    id = str(id)
    zero_count = 7 - len(id)
    zero = ""
    for i in range(zero_count):
        zero += "0"
    return "tt" + zero + id


def explanation_generation_for_recommendations():
    df = pd.read_csv(rec_dir + 'kgin_top_10.csv', header=None, index_col=False)
    df.columns = ["uid", "iid", "rate"]
    exp_df = pd.DataFrame()
    for i in range(len(df)):
        uid = str(df.loc[i, "uid"])
        iid = str(df.loc[i, "iid"])
        pred_rate = str(df.loc[i, "rate"])
        exp, persuade_weight, exp_type = explanation_generation(uid, iid)
        exp_df.loc[0, "user_id"] = str(uid)
        exp_df.loc[0, "movie_id"] = str(iid)
        exp_df.loc[0, "prediction_rate"] = str(pred_rate)
        exp_df.loc[0, "exp"] = str(exp)
        exp_df.loc[0, "exp_type"] = str(exp_type)
        exp_df.loc[0, "persuade_degree"] = str(persuade_weight)
        exp_df.to_csv(os.path.join(exp_dir + 'explanation_kgin.csv'), mode='a', header=None, index=False)


def write_persuasion_profiles():
    new_df = pd.DataFrame()
    # df = pd.read_csv("data/users.dat", sep="::", engine='python', header=None)
    # df.columns = ["uid", "tw_id"]
    users_df = pd.read_csv('data/dataset/gold_users.csv', index_col=False)
    users = users_df["user_id"].tolist()
    for i in range(len(users)):
        uid = users[i]
        # result = df.query('uid == ' + str(uid))
        # tw_id = result['tw_id'].tolist()[0]
        new_df.loc[i, "user_id"] = str(uid)
        social, commit, authority = get_persuasion_profile(uid)
        new_df.loc[i, "social"] = social
        new_df.loc[i, "commit"] = commit
        new_df.loc[i, "authority"] = authority
    new_df.to_csv(os.path.join('data/persuasion_profiles.csv'), mode='w', index=False)

import matplotlib.pyplot as plt
def stats1():
    df = pd.read_csv('data/persuasion_profiles.csv', index_col=False)
    s = df["social"].tolist()
    c = df["commit"].tolist()
    a = df["authority"].tolist()

    print(max(s), min(s),max(c), min(c), max(a), min(a))
    sca = csa = sac = neutral = 0
    plt.boxplot(s)
    plt.show()
    plt.boxplot(c)
    plt.show()
    plt.boxplot(a)
    plt.show()
    # for i in range(len(df)):
    #     s = df.loc[i,"social"]
    #     c = df.loc[i, "commit"]
    #     a = df.loc[i, "authority"]
    #     if s == c:
    #         print(i)
    #     if c == a:
    #         print(i)
        # if s == c == a == 0:
        #     neutral += 1
        # elif s >= c and c >= a:
        #     sca += 1
        # elif c >= s and s >= a:
        #     csa += 1
        # elif s >= a and a >= c:
        #     sac += 1
    print(sca, csa, sac, neutral)


def get_persuasion_profile(user_id):
    personality = get_user_personality(user_id)
    social = commit = authority = 0
    count = 0
    if personality[0] == 1: #high_EXT
        social += 4
        commit += 3
        authority += 1
    if personality[0] == -1: #low_EXT
        social += 5
        commit += 3
        authority += 1
    if personality[1] == 1: #high_AGR
        social += 4
        commit += 3
        authority += 2
    if personality[1] == -1: #low_AGR
        social += 3
        commit += 4
        authority += 1
    if personality[2] == 1: #high_CON
        social += 3
        commit += 5
        authority += 2
    if personality[2] == -1: #low_CON
        social += 3
        commit += 4
        authority += 1
    if personality[3] == 1: #high_NEU
        social += 4
        commit += 3
        authority += 1
    if personality[3] == -1: #low_NEU
        social += 4
        commit += 1
        authority += 3
    if personality[4] == 1: #high_OPN
        social += 4
        commit += 3
        authority += 2
    if personality[4] == -1: #low_OPN
        social += 5
        commit += 3
        authority += 1

    social = float("{:.2f}".format(social / count))
    commit = float("{:.2f}".format(commit / count))
    authority = float("{:.2f}".format(authority / count))
    return social, commit, authority
  
# stats1()
# write_persuasion_profiles()
explanation_generation_for_recommendations()
# df = pd.read_csv(rec_dir + 'fm_top_10.csv', header=None, index_col=False)
# df.columns = ["uid", "iid", "rate"]
# x = df["iid"].tolist()
# x = list(dict.fromkeys(x))
# print(len(x))

