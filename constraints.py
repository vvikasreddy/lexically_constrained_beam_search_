# -*- coding: utf-8 -*-
"""constraints.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/vvikasreddy/lexically_constrained_beam_search_/blob/main/constraints.ipynb
"""

!pip install datasets

# importing necessary libraries

from datasets import load_dataset
from collections import defaultdict
from tqdm import tqdm

# loading the wmt dataset, turkish to english

ds = load_dataset("wmt/wmt16", "tr-en")

def get_ngrams(src, n = 2, ):
  """
  The function returns the n_grams of length n, from the given sentence."""

  src = src.split(" ")
  src = [tuple(src[i:i+n]) for i in range(len(src) - n + 1)]
  return src

def constraints():

  """
  The function returns the """

  src_ngrams_count = defaultdict(int)
  tgt_ngrams_count = defaultdict(int)
  dict_pairs = defaultdict(int)

  dict_pairs_count = 0
  total_src_words = 0
  total_tgt_words = 0


  count = 0
  n_gram = 2
  for doc in tqdm(ds["train"]["translation"]):


    # get the src, and tgt
    src = doc["tr"]
    tgt = doc["en"]

    # get the ngrams, default n = 2
    src_ngrams = get_ngrams(src, n = n_gram)
    tgt_ngrams = get_ngrams(tgt, n = n_gram)


    # count the occurences of each of the ngram
    for tgt_ngram in tgt_ngrams:
      total_tgt_words += n_gram
      tgt_ngrams_count[tgt_ngram] += 1

    for src_ngram in src_ngrams:
      total_src_words += n_gram
      src_ngrams_count[src_ngram] += 1

    # # count the combined co-occurence of the ngram

    for src_ngram in src_ngrams:
      for tgt_ngram in tgt_ngrams:
        dict_pairs_count+= min(src_ngrams_count[src_ngram], tgt_ngrams_count[tgt_ngram])
        # dict_pairs[(src_ngram, tgt_ngram)] += min(src_ngrams_count[src_ngram], tgt_ngrams_count[tgt_ngram])


  return dict_pairs_count,  src_ngrams_count, tgt_ngrams_count, total_src_words, total_tgt_words

# dict_pairs_count, dicr_pairs, src_ngrams_count, tgt_ngrams_count, total_src_words, total_tgt_words =  constraints()

def get_count_dict_pairs(filtered_src, filtered_tgt, src_ngrams_count, tgt_ngrams_count):

  dict_pairs = defaultdict(int)

  count = 0
  for doc in tqdm(ds["train"]["translation"]):

    # get the src, and tgt
    src = doc["tr"]
    tgt = doc["en"]

    # get the ngrams, default n = 2
    src_ngrams = get_ngrams(src)
    tgt_ngrams = get_ngrams(tgt)

    # # count the combined co-occurence of the ngram

    for src_ngram in src_ngrams:
      if src_ngram not in filtered_src: continue
      for tgt_ngram in tgt_ngrams:

        if tgt_ngram not in filtered_tgt: continue
        dict_pairs[(src_ngram, tgt_ngram)] += min(src_ngrams_count[src_ngram], tgt_ngrams_count[tgt_ngram])

    # if count %1000 == 0:
    #   print(count)
    count += 1

  return dict_pairs
# dict_pairs =  get_count_dict_pairs()

import math

def calculate_pmi(dict_pairs_count, dict_pairs, src_ngrams_count, tgt_ngrams_count, total_tgt_words, total_src_words):
    ignored_count = 0
    pmi_dict = {}
    count = 0

    total_dict_pairs = dict_pairs_count

    for (src_ngram, tgt_ngram), count in tqdm(dict_pairs.items()):
        p_src_tgt = dict_pairs[(src_ngram, tgt_ngram)] / total_dict_pairs

        p_src = src_ngrams_count[src_ngram] / total_src_words
        p_tgt = tgt_ngrams_count[tgt_ngram] / total_tgt_words

        if p_src == 0 or p_tgt == 0:
          pmi = 0
        else:
          pmi = math.log2(p_src_tgt / (p_src * p_tgt))/ -math.log2(p_src_tgt)

        if pmi > 0.9:
          pmi_dict[(src_ngram, tgt_ngram)] = pmi
        else:
          ignored_count += 1

    return pmi_dict

def get_constraints():

# get the count and filtering if occurences is less than min_count, set 5

  dict_pairs_count, src_ngrams_count, tgt_ngrams_count, total_src_words, total_tgt_words =  constraints()
  min_count = 3
  # dict_pairs_count, dict_pairs, src_ngrams_count, tgt_ngrams_count, total_src_words, total_tgt_words


  filtered_src = {k: v for k, v in src_ngrams_count.items() if v >= min_count}
  filtered_tgt = {k: v for k, v in tgt_ngrams_count.items() if v >= min_count}

  dict_pairs =  get_count_dict_pairs( src_ngrams_count=src_ngrams_count, tgt_ngrams_count= tgt_ngrams_count, filtered_src=filtered_src, filtered_tgt=filtered_tgt)



  pmi_scores = calculate_pmi(dict_pairs_count, dict_pairs, filtered_src, filtered_tgt, total_tgt_words, total_src_words)


  # dictionary to only return the pair with max PMI value; since, there might be a different tgt value for the same src.
  max_pmi_dict = {}


  for (src, tgt), pmi_value in pmi_scores.items():
      if src not in max_pmi_dict:
          max_pmi_dict[src] = (tgt, pmi_value)
      elif pmi_value > max_pmi_dict[src][1]:
        max_pmi_dict[src] = (tgt, pmi_value)

  return max_pmi_dict

# pmi_scores = get_constraints()

# pmi_scores

# len(pmi_scores)

# max_entry = max(pmi_scores.items(), key=lambda x: x[1][1])
# print("Entry with max value:", max_entry)

