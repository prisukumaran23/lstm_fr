
## LSTM - Gender Agreement
---
This repository contains the following:
1. Data sets for training and testing the LSTM language models
2. Syntactic evaluation sets 
    * [Number agreement](https://github.com/prisukumaran23/lstm_fr/tree/main/testsets/num_agr) taken from [Mueller et al. (2020)](https://aclanthology.org/2020.acl-main.490/)
    * [Gender agreement](https://github.com/prisukumaran23/lstm_fr/tree/main/testsets) 
3. Notes on model training and evaluation

### 1. Data Sets
---
* [Original French Corpus](https://github.com/prisukumaran23/lstm_fr/tree/main/data/original): From Mueller et al. (2020)
* [Reduced French Corpus](https://github.com/prisukumaran23/lstm_fr/tree/main/data) used in this work. [Script](https://github.com/prisukumaran23/lstm_fr/blob/main/make_clean_corpus.py) to clean the corpus. 

### 2. Syntactic Evaluation Sets
---
Number agreement datasets were taken from Mueller et al. (2020) to test our model's robustness and replicate findings.

Gender agreement evaluation sets contained noun-adjective and noun-passive-verb agreement phrases. Phrases were constructed by systematically varying 40 nouns, 15 adjectives/verbs, and 30
distractor phrases with up to 11 words, provided [here](https://github.com/prisukumaran23/lstm_fr/tree/main/utils_create). Each condition had two sub-conditions where the main noun was singular or plural. 

### 3. Model Training and Evaluation
---
We used the LSTM model and training/evalution code from [Gulordava et al. (2018)](https://github.com/facebookresearch/colorlessgreenRNNs) with minor modifications.
