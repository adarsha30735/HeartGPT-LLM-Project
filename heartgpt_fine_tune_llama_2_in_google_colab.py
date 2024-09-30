# -*- coding: utf-8 -*-
"""HeartGPT_Fine_tune_Llama_2_in_Google_Colab (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EcOSO9PnLG84Br4iZqbqpo_HNSggOcHB

# Fine-tune Llama 2 in Google Colab
[GitHub Gist](https://gist.github.com/younesbelkada/9f7f75c94bdc1981c8ca5cc937d4a4da).
"""

!pip install -q accelerate==0.21.0 peft==0.4.0 bitsandbytes==0.40.2 transformers==4.31.0 trl==0.4.7

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)


from peft import LoraConfig, PeftModel
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

# The model that you want to train from the Hugging Face hub
model_name = "NousResearch/Llama-2-7b-chat-hf"

# The instruction dataset to use
dataset_name = "adarsha30735/datafood"

# Fine-tuned model name
new_model = "llama-2-7b-heartgpt"

################################################################################
# QLoRA parameters
################################################################################

# LoRA attention dimension
lora_r = 64

# Alpha parameter for LoRA scaling
lora_alpha = 16

# Dropout probability for LoRA layers
lora_dropout = 0.1

################################################################################
# bitsandbytes parameters
################################################################################

# Activate 4-bit precision base model loading
use_4bit = True

# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16"

# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4"

# Activate nested quantization for 4-bit base models (double quantization)
use_nested_quant = False

################################################################################
# TrainingArguments parameters
################################################################################

# Output directory where the model predictions and checkpoints will be stored
output_dir = "./results"

# Number of training epochs
num_train_epochs = 1

# Enable fp16/bf16 training (set bf16 to True with an A100)
fp16 = False
bf16 = False

# Batch size per GPU for training
per_device_train_batch_size = 4

# Batch size per GPU for evaluation
per_device_eval_batch_size = 4

# Number of update steps to accumulate the gradients for
gradient_accumulation_steps = 1

# Enable gradient checkpointing
gradient_checkpointing = True

# Maximum gradient normal (gradient clipping)
max_grad_norm = 0.3

# Initial learning rate (AdamW optimizer)
learning_rate = 2e-4

# Weight decay to apply to all layers except bias/LayerNorm weights
weight_decay = 0.001

# Optimizer to use
optim = "paged_adamw_32bit"

# Learning rate schedule
lr_scheduler_type = "cosine"

# Number of training steps (overrides num_train_epochs)
max_steps = -1

# Ratio of steps for a linear warmup (from 0 to learning rate)
warmup_ratio = 0.03

# Group sequences into batches with same length
# Saves memory and speeds up training considerably
group_by_length = True

# Save checkpoint every X updates steps
save_steps = 0

# Log every X updates steps
logging_steps = 25

################################################################################
# SFT parameters
################################################################################

# Maximum sequence length to use
max_seq_length = None

# Pack multiple short examples in the same input sequence to increase efficiency
packing = False

# Load the entire model on the GPU 0
device_map = {"": 0}

# Load dataset (you can process it here)
dataset = load_dataset(dataset_name, split="train")

# Load tokenizer and model with QLoRA configuration
compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
)

# Check GPU compatibility with bfloat16
if compute_dtype == torch.float16 and use_4bit:
    major, _ = torch.cuda.get_device_capability()
    if major >= 8:
        print("=" * 80)
        print("Your GPU supports bfloat16: accelerate training with bf16=True")
        print("=" * 80)

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map=device_map
)
model.config.use_cache = False
model.config.pretraining_tp = 1

# Load LLaMA tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training

# Load LoRA configuration
peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    bias="none",
    task_type="CAUSAL_LM",
)

# Set training parameters
training_arguments = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=num_train_epochs,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    optim=optim,
    save_steps=save_steps,
    logging_steps=logging_steps,
    learning_rate=learning_rate,
    weight_decay=weight_decay,
    fp16=fp16,
    bf16=bf16,
    max_grad_norm=max_grad_norm,
    max_steps=max_steps,
    warmup_ratio=warmup_ratio,
    group_by_length=group_by_length,
    lr_scheduler_type=lr_scheduler_type,
    report_to="tensorboard"
)

# Set supervised fine-tuning parameters


trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    args=training_arguments,
    packing=packing,
)

trainer.train()

# Train model
trainer.train()

# Save trained model
trainer.model.save_pretrained(new_model)

# Commented out IPython magic to ensure Python compatibility.
#  %load_ext tensorboard
#  %tensorboard --logdir results/runs

"""User inputs of various food items"""

# Run text generation pipeline with our next model
prompt_2 = """ You will be provided with food queries \
    You need to categorize the given food description to either of the options: Heart-healthy, Heart-unhealthy and Ambivalent \
    You will also give score to the food out of 5. 1 being unhealthiest and 5 being healthiest.\
    You will use principles from the American Heart Association for healthy diets to categorize and score the given food description\
    The principles are: Balance energy for a healthy weight.\
    Prioritize fruits, vegetables, and variety.\
    Choose whole grains over refined. Opt for healthy protein: plant-based, fish, low-fat dairy, lean meats.\
    Use liquid plant oils, avoid tropical oils, animal fats.\
    Prefer minimally processed over ultra-processed foods.\
    Limit added sugars in beverages and food. \
    Opt for low orno salt in food choices. \
    Avoid alcohol or limit intake if chosen.\
    All your responses must be one category. \
    You will also give score out of 5. 1 being unhealthiest and 5 being healthiest.\
    ####Categorize and give score to this description of food.\
    Main food description:Buckwheat groats\
    Food Code:56200510\
    WWEIA Category description:Pasta, noodles, cooked grains\
    Ingredient description: Buckwheat groats, roasted, cooked \
    Weight of the food:198 grams####"""


pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
result = pipe(f"<s>[INST] {prompt_2} [/INST]")
print(result[0]['generated_text'])

# Run text generation pipeline with our next model
prompt_3 = """ You will be provided with food queries \
    You need to categorize the given food description to either of the options: Heart-healthy, Heart-unhealthy and Ambivalent \
    You will also give score to the food out of 5. 1 being unhealthiest and 5 being healthiest.\
    You will use principles from the American Heart Association for healthy diets to categorize and score the given food description\
    The principles are: Balance energy for a healthy weight.\
    Prioritize fruits, vegetables, and variety.\
    Choose whole grains over refined. Opt for healthy protein: plant-based, fish, low-fat dairy, lean meats.\
    Use liquid plant oils, avoid tropical oils, animal fats.\
    Prefer minimally processed over ultra-processed foods.\
    Limit added sugars in beverages and food. \
    Opt for low orno salt in food choices. \
    Avoid alcohol or limit intake if chosen.\
    All your responses must be one category. \
    You will also give score out of 5. 1 being unhealthiest and 5 being healthiest.\
    ####Categorize and give score to this description of food.\
    Main food description:Fried pork chunks, Puerto Rican style\
    Food Code:22402510\
    WWEIA Category description: Pork\
    Ingredient description: Pork, fresh, loin, top loin (chops),\
    boneless, separable lean and fat, raw \
    Weight of the food:680.4 grams. ####"""


pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
result = pipe(f"<s>[INST] {prompt_3} [/INST]")
print(result[0]['generated_text'])

# Run text generation pipeline with our next model
prompt_4 = """ You will be provided with food queries \
    You need to categorize the given food description to either of the options: Heart-healthy, Heart-unhealthy and Ambivalent \
    You will also give score to the food out of 5. 1 being unhealthiest and 5 being healthiest.\
    You will use principles from the American Heart Association for healthy diets to categorize and score the given food description\
    The principles are: Balance energy for a healthy weight.\
    Prioritize fruits, vegetables, and variety.\
    Choose whole grains over refined. Opt for healthy protein: plant-based, fish, low-fat dairy, lean meats.\
    Use liquid plant oils, avoid tropical oils, animal fats.\
    Prefer minimally processed over ultra-processed foods.\
    Limit added sugars in beverages and food. \
    Opt for low orno salt in food choices. \
    Avoid alcohol or limit intake if chosen.\
    All your responses must be one category. \
    You will also give score out of 5. 1 being unhealthiest and 5 being healthiest.\
    #### Categorize and give score to this description of food.\
    Main food description:Chicken breast, baked, coated, skin / coating eaten\
    Food Code:24123120\
    WWEIA Category description: Chicken, whole pieces\
    Ingredient description: Chicken breast, baked, broiled, or roasted, skin eaten, from raw \
    Weight of the food:88 grams. ####"""


pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
result = pipe(f"<s>[INST] {prompt_4} [/INST]")
print(result[0]['generated_text'])

# Run text generation pipeline with our next model
prompt_5 = """ You will be provided with food queries \
    You need to categorize the given food description to either of the options: Heart-healthy, Heart-unhealthy and Ambivalent \
    You will also give score to the food out of 5. 1 being unhealthiest and 5 being healthiest.\
    You will use principles from the American Heart Association for healthy diets to categorize and score the given food description\
    The principles are: Balance energy for a healthy weight.\
    Prioritize fruits, vegetables, and variety.\
    Choose whole grains over refined. Opt for healthy protein: plant-based, fish, low-fat dairy, lean meats.\
    Use liquid plant oils, avoid tropical oils, animal fats.\
    Prefer minimally processed over ultra-processed foods.\
    Limit added sugars in beverages and food. \
    Opt for low orno salt in food choices. \
    Avoid alcohol or limit intake if chosen.\
    All your responses must be one category. \
    You will also give score out of 5. 1 being unhealthiest and 5 being healthiest.\
    ####Food1: Categorize and give score to this description of food.
    Main food description:Beef, rice, and vegetables including carrots, broccoli, and/or dark-green leafy; gravy
    Food Code:27315410
    WWEIA Category description:Meat mixed dishes
    Ingredient description:Rice, white, long-grain, regular, enriched, cooked
    Weight of the food:50.0 grams. ####"
    ####Fodd2: Categorize and give score to this description of food.
    Main food description:Swedish meatballs with cream or white sauce
    Food Code:27113300
    WWEIA Category description:Meat mixed dishes
    Ingredient description:Beverages, water, tap, drinking
    Weight of the food:177.75 grams. ####"""


pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
result = pipe(f"<s>[INST] {prompt_5} [/INST]")
print(result[0]['generated_text'])

# Run text generation pipeline with our next model
prompt_6 = """ You will be provided with food queries \
    You need to categorize the given food description to either of the options: Heart-healthy, Heart-unhealthy and Ambivalent \
    You will also give score to the food out of 5. 1 being unhealthiest and 5 being healthiest.\
    You will use principles from the American Heart Association for healthy diets to categorize and score the given food description\
    The principles are: Balance energy for a healthy weight.\
    Prioritize fruits, vegetables, and variety.\
    Choose whole grains over refined. Opt for healthy protein: plant-based, fish, low-fat dairy, lean meats.\
    Use liquid plant oils, avoid tropical oils, animal fats.\
    Prefer minimally processed over ultra-processed foods.\
    Limit added sugars in beverages and food. \
    Opt for low orno salt in food choices. \
    Avoid alcohol or limit intake if chosen.\
    All your responses must be one category. \
    You will also give score out of 5. 1 being unhealthiest and 5 being healthiest.\
    ####Food 1:Categorize and give score to this description of food.
    Main food description:Pork chop stewed with vegetables, Puerto Rican style
    Food Code:27422010
    WWEIA Category description:Meat mixed dishes
    Ingredient description:Tomatoes, red, ripe, canned, packed in tomato juice
    Weight of the food:793.8 grams. ####
    ####Food 2:Categorize and give score to this description of food.
    Main food description:Pasta, whole grain, with cream sauce and poultry, restaurant
    Food Code:58146721
    WWEIA Category description:Pasta mixed dishes, excludes macaroni and cheese
    Ingredient description:Salt, table, iodized
    Weight of the food:2.5 grams. ####
    """

pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
result = pipe(f"<s>[INST] {prompt_6} [/INST]")
print(result[0]['generated_text'])

# Run text generation pipeline with our next model
prompt_check = """ what is an apple####
    """

pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
result = pipe(f"<s>[INST] {prompt_check} [/INST]")
print(result[0]['generated_text'])

# Empty VRAM
del model
del pipe
del trainer
import gc
gc.collect()
gc.collect()

# Reload model in FP16 and merge it with LoRA weights
base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map,
)
model = PeftModel.from_pretrained(base_model, new_model)
model = model.merge_and_unload()

# Reload tokenizer to save it
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

import locale
locale.getpreferredencoding = lambda: "UTF-8"

from huggingface_hub import notebook_login

notebook_login()

model.push_to_hub("2_llma-heart-status-dataset", use_auth_token=True)