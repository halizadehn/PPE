# Persuasion-Aware Explanations for Recommended Items

<p align="justify">This repository contains the implementation of our proposed approach for generating persuasive explanations in recommender systems (RSs). Our method constructs a persuasion profile for each user and generates persuasion-aware explanations for items recommended by various RS baselines. These explanations are evaluated from an explainability perspective using metrics such as model fidelity. We also incorporate the persuasiveness degree of each explanation to re-rank the recommendation list and assess the impact on recommendation utility. Experimental results on a real-world movie recommendation dataset show that our approach effectively generates persuasive explanations while also improving the utility of the recommendations. </p>

## Pipeline Overview
<img src="Figures/overview.png" />


## Dataset 

<p align="justify"> We use the publicly available <a href="https://github.com/sidooms/MovieTweetings">MovieTweetings</a> dataset. The dataset consists of three main files:

- **users.dat:** maps internal user IDs to their Twitter IDs, enabling further user-level analysis such as personality trait extraction from tweets.

- **items.dat:** contains information about the rated items (i.e., movies), including metadata such as genres.

- **ratings.dat:** stores the extracted ratings in the format: user_id, movie_id, rating, rating_timestamp. The ratings are scaled from 0 to 10.

  **Preprocessing**: First, we preprocessed the dataset by filtering out low frequency users and infrequent items (i.e., lower than 10). After that, we gathered users’ recent tweets from the past year using [tweepy](https://github.com/tweepy/tweepy). Users with fewer than 100 tweets were excluded. The dataset, after preprocessing, consists of 2, 291 users, 8, 080 movies, 160, 696 ratings, and 1, 013, 140
tweets.

  **Dataset statistics after preprocessing:**
<img src="Figures/dataset.JPG" />
</p>


## Recommednation models 
<div style="text-align: justify">
<p align="justify"> To demonstrate the model-agnostic nature of our explanation generation approach, we applied five RS baselines included two factorization models (Bayesian Personalized Ranking for Matrix Factorization (BPRMF) and Neural Factorization Machines (NFM)) and three knowledge-aware models (Collaborative Knowledge-based Embedding (CKE), Knowledge Graph Attention Network (KGAT) and Knowledge Graph-based Intent Network (KGIN)). 
  
- **KGIN:** This model combines various relationships within the knowledge graph to understand the intent behind interactions between users and items. The code is available at <a href="https://github.com/huangtinglin/Knowledge_Graph_based_Intent_Network">https://github.com/huangtinglin/Knowledge_Graph_based_Intent_Network</a>.

- **KGAT:** This model build a collaborative knowledge graph and employs an attentive aggregation mechanism to generate representations for users and items. The code is available at <a href="https://github.com/xiangwang1223/knowledge_graph_attention_network">https://github.com/xiangwang1223/knowledge_graph_attention_network</a>.

- **CKE:** This approach combines a collaborative filter (CF) module with knowledge embeddings of items derived from TransR. 

- **NFM** This method is a state-of-the-art neural network-based factorization model. The code is available at <a href="https://github.com/hexiangnan/neural_factorization_machine">https://github.com/hexiangnan/neural_factorization_machine</a>. 

- **BPRMF** Bayesian Personalized Ranking is a widely used collaborative filtering method that only considers the user-item interactions, without utilizing any external knowledge about the users or items. 
</p>
</div>

## Code Structure
This section provides an overview of the key files in the repository and their respective roles.

- **[personality_assessment.py:](Code/personality_assessment.py)** This file implements the assessment of users' personality traits based on their textual content, using the <a href="https://www.nature.com/articles/srep04761">vectorial semantics approach</a> proposed by Neuman and Cohen. In this approach, a set of vectors is created using a limited number of adjectives that, based on theoretical and/or empirical knowledge, reflect the core dimensions of personality traits. By leveraging context-free word embeddings, the semantic similarity between these vectors and the users' textual data (i.e., tweets) is computed. These similarity scores are then used to quantify the presence of specific personality traits in the text.

- **[persuasive_explanation_generation.py](Code/persuasive_explanation_generation.py):** This file implements the generation of persuasive explanations, as described in Algorithm 1 of the paper. The approach focuses on creating explanations that align with the most persuasive principles found in the user's persuasion profile.
 
- **[explanation_baselines.py](Code/explanation_baselines.py):** This file implements three distinct baselines for explanation generation: rating-based, feature-based, and award-based. Each approach leverages a unique method to generate explanations for recommended items, offering diverse strategies for comparison and evaluation.

- **[metrics.py](Code/metrics.py):** This file implements evaluation metrics, including model fidelity. Additionally, it introduces a new metric, persuasion-based fidelity, which takes into account not only the presence of an explanation but also its persuasive effectiveness in influencing users.


## Results
<p align="justify"> To assess the impact of the re-ordering approach on the upper segments of the recommendation list, in addition to the results reported in the paper for K=10, we present results for K=3 and K=5 in Figure 1. A careful examination of these figures reveals consistent improvements, aligning with the findings for K=10. Specifically, for K=3, the re-ordering approach led to an average NDCG improvement of approximately 13.36% and an average MRR improvement of around 14.72%. For K=5, the improvements were slightly smaller but still notable, with an average NDCG improvement of about 8.22% and an average MRR improvement of approximately 11.54%. </p>
  
<img src="Figures/re-ordering impact across different K.JPG" width="700"/>
<p style="font-size:8px;"><strong><em>Figure 1: Impact of the proposed re-ranking approach on recommendation utility</em></strong></p>

<p align="justify"> Table 1 and Table 2 present the model fidelity and persuasion-based fidelity for the top-3 and top-5 recommendations, evaluated across various explanation styles. The results in these tables align consistently with those for k=10, as reported in the paper, thereby demonstrating the generalizability of the observed findings across different recommendation sets.
</p>
<img src="Figures/fidelity across different K.JPG" width="800"/>

**Note:** Based on results, knowledge-aware RSs like CKE, KGAT, and KGIN consistently exhibit higher model fidelity than other RS baselines such as BPRMF and NFM across different values of K in the feature-based style. This observation aligns with the fact that these RSs incorporate item features, such as actor, director, and genre, into their recommendation generation algorithms. This integration further reinforces the support for generating explanations based on these features for recommended items.


## Future Works
- <p align="justify">The findings presented in this paper are derived from an extensive analysis conducted on a dataset specifically focused on the Movie domain. While the insights and implications drawn from our study may have broader relevance and applicability across different domains and contexts, as future work, we intend to undertake further investigations to validate and generalize our results. </p>
- <p align="justify">As another direction for future work, we aim to enhance the technical depth of our approach. For example, we plan to extend our framework by incorporating more advanced personalization models, such as transformer-based architectures that can jointly learn user preferences and persuasive tendencies in an end-to-end manner. Additionally, we intend to expand our framework to support multi-objective optimization—balancing recommendation accuracy and persuasive effectiveness—which would significantly strengthen the model’s technical sophistication and practical utility.</p>
- <p align="justify">Another important direction for future work is conducting real-user evaluations to complement our current findings based on historical data. While offline experiments offer controlled and scalable evaluation, they have inherent limitations in capturing users’ real-time reactions and behavioral changes. To address this, we plan to design user studies that test the persuasive impact and perceived relevance of explanations in live settings. Such evaluations would provide deeper insights into the effectiveness of our approach in practical, user-facing environments. </p>

## Citation
Havva Alizadeh Noughabi, Behshid Behkamal, Fattane Zarrinkalam, Mohsen Kahani, "Personalized Persuasion-Aware Explanations in Recommender Systems", 19th ACM Conference on Recommender Systems (RecSys 2025).

