import os
import statistics
import pandas as pd
data_dir = "Data/"
rec_dir = "Data/recommendations/"


def get_user_personality(user_id):
    personality_df = pd.read_csv(data_dir + "Personality/users_personality.csv", index_col=False)
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


def get_persuasion_profile(user_id):
    personality = get_user_personality(user_id)
    socialproof_score = commitment_score = authority_score = 0
    count = 0
    trait_weights = {
        0: {1: (4, 3, 1), -1: (5, 3, 1)},  # EXT
        1: {1: (4, 3, 2), -1: (3, 4, 1)},  # AGR
        2: {1: (3, 5, 2), -1: (3, 4, 1)},  # CON
        3: {1: (4, 3, 1), -1: (4, 1, 3)},  # NEU
        4: {1: (4, 3, 2), -1: (5, 3, 1)}   # OPN
    }

    for i, value in enumerate(personality):
        if value in trait_weights[i]:
            s, c, a = trait_weights[i][value]
            social += s
            commit += c
            authority += a
            count += 1

    socialproof_score = round(socialproof_score / count, 2)
    commitment_score = round(commitment_score / count, 2)
    authority_score = round(authority_score / count, 2)
    return socialproof_score, commitment_score, authority_score


def generate_explanations_for_recommendations(rec_filepath):
    df = pd.read_csv(rec_filepath, header=None, index_col=False)
    df.columns = ["uid", "iid", "rate"]

    output_path = os.path.join(data_dir, 'explanations.csv')
    results = []
    for _, row in df.iterrows():
        uid = str(row["uid"])
        iid = str(row["iid"])
        pred_rate = str(row["rate"])
        explanation, persuasiveness_degree, principle = explanation_generation(uid, iid)
        results.append({
            "user_id": uid,
            "movie_id": iid,
            "prediction_rate": pred_rate,
            "exp": str(explanation),
            "exp_type": str(principle),
            "persuade_degree": str(persuasiveness_degree)
        })

    exp_df = pd.DataFrame(results)
    exp_df.to_csv(output_path, mode='a', header=False, index=False)
    
