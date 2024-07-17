# Ref: https://github.com/kojima-takeshi188/zero_shot_cot
# Ref: https://github.com/sylinrl/TruthfulQA/blob/main/truthfulqa/metrics.py
# Ref: https://github.com/sylinrl/TruthfulQA/blob/main/truthfulqa/utilities.py

import re, pdb
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the tokenizer and model
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

def LlamaChatCompletion(model_name, prompt, max_tokens):
    
    # Tokenize the input prompt
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    # Generate the output
    outputs = model.generate(
        input_ids=input_ids,
        max_new_tokens=max_tokens,
        return_dict_in_generate=True,
        output_scores=False,
        output_hidden_states=False
    )

    # Decode the output
    decoded_outputs = tokenizer.batch_decode(outputs.sequences, skip_special_tokens=True)
    
    return decoded_outputs
    
