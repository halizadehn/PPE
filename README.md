# Persuasion-Aware Explanations for Recommended Items

<p align="justify">This repository contains the implementation of our proposed approach for generating persuasive explanations in recommender systems (RSs). Our method constructs a persuasion profile for each user and generates persuasion-aware explanations for items recommended by various RS baselines. These explanations are evaluated from an explainability perspective using metrics such as model fidelity. We also incorporate the persuasiveness degree of each explanation to re-rank the recommendation list and assess the impact on recommendation utility. Experimental results on a real-world movie recommendation dataset show that our approach effectively generates persuasive explanations while also improving the utility of the recommendations. </p>

## Dataset 

<p align="justify"> We use the publicly available <a href="https://github.com/sidooms/MovieTweetings">MovieTweetings</a> dataset. The dataset consists of three main files:

- **`users.dat`**  
  Maps internal user IDs to their actual Twitter IDs, enabling further user-level analysis such as personality trait extraction from tweets.

- **`items.dat`**  
  Contains information about the rated items (i.e., movies), including metadata such as genres.

- **`ratings.dat`**  
  Stores the extracted ratings in the format: `user_id, movie_id, rating, rating_timestamp`.  The ratings are scaled from **0 to 10**.
</p>
