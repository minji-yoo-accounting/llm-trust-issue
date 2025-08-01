import os, pdb
from openai import OpenAI
from utils.api_llama import LlamaChatCompletion
                

#calculate_result_per_question('vicuna', 'a', 'a', {}, {}, {}, 'hint0', 'multi', False)
def calculate_result_per_question(model_name, question, prompt, final_result, error_dataset, qa_dataset, hint_type, task_type, use_cot, temperature=0.0):
    """
    - final_result is used to record the result of each question
    - error_dataset is used to record the error message of each question, if the error occurs
    - hint_type is used for record the hint type, e.g. hint0, hint1, hint2, hint3, hint4; if hint is not used, then hint_type is 'hint0'
    - use_cot is used to indicate whether to use cot or not
    
    return:
        final_result: updated final_result
        error_dataset: updated error_dataset
    """
    # uncomment only for gpt models
    client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],  # this is also the default, it can be omitted
)

    # run model api and get response
    max_tokens = 2000 if use_cot else 400
    max_req_count = 3
    req_success = False
    while not req_success and max_req_count > 0:
        try:
            if model_name.lower() == 'chatgpt':
                response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                            messages=[{'role':'user','content':prompt}],									
                                            temperature = temperature,
                                        max_tokens=max_tokens)
                print(response)
                orginal_anser = response.choices[0].message.content
                
            elif model_name.lower() == 'chatgpt-0301':
                response = client.chat.completions.create(model="gpt-3.5-turbo-0301",
                                            messages=[{'role':'user','content':prompt}],									
                                            temperature = temperature,
                                        max_tokens=max_tokens)
        
                orginal_anser = response['choices'][0]['message']['content']
                
            elif model_name.lower() == 'chatgpt-0613':
                response = client.chat.completions.create(model="gpt-3.5-turbo-0613",
                                            messages=[{'role':'user','content':prompt}],									
                                            temperature = temperature,
                                        max_tokens=max_tokens)
        
                orginal_anser = response['choices'][0]['message']['content']

            elif model_name.lower() == 'gpt3':
                response = client.chat.completions.create(model='text-davinci-003',
                                                    prompt=prompt,
                                                    temperature=temperature,
                                                    max_tokens=max_tokens
                                                    )    
                candidates = response["choices"]
                orginal_anser = [candidate["text"] for candidate in candidates][0]
            
            elif model_name.lower()  == 'gpt4':
                response = client.chat.completions.create(model="gpt-4",  messages=[{'role':'user','content':prompt}], temperature=temperature, max_tokens=max_tokens)
                orginal_anser = response["choices"][0]["message"]["content"]
                
            elif model_name.lower()  == 'o4-mini':
                response = client.chat.completions.create(model="o4-mini", reasoning_effort="medium", messages=[{"role": "user","content": prompt}])
                orginal_anser = response.choices[0].message.content
            
            elif model_name.lower() == 'vicuna':
                from utils.api_local import VicunaChatCompletion
                orginal_anser = VicunaChatCompletion(prompt)
                
            elif model_name.lower() == 'llama_2_7b_chat_hf':
                use_sampling = True # single prompting: False / ensemble: True 
                orginal_anser = LlamaChatCompletion(prompt, max_tokens=max_tokens)
                
                
            else:
                raise ValueError(f"{model_name} not supported")            
            
        
            dict_value = {'hint_response': orginal_anser, 'real_answer':qa_dataset[question]}
            final_result[question][hint_type] = dict_value
            
            print(dict_value)
            print('||||||||||||||||||||||||||\n\n')
            req_success = True
        
        except Exception as e:
            print(e)
            print(f"max_req_count: {max_req_count}")
            if max_req_count > 0:
                max_req_count -= 1
            else:
                if question not in error_dataset:
                    error_dataset[question] = {}
                error_dataset[question][hint_type] = {'error_message': str(e), 'real_answer':qa_dataset[question], 'used_prompt': prompt}

    return final_result, error_dataset
