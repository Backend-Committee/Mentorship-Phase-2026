# Stack Overflow API Fetcher

A Python application that fetches recent questions from Stack Overflow, filters upvoted content, and saves the data in JSON format.

---

## Features

- Fetch latest active questions from Stack Overflow
- Filter questions with positive scores (upvoted only)
- Save data to JSON files
- View previously saved data
- Custom output filenames
- Menu-driven interface

---

## Project Description

This program interacts with the Stack Exchange API to retrieve recent Stack Overflow questions. It processes the returned data by filtering only upvoted questions, renames fields for clarity, and saves the results to a JSON file. Users can view saved data without making additional API calls.

---

## API Documentation

Stack Exchange API Documentation: https://api.stackexchange.com/docs

Endpoint used: `/2.3/questions`

API Reference: https://api.stackexchange.com/docs/questions

---

## Requirements

- Python 3.6 or higher
- requests library

---

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install requests
```

---

## API Key Setup

**Good news: No API key required for basic usage.**

The Stack Exchange API allows anonymous requests with the following limits:
- Without API key: 300 requests per day
- With API key: 10,000 requests per day

For most use cases, 300 requests per day is sufficient.

### Optional: To obtain an API key (if needed)

1. Register an application at: https://stackapps.com/apps/oauth/register
2. After registration, you will receive an API key
3. Modify the URL in `fetch_stackoverflow_questions()` to include your key:
```python
url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&key=YOUR_API_KEY'
```

---

## How to Run

1. Navigate to the project directory:
```bash
cd path/to/project
```

2. Run the program:
```bash
python api_program.py
```

3. Follow the menu prompts:
   - Option 1: Fetch new questions from Stack Overflow
   - Option 2: View previously saved data
   - Option 3: Change output filename
   - Option 4: Exit program

---

## Usage Example

```bash
$ python api_program.py

------------------------------------------------------------
Stack OverFlow API Fetcher
------------------------------------------------------------
1. Fetch New Questions
2. View Saved Data
3. Change Output Filename
4. Exit
------------------------------------------------------------

Enter your choice (1-4): 1

Fetching new data...
Fetching data from API..
Fetching Successful!
Data Saved Successfully to output.json

------------------------------------------------------------
Summary
------------------------------------------------------------
Total questions with upvotes: 25

First 3 Questions:
------------------------------------------------------------

1. How to use async/await in Python?
Upvotes: 5 | Answered: True
URL: https://stackoverflow.com/questions/...
------------------------------------------------------------
```

---

## Output Format

The program saves data in JSON format with the following structure:

```json
{
  "total_upvoted_questions": 25,
  "questions": [
    {
      "question_title": "How to use async/await in Python?",
      "url": "https://stackoverflow.com/questions/12345678",
      "id": 12345678,
      "upvotes": 5,
      "answered?": true
    }
  ]
}
```

---

## Field Descriptions

| Field | Description |
|-------|-------------|
| question_title | Title of the Stack Overflow question |
| url | Direct link to the question |
| id | Unique question identifier |
| upvotes | Number of upvotes (score) |
| answered? | Whether the question has an accepted answer |

---

## Files Created

- `output.json` - Default file containing fetched questions (customizable via menu)
- Custom filename specified by user (if using option 3)

---

## Error Handling

The program handles the following errors:

- Network connectivity issues
- Invalid API responses
- Missing or corrupted JSON files
- Invalid user input

---

## Customization

### Change API Parameters

Modify the URL in `fetch_stackoverflow_questions()`:

```python
# Sort by votes instead of activity
url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow'

# Filter by tag (e.g., python)
url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=python&site=stackoverflow'

# Change number of results (default is 30)
url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&pagesize=50'
```

### Modify Filter Criteria

Change the score threshold in `process_data()`:

```python
# Only questions with 10 or more upvotes
filtered_questions = [q for q in questions if q.get('score', 0) >= 10]
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
Install the requests library:
```bash
pip install requests
```

### "Failed to Fetch Data"
- Check internet connection
- Verify API endpoint is accessible
- Check if rate limit has been exceeded (300 requests/day)

### "File not found" when viewing saved data
Fetch data first using option 1 before trying to view saved data.

---

## Rate Limits

Without API key: 300 requests per day
With API key: 10,000 requests per day

The program does not track your request count. Monitor your usage to avoid hitting rate limits.

---

## License

This project is provided as-is for educational purposes.

---

## Additional Resources

- Stack Exchange API Documentation: https://api.stackexchange.com/docs
- Python Requests Library: https://requests.readthedocs.io/
- JSON in Python: https://docs.python.org/3/library/json.html
