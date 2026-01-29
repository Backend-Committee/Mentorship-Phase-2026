Meal Data Processor ??
Project Description
This project is a Python-based data processing tool that fetches meal recipes from an external API. It filters and organizes data based on specific cuisines (Indian and Chinese), renames data fields for better readability, and exports the results into structured JSON files.

API Documentation
This project utilizes the public API from: TheMealDB API Documentation

Setup Instructions
To get this project running on your local machine, follow these steps:

Install Python: Ensure you have Python installed on your system.

Install Dependencies: This project requires the requests library. Install it using pip:

Bash
pip install requests
File Setup: Save the code in a file named main.py.

API Key Setup
This project uses the Free Tier API key (1) provided by TheMealDB for development purposes.

No private API key is required to run the current version of this script.

How to Run the Project
Run the script through your terminal or command prompt:

Bash
python main.py
Features & Outputs:
Data Transformation: Renames raw API fields to user-friendly keys like Meal_Name and Meal_Link_Youtube.

Data Export: Generates three JSON files:

meal_combine.json: The full list of processed chicken meals.

Egyptian_Meals.json: (Contains Indian cuisine data as per the filter).

Chinese_Meals.json: Contains filtered Chinese cuisine data.

Console Summary: Displays the HTTP status code and the total count of meals processed for each category.

Expected Console Output:
Plaintext
Status_Code 200
Number of Total Meals :  [Total Count]
Number of Indian Meals : [Count]
Number of Chinese Meals : [Count]