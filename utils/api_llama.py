# Ref: https://github.com/kojima-takeshi188/zero_shot_cot
# Ref: https://github.com/sylinrl/TruthfulQA/blob/main/truthfulqa/metrics.py
# Ref: https://github.com/sylinrl/TruthfulQA/blob/main/truthfulqa/utilities.py

import torch
from transformers import AutoTokenizer, pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the tokenizer and model using the pipeline method
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
text_generation_pipeline = pipeline(
    "text-generation",
    model=model_name,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)



def LlamaChatCompletion(prompt, use_sampling=True, temperature=0.6, top_p=0.9, repetition_penalty=1.2, max_token = max_token):
    # Generate the output with sampling, temperature, top_p, and repetition penalty
    sequences = text_generation_pipeline(
        prompt,
        do_sample=use_sampling,
        temperature=temperature if use_sampling else None,
        top_k=10 if use_sampling else None,
        top_p=top_p if use_sampling else None,
        repetition_penalty=repetition_penalty,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=max_token,
    )
    
    # Extract and return the generated text
    return [seq['generated_text'] for seq in sequences]
