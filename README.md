How Much Should We Trust LLM-Based Measures for Accounting and Finance Research? 
==
Code repository for the paper "How Much Should We Trust LLM-Based Measures for Accounting and Finance Research?"

Paper: [Add SSRN Link]

Author: [Minji Yoo] (The Wharton School, University of Pennsylvania)

## 01 Abstract

This paper investigates the reliability of self-reported confidence scores from large language models (LLMs) in the context of accounting and finance research. Researchers often ask ChatGPT to provide confidence levels for their predictions and use these scores to measure the likelihood that a sample is correctly labeled. This study evaluates their reliability by examining: 1) how well LLMs' expressed confidence aligns with their actual accuracy (calibration), and 2) how effectively these models distinguish between correct and incorrect predictions (failure prediction). To address these questions, I conduct experiments using ChatGPT on sentiment analysis of financial text, a common task in accounting and finance research. The results show a large 40\% difference between the average accuracy of predictions and the self-reported confidence scores under popular prompt strategies, indicating significant overconfidence. The paper proposes alternative methods to mitigate this issue. A modified prompt strategy from artificial intelligence literature reduces the overconfidence gap to 19\%, while a fine-tuning approach that directly retrieves the probability of predicted labels from the model, instead of relying on self-reported confidence scores, effectively eliminates overconfidence. Furthermore, smaller non-generative LLMs, such as RoBERTa, do not exhibit the overconfidence problem and outperform prompted ChatGPT in both calibration and failure prediction when finetuned. Finally, the paper demonstrates how empirical analysis can be influenced by the methods used to obtain confidence scores.


[Under construction]
In case of Llama2 model, you need to specify do_sampling in llm_query_helper.py 

Finetuning ChatGPT and Llama2:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1efaeCj3tAxOXl8fn5pLT9j2PUR73UdAm?usp=sharing)

Finetuning RoBERTa and FinBERT:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1lVfRK2COCHEz1gdQ2fodA31wkNwJjIgL?usp=sharing)

Testing Finetuned models:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uQ9jc4SlK_zG892CMEY6Bvu9CZwZKrNb?usp=sharing)

Finetuned models can be found here: [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Profile-yellow)](https://huggingface.co/minjiyoo)
