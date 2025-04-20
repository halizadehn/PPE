import os
import statistics
import pandas as pd
data_dir = "Data/"
rec_dir = "Data/recommendations/"

 
def rating_based_explanation(user_id, movie_id):
    mid = id_to_imdb_id(movie_id)
    ratings_df = pd.read_csv(data_dir + 'IMDB/ratings.csv', index_col=False)
    result = ratings_df.query('tconst == "%s"' % mid)
    if not result.empty:
        avg_rate = result["averageRating"].tolist()[0]
        if avg_rate >= 8:
            return avg_rate, persuasiveness_degree
    return None, 0


def feature_based_explanation(user_id, movie_id):
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


def award_based_explanation(user_id, movie_id):
    oscar_df = pd.read_csv(data_dir + 'IMDB/the_oscar_award.csv', index_col=False)
    movie_name = get_movie_name(movie_id)
    result = oscar_df.query('film == "%s"' % movie_name)
    if result.empty:
        return None, 0
    winners = result[result["winner"] == True]
    if winners.empty:
        return None, 0
    return len(winners), persuasiveness_degree


def generate_explanations_for_recommendations(rec_filepath):
    df = pd.read_csv(rec_filepath, header=None, index_col=False)
    df.columns = ["uid", "iid", "rate"]

    output_path = os.path.join(data_dir, 'feature_based_explanations.csv')
    results = []
    for _, row in df.iterrows():
        uid = str(row["uid"])
        iid = str(row["iid"])
        pred_rate = str(row["rate"])
        explanation = feature_based_explanation(uid, iid)
        results.append({
            "user_id": uid,
            "movie_id": iid,
            "prediction_rate": pred_rate,
            "exp": str(explanation),
        })

    exp_df = pd.DataFrame(results)
    exp_df.to_csv(output_path, mode='a', header=False, index=False)
    
