# Food Categorization and Health Scoring Model

## Database Details
This project utilizes the FoodData Central database provided by the USDA. The database contains extensive information on food items and their nutrient profiles.

### 1. FoodData Central Data
- **Description**: The database includes over 19,310 different categories of general food.
- **Source**:
  - [Download datasets](https://fdc.nal.usda.gov/download-datasets.html)
  - [Data Dictionary](https://fdc.nal.usda.gov/data-dictionary.html)
- **Contents**: Detailed nutritional information for a variety of food items, organized across multiple categories.

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
