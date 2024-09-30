# Food Categorization and Health Scoring Model

## Database Details
This project utilizes the FoodData Central database provided by the USDA. The database contains extensive information on food items and their nutrient profiles.

### FoodData Central Data
- **Description**: The database includes over 19,310 different categories of general food.
- **Source**:
  - [Download datasets](https://fdc.nal.usda.gov/download-datasets.html)
  - [Data Dictionary](https://fdc.nal.usda.gov/data-dictionary.html)
- **Contents**: Detailed nutritional information for a variety of food items, organized across multiple categories.
## Table of Contents
1. [Task 3: Structuring ChatGPT Responses and Uploading to Hugging Face](#task-3-structuring-chatgpt-responses-and-uploading-to-hugging-face)
2. [Data Formatting](#data-formatting)
3. [Example Data Entry](#example-data-entry)
4. [Upload to Hugging Face](#upload-to-hugging-face)
5. [Fine-Tuning Script](#fine-tuning-script)



## Project Purpose
The purpose of this project is to model a customized large language model capable of categorizing food or food ingredients based on various features. The project leverages the FoodData Central database and organizes food items using attributes such as:

- Food Code
- Main Food Description
- WWEIA Category Number
- WWEIA Category Description
- Seq Num
- Ingredient Code
- Ingredient Description
- Ingredient Weight (g)
- Retention Code
- Moisture Change (%)

### Example of Categorized Data:
| Food Code | Main Food Description | WWEIA Category Number | WWEIA Category Description | Seq Num | Ingredient Code | Ingredient Description | Ingredient Weight (g) | Retention Code | Moisture Change (%) |
|-----------|-----------------------|-----------------------|----------------------------|---------|------------------|------------------------|-----------------------|----------------|---------------------|
| 11000000  | Milk, human           | 9602                  | Human milk                 | 1       | 1107             | Milk, human, mature, fluid (For Reference Only) | 100                   | 0              | 0                   |

This model aims to accurately categorize food items based on these features, enabling better data organization and retrieval.

## Project Process
To categorize the 19,310 food items and their features, ChatGPT-3 was utilized with carefully designed prompt engineering. The model was tasked with assigning categories and scores to each food item based on American Heart Association principles.

### Prompt Engineering
A custom prompt was created to ensure accurate and consistent responses. The prompt categorized food into three categories and provided a healthiness score based on American Heart Association guidelines:

#### Categories:
- Heart-Healthy
- Heart-Unhealthy
- Ambivalent

#### Scoring:
- 1 = Unhealthiest food
- 2 = Unhealthy food
- 3 = Ambivalent food
- 4 = Healthy food
- 5 = Healthiest food

# Food Categorization and Health Scoring Project



### The prompt used is as follows:
```python
def find_category_and_score_v2(user_input):
    """
    Categorize and score food descriptions based on American Heart Association principles.
    """
    delimiter = "####"
    system_message = f"""
    You will be provided with a food query ...
    (continues with prompt description)
    """
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
    ]
    return get_completion_from_messages(messages)
```

## Example Query

### Input Example



### JSON Output
```json
[
  {
    "Main food description": "Milk, human",
    "Food Code": "11000000",
    "category": "Heart-Healthy",
    "Score": 5
  }
]
```
This process was repeated for all 19,310 food items, generating a category and score for each.


# Food Item Database Creation

## Database Creation
After several hours of response collection over multiple days, a comprehensive database was constructed using the outputs generated by ChatGPT-3. This database contains the categorized results and scores for over 19,310 food items.

## Process Summary

### ChatGPT-3 Prompting
The model was prompted using custom-engineered queries to categorize food items based on features like:

- **Main food description**
- **Food code**
- **WWEIA category number**
- **Ingredient description**, etc.

### Response Collection
The responses from the model included JSON-formatted objects, containing:

- **Food Category** (Heart-Healthy, Heart-Unhealthy, Ambivalent)
- **Health Score** (1-5, based on American Heart Association guidelines)

### Example of Collected Data
```json
[
  {
    "Main food description": "Milk, human",
    "Food Code": "11000000",
    "category": "Heart-Healthy",
    "Score": 5
  },
  {
    "Main food description": "Beef, raw",
    "Food Code": "13010000",
    "category": "Heart-Unhealthy",
    "Score": 1
  }
]
```
# Task 2: Fine-tuning the LLaMA Model

After constructing the database of food categorizations and health scores, the next step was to fine-tune a pre-trained LLaMA model using this dataset. The fine-tuned model was designed to specialize in categorizing food based on American Heart Association guidelines, similar to the original task handled by ChatGPT-3.

## Fine-tuning Process

### Base Model
The model selected for fine-tuning is the **LLaMA-2-7B Chat model**, available on Hugging Face:

```python
model_name = "NousResearch/Llama-2-7b-chat-hf"
```


# Dataset

The instruction dataset created during Task 1 was uploaded to Hugging Face under the following name:

```python
dataset_name = "adarsha30735/datafood"
```
## Fine-tuning Objective

The goal of fine-tuning was to adapt the LLaMA-2-7B model to better understand and categorize food items based on the patterns and features captured in the dataset.

## Output

The fine-tuned model was saved under the name **llama-2-7b-heartgpt**, specializing in food categorization:

```python
new_model = "llama-2-7b-heartgpt"
```
## Model Creation

A new model was created and trained using the fine-tuned dataset, enabling it to predict food healthiness, provide heart-health categories, and score new food items more accurately than before.

## Final Model

The fine-tuned **llama-2-7b-heartgpt** model is ready for inference tasks related to food categorization and health scoring based on the provided data.

# Task 3: Structuring ChatGPT Responses and Uploading to Hugging Face

The responses generated by ChatGPT-3 for all 19,310 food items were structured and formatted before being uploaded to Hugging Face. This dataset now serves as the training data for fine-tuning the LLaMA-2-7B model, specializing in food categorization and health scoring.

## Data Formatting

All 19,310 responses were structured in a consistent format, ensuring each entry included all the necessary fields related to the food item, its features, and ChatGPT's classification result.

### Structured Data Format

```css
<s>
Food code    Main food description    WWEIA Category number    WWEIA Category description    Seq num    Ingredient code    Ingredient description    Ingredient weight (g)    Retention code    Moisture change (%)    Formatted Description    ChatGPT classification result
</s>
```

## Example Data Entry

```yaml
<s>
11000000    Milk, human    9602    Human milk    1    1107    Milk, human, mature, fluid (For Reference Only)    100    0    0    ####Categorize and give score to this description of food.
Main food description: Milk, human
Food Code: 11000000
WWEIA Category description: Human milk
Ingredient description: Milk, human, mature, fluid (For Reference Only)
Weight of the food: 100.0 grams.
####
[{
    'Main food description': 'Milk, human',
    'Food Code': '11000000',
    'category': 'Heart-Healthy',
    'Score': 5
}]
</s>
```

## Upload to Hugging Face

The entire structured dataset was then uploaded to Hugging Face under the following dataset name:

```bash
adarsha30735/datafood
```


### Script Overview

- **Script Name:** `heartgpt_fine_tune_llama_2_in_google_colab.py`
- **Purpose:** Fine-tunes the LLaMA-2-7B model to specialize in food categorization and health scoring based on the data provided.
- **Environment:** The script is optimized to run in Google Colab, leveraging its computational resources for model training.

### Key Features

- Loads the dataset from Hugging Face.
- Configures model parameters and hyperparameters for training.
- Implements training loops, validation, and evaluation metrics.
- Saves the fine-tuned model for future inference tasks.

### How to Use

1. Open Google Colab and create a new notebook.
2. Upload the `heartgpt_fine_tune_llama_2_in_google_colab.py` script to your Colab environment.
3. Run the script, ensuring that you have the necessary libraries and access to the dataset on Hugging Face.
4. After training, the fine-tuned model will be saved under the name **llama-2-7b-heartgpt**.



## Contributors and Fine-Tuning Reference

The fine-tuning of the LLaMA-2-7B model was successfully completed with the assistance of various contributors who provided insights and guidance throughout the process. A key resource utilized during this phase was the code from the **Guanaco Dataset**, which served as a reference for adapting the model to our specific needs in food categorization and health scoring.

For detailed reference code, you can check the GitHub page [here](https://gist.github.com/younesbelkada/9f7f75c94bdc1981c8ca5cc937d4a4da).

### Fine-Tuning Process Overview

**Reference Code:** The fine-tuning code adapted from the Guanaco Dataset was instrumental in streamlining the training process for our specific dataset of food items. The structure, methodology, and techniques employed in the reference helped optimize our fine-tuning approach.


### Implementation

The reference code provided by contributors was modified to fit our dataset structure and fine-tuning objectives, ensuring the model could effectively learn from the data. The integration of techniques from the Guanaco Dataset ensured that our model adhered to the best practices in fine-tuning transformer models for specific tasks.

### Final Model

The final output from this collaborative fine-tuning process is the **llama-2-7b-heartgpt** model, which excels in predicting the healthiness of food items, categorizing them according to American Heart Association guidelines, and providing accurate scores based on the processed dataset.
