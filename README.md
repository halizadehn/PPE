# Persuasion-Aware Explanations for Recommended Items

<p align="justify">This repository contains the implementation of our proposed approach for generating persuasive explanations in recommender systems (RSs). Our method constructs a persuasion profile for each user and generates persuasion-aware explanations for items recommended by various RS baselines. These explanations are evaluated from an explainability perspective using metrics such as model fidelity. We also incorporate the persuasiveness degree of each explanation to re-rank the recommendation list and assess the impact on recommendation utility. Experimental results on a real-world movie recommendation dataset show that our approach effectively generates persuasive explanations while also improving the utility of the recommendations. </p>

## Dataset 

<p align="justify"> We use the publicly available <a href="https://github.com/sidooms/MovieTweetings">MovieTweetings</a> dataset. The dataset consists of three main files:

- **users.dat:** maps internal user IDs to their Twitter IDs, enabling further user-level analysis such as personality trait extraction from tweets.

- **items.dat:** contains information about the rated items (i.e., movies), including metadata such as genres.

- **ratings.dat:** stores the extracted ratings in the format: user_id, movie_id, rating, rating_timestamp. The ratings are scaled from 0 to 10.
  
</p>

## Recommednation models 

<p align="justify"> To demonstrate the model-agnostic nature of our explanation generation approach, we applied five RS baselines included two factorization models (Bayesian Personalized Ranking for Matrix Factorization (BPRMF) and Neural Factorization Machines (NFM)) and three knowledge-aware models (Collaborative Knowledge-based Embedding (CKE), Knowledge Graph Attention Network (KGAT) and Knowledge Graph-based Intent Network (KGIN)). 
  
- **KGIN:** This model combines various relationships within the knowledge graph to understand the intent behind interactions between users and items. The code is available at https://github.com/huangtinglin/Knowledge_Graph_based_Intent_Network.

- **KGAT:** This model build a collaborative knowledge graph and employs an attentive aggregation mechanism to generate representations for users and items. The code is available at https://github.com/xiangwang1223/knowledge_graph_attention_network.

- **CKE:** This approach combines a collaborative filter (CF) module with knowledge embeddings of items derived from TransR. 

- **NFM** This method is a state-of-the-art neural network-based factorization model. The code is available at https://github.com/hexiangnan/neural_factorization_machine. 

- **BPRMF** Bayesian Personalized Ranking is a widely used collaborative filtering method that only considers the user-item interactions, without utilizing any external knowledge about the users or items. 

</p>

## Code Structure
<p align="justify"> This section outlines the main files in the repository and their specific roles. 

- **personality_assessment.py:** This file implements the assessment of users' personality traits based on their textual content, using the [vectorial semantics approach](https://www.nature.com/articles/srep04761) proposed by Neuman and Cohen. In this approach, a set of vectors is created using a limited number of adjectives that, based on theoretical and/or empirical knowledge, reflect the core dimensions of personality traits. By leveraging context-free word embeddings, the semantic similarity between these vectors and the users' textual data (i.e., tweets) is computed. These similarity scores are then used to quantify the presence of specific personality traits in the text.


- **persuasive_explanation_generation.py** This approach.
 
- **explanation_baselines.py** This approach.

- **metrics.py** This approach.
  
</p>

## Evaluation
insert figures and tables for different K


