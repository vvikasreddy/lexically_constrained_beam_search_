# Lexically Constrained Beam Search for Machine Translation

## Overview
This project explores the concept of lexically constrained beam search, based on the algorithm presented in Hokamp and Liu’s paper. The main goal is to improve the quality of machine translation by incorporating contextually relevant constraints, which guide the model’s translation process. This approach allows for more accurate translations by forcing content-relevant words into the output without changing model parameters.

The algorithm is applied to machine translation from Turkish (source language) to English (target language) using the WMT dataset and the MarianMT model.

## Algorithm

In text generation, always choosing the next word with highest probability might not produce optimal results. However, pursuing k best probabilities at each time step is a good idea to generate better translations. We can force content-relevant words (constraints) in the machine output using beam search to get contextually relevant translations. I am applying this algorithm to aid machine translation from Turkish(source language) to English(target language). The dataset utilized is WMT (Turkish-English), and the model employed is MarianMT.

![Image Description](images/Visual_explanation_of_algorithm.png)
 
### Fig 1:  visualization of the decoding process (reference: ![Hokamp and liu Paper](https://aclanthology.org/P17-1141.pdf))

The algorithm can be better explained using the above image, x axis contains the sequence length or time steps, y axis indicate the constraints covered so far. It can be viewed as a dynamic programming problem, which can be solved using a bottom-up approach. Meaning the values for the top nodes, can be filled by using the bottom nodes, each node holds k best values. The values for each node can be filled by generating new constraints (indicated by dashed lines) or continuing from model predictions (horizontal line). From the generated sequences, k best values are chosen to fill the current node. Hokamp and Liu also provide an algorithm to implement the model, which I am using as a reference.

For example, as seen in Fig. 1 and Fig. 2:
(x,y) -> x represents the timestep, y represents the constraints covered. To obtain the top k beams for node (5,2), we add a constraint to all sequences generated from node (4,1) (shown by the vertical dashed line), this results in k beams. For each of the k beams at (4,2) corresponding k beams are generated, i.e k x k. Altogether, this process creates approximately k × k beams from (4,2) and k beams from (4,1), resulting in k × k + k sequences. From this set, we then select only the k best sequences.

Note: we only add a constraint to all the sequences going from (4,1) to (5,2), resulting in k beams. K used for the beam search algorithm is 4. Due to computational constraints, I capped the maximum sequence length to 23, and used the beam size ‘k’ of length 4.

![example of generating next k beams. (k = 3](images/example_generating_next_k_beams.png)

### Fig 2:  visualization of the decoding process (reference: ![Hokamp and liu Paper](https://aclanthology.org/P17-1141.pdf))

## Implementation:
I have followed the algorithm presented in the paper by Hokamp and Liu. While it was time-consuming to implement, it was achievable.

The implementation is divided into two phases:
### I. Extracting the constraints as specified in the paper by Hokamp and Liu.
### II. Developing the beam search algorithm. (as discussed in Algorithm section)

Since beam search is computationally expensive, I validated the algorithm using approximately 1000 translations, matching the size of the validation set. Not all Turkish sentences have associated constraints, so I selected Turkish texts that appeared to have relevant constraints.

### (I) Extracting the constraints
Constraints need to be extracted from the training data so they can later be applied to new, unseen data. The main idea is to find pairs that appear together frequently. For these pairs, we select candidates with a Normalized Pointwise Mutual Information (NPMI) score greater than
0.9. Candidates whose occurrence is less than 3 are removed. 

For ex : let x be a source sentence, y be a translated sentence, p(x,y) -> probability of joint occurrence, among all bigrams, p(x) and p(y) represent probabilities of occurrence among all bigrams in source and target language respectively. and h(x,y) = -log(p(x,y)).

I have extracted constraints from bigrams (length 2). From a corpus of 207,000 translation pairs, I was able to extract 570 pairs, only pairs with NPMI score greater than 0.9 were chosen. I have also experimented with lowering the NPMI threshold, which resulted in more constraints but reduced
quality. I doubt the number of constraints would be significant even if I extract from ngrams length 3-5 and it is also computationally expensive. Hokamp and Liu mentioned they did not use common datasets like wmt, but used post-editing corpus of auto-desk, because the corpus revolves behind a particular context, they might extract a good chunk of constraints. This problem also exists during the evaluation phase; with limited constraints, there is minimal improvement in the metrics.

## Evaluation:
I have conducted visual inspection of the constraints generated, which suggests a fair correlation. Sanity tests were conducted to evaluate the generated beams and also verified that the constraints appeared in the translations. 

The BLEU score is used to evaluate the predictions. Two types of translations were generated: with forced constraints and without constraints. The BLEU score is as follows 22.82 and 35.93 respectively. Weightage was only given to n-grams of lengths 1 and 2, while others were ignored, as the constraints were generated using n-grams of length 2. BLEU measures the overlap between n-grams of the predicted and target translations. The higher score indicates higher similarity and translation quality. However, there are cases where BLEU might fall short—for example, if the model generates synonymous translations, resulting in a lower score, or if constraints are included but form sentences that lack grammatical sense.

ROUGE-1, ROUGE-2, and ROUGE-L scores were also calculated; they measure the overlap of n-grams of length 1, length 2, and the longest common subsequence, respectively. The scores with constraints are as follows: ROUGE-1: 0.4788, ROUGE-2: 0.2732, and ROUGE-L: 0.4054. Without constraints, the scores are higher, with ROUGE-1: 0.6108, ROUGE-2: 0.4387, and ROUGE-L: 0.5602.

## Summary:
Since the WMT dataset is not domain-specific, the constraints generated did not significantly enhance the meaning of the translations. Even Hokamp and Liu mentioned that they did not use WMT for their analysis, which may explain why the added constraints did not improve the results in this case, in fact, constraints reduced the quality by forcing constraints into the translations. This approach can be applied to any dataset, however using a domain-specific one would likely yield more meaningful improvements. Overall, the project successfully incorporates constraints into the generation process, but a more focused dataset could improve its effectiveness.

## References

1. [Marian MT model](https://huggingface.co/docs/transformers/model_doc/marian)
2. [Code to get the logits](https://huggingface.co/docs/transformers/main_classes/output)
3. [To get the BOS and EOS tokens](https://huggingface.co/docs/transformers/main_classes/configuration#transformers.PretrainedConfig.decoder_start_token_id)
4. [Get top-k values](https://pytorch.org/docs/stable/generated/torch.topk.html)
5. [Hokamp and Liu paper: Lexically Constrained Decoding for Sequence Generation Using Grid Beam Search](https://arxiv.org/pdf/1704.07138)
6. [BLEU score evaluation](https://www.nltk.org/api/nltk.translate.bleu_score.html)
7. [ROUGE score evaluation](https://huggingface.co/spaces/evaluate-metric/rouge/blob/main/README.md)
