# 🌟 Lexically Constrained Beam Search  

## 📖 Overview  
This project explores **lexically constrained beam search**, inspired by the algorithm presented in **Hokamp and Liu’s paper**. The goal is to enhance machine translation by incorporating **contextually relevant constraints** to guide the translation process. This method ensures that specific words or phrases appear in the output while keeping the model parameters unchanged.  

- **Language Pair**: Turkish → English  
- **Dataset**: WMT (Turkish-English)  
- **Model**: [MarianMT](https://huggingface.co/docs/transformers/model_doc/marian)  

---

## 🧠 Algorithm  
Beam search improves text generation by pursuing the top **k probabilities** instead of choosing the highest probability word at each step. The use of constraints helps generate contextually relevant translations from **content-relevant constraints**.

1. **Dynamic Programming Framework**: Sequence generation is represented on a grid where the x-axis corresponds to sequence length (time steps), and the y-axis represents constraints covered so far.
2. **Constraint Handling**: Nodes can advance constraints by either generating new constraints (dashed lines) or using model predictions (horizontal lines).
3. **Beam Search Optimization**: At each node, sequences are expanded, and the top-k beams are retained, ensuring efficient exploration of possibilities.
4. **Beam Parameters**: A beam size (k) of 4 and a maximum sequence length of 23 are used to limit computational costs while maintaining quality.
5. **Selection Strategy**: To determine the top-k beams for each node, sequences are ranked based on coverage and probability, adhering to the constraints efficiently.

---

![Visual Algorithm Explanation](images/Visual_explanation_of_algorithm.png)  
**Fig. 1**: Visualization of decoding (adapted from [Hokamp and Liu](https://aclanthology.org/P17-1141.pdf)).  

---

### Example:  
To calculate top-k beams for a node `(5,2)`:  
- Add constraints from `(4,1)` (vertical dashed line) → k beams.  
- Generate sequences from `(4,2)` → k × k beams.  
- Retain the top-k sequences for `(5,2)`.

![Example Generating Next k Beams](images/example_generating_next_k_beams.png)  
**Fig. 2**: Beam search process explained.  

---

## ⚙️ Implementation  

### 🔧 Steps:  
1. **Constraint Extraction**:  
   - Constraints were extracted from bigrams in a corpus of 207,000 translation pairs, yielding 570 pairs with an NPMI score > 0.9; experimenting with lower thresholds increased quantity but reduced quality. Extracting constraints from ngrams of length 3–5 was deemed computationally expensive and likely insignificant in improving results.

   - Hokamp and Liu's use of a post-editing corpus with a specific context, unlike common datasets like WMT, enabled them to extract more meaningful constraints, highlighting challenges in evaluation and metric improvement with limited constraints in a general dataset.

2. **Beam Search Algorithm**:  
   - The Beam search algorithm can be implemented using Dynamic programming approach (bottom-up) as presented in the Fig 1.  
   - Validated using ~1000 translations with constrained and unconstrained output.

---

## 📊 Evaluation  

### 🔍 Metrics:  
- **BLEU Score**: Measures n-gram overlap between predicted and target translations.  
  - **With Constraints**: 22.82  
  - **Without Constraints**: 35.93  

| **Metric**  | **With Constraints** | **Without Constraints** |  
|-------------|-----------------------|--------------------------|  
| BLEU        | 22.82                | 35.93                   |  
| ROUGE-1     | 0.4788               | 0.6108                  |  
| ROUGE-2     | 0.2732               | 0.4387                  |  
| ROUGE-L     | 0.4054               | 0.5602                  |  

---

### ✏️ Observations:  
- BLEU and ROUGE scores were lower with constraints, suggesting they reduced fluency in some translations.  
- Constraints improved relevance but occasionally forced unnatural phrasing.  
- **Sanity Tests** confirmed the presence of constraints in output translations.  

---

## 📝 Summary  
- **Dataset Limitations**: The WMT dataset’s lack of domain specificity hindered the generation of impactful constraints.  
- **Key Finding**: Domain-specific datasets (e.g., Autodesk post-editing corpus) could significantly improve constraint quality.  
- **Outcome**: Successfully implemented constrained beam search, demonstrating its potential for translation tasks with proper datasets.  

---

## 📚 References  
1. [Marian MT model](https://huggingface.co/docs/transformers/model_doc/marian)  
2. [Code to get the logits](https://huggingface.co/docs/transformers/main_classes/output)  
3. [BOS and EOS tokens](https://huggingface.co/docs/transformers/main_classes/configuration#transformers.PretrainedConfig.decoder_start_token_id)  
4. [Torch top-k values](https://pytorch.org/docs/stable/generated/torch.topk.html)  
5. [Hokamp and Liu Paper](https://arxiv.org/pdf/1704.07138)  
6. [BLEU score evaluation](https://www.nltk.org/api/nltk.translate.bleu_score.html)  
7. [ROUGE score evaluation](https://huggingface.co/spaces/evaluate-metric/rouge/blob/main/README.md)  
