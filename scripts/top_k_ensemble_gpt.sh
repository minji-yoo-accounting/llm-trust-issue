#!/bin/bash

#set this in bash terminal
#export OPENAI_API_KEY=""
#echo $OPENAI_API_KEY


# prompt strategy = top-k
# sampling strategy = self-random ->  by setting NUM_ENSEMBLE to decide the number of samples we want to draw from a given question
# aggregator = consistency / avg-conf / pair-rank (all of them will be automatically computed in the same script)
PROMPT_TYPE="top_k"
SAMPLING_TYPE="self_random" 
NUM_ENSEMBLE=5 
CONFIDENCE_TYPE="${PROMPT_TYPE}_${SAMPLING_TYPE}_${NUM_ENSEMBLE}"



# TODO uncomment following lines to run on different settings
#############################################################

# DATASET_NAME="Financial_PhraseBank"
# MODEL_NAME="chatgpt"
# TASK_TYPE="multi_choice_qa"
# DATASET_PATH="C:/Users/minjiyoo/Desktop/llm-uncertainty/bank.csv"
# USE_COT=false # use cot or not
# TEMPERATURE=0.7
# TOP_K=3

DATASET_NAME="ReutersNews"
MODEL_NAME="chatgpt"
TASK_TYPE="multi_choice_qa"
DATASET_PATH="C:/Users/minjiyoo/Desktop/llm-uncertainty/articles.csv"
USE_COT=false # use cot or not
TEMPERATURE=0.7
TOP_K=3

#############################################################
# set time stamp to differentiate the output file
TIME_STAMPE=$(date "+%m-%d-%H-%M")

OUTPUT_DIR="final_output/$CONFIDENCE_TYPE/$MODEL_NAME/$DATASET_NAME"
RESULT_FILE="$OUTPUT_DIR/${DATASET_NAME}_${MODEL_NAME}_${TIME_STAMPE}.json"
USE_COT_FLAG=""

if [ "$USE_COT" = true ] ; then
    USE_COT_FLAG="--use_cot"
fi

python3 ../query_top_k.py \
   --dataset_name  $DATASET_NAME \
   --data_path $DATASET_PATH \
   --output_file  $RESULT_FILE \
   --model_name  $MODEL_NAME \
   --task_type  $TASK_TYPE  \
   --prompt_type $PROMPT_TYPE \
   --num_K $TOP_K \
   --sampling_type $SAMPLING_TYPE \
   --num_ensemble $NUM_ENSEMBLE \
   --temperature_for_ensemble $TEMPERATURE \
   $USE_COT_FLAG


# uncomment following lines to run test and visualization
python3 ../extract_answers.py \
   --input_file $RESULT_FILE \
   --model_name  $MODEL_NAME \
   --dataset_name  $DATASET_NAME \
   --task_type  $TASK_TYPE   \
   --prompt_type $PROMPT_TYPE \
   --num_K $TOP_K \
   --sampling_type $SAMPLING_TYPE \
   --num_ensemble $NUM_ENSEMBLE \
    $USE_COT_FLAG

RESULT_FILE_PROCESSED=$(echo $RESULT_FILE | sed 's/\.json$/_processed.json/')

python3 ../vis_aggregated_conf_top_k.py \
    --input_file $RESULT_FILE_PROCESSED \
    --model_name  $MODEL_NAME \
    --dataset_name  $DATASET_NAME \
    --task_type  $TASK_TYPE   \
    --prompt_type $PROMPT_TYPE  \
    --num_K $TOP_K \
    --sampling_type $SAMPLING_TYPE \
    --num_ensemble $NUM_ENSEMBLE \
    $USE_COT_FLAG    
