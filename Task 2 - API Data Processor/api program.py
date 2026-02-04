import requests
import json

def fetch_stackoverflow_questions():
    #fetches the recent questions from stackoverflow
    url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow'

    print("Fetching data from API..")
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Fetching Successful!")
        return response.json()
    else:
        print(f"Error: {response.status_code} with the Fetching Process")
        return None
    
def process_data(data):
    if not data or 'items' not in data:
        return None
    
    questions = data['items']
    #filters only questions with positive scores (above 0/ upvoted questions)
    filtered_questions = [q for q in questions if q.get('score', 0) > 0]

    processed_questions = []
    for question in filtered_questions:
        processed_questions.append({
            #renamed the fields
            'question_title': question.get('title', 'No Title Available'),
            'url': question.get('link', ''),
            'id': question.get('question_id', 0),
            'upvotes': question.get('score', 0),
            'answered?': question.get('is_answered', False)
            })


    total_questions = len(processed_questions)
    result = {
        "total_upvoted_questions": total_questions,
        "questions": processed_questions
    }

    return result

def save_to_file(data, filename='output.json'):

    #saves the processed data to a json file
    with open(filename, "w") as f:
        json.dump(data, f, indent = 2)
    print(f"Data Saved Successfully to {filename}")


def display_summary(data):
    #displays a summary of the fetched questions
        print("\n" + "-" * 60)
        print("Summary")
        print("-" * 60)
        print(f"Total questions with upvotes: {data['total_upvoted_questions']}")
        print(f"\nFirst 3 Questions:")
        print("-" * 60)
        for i, q in enumerate(data['questions'][:3], 1):
            print(f"\n{i}. {q['question_title']}")
        print(f"Upvotes: {q['upvotes']} | Answered: {q['answered']}")
        print(f"URL: {q['url']}")
        print("-" * 60)

#Menu System

def show_menu():
    #displays the menu/choices u can do
        print("\n" + "-" * 60)
        print("Stack OverFlow API Fetcher")
        print("-" * 60)
        print("1. Fetch New Questions")
        print("2. View Saved Data")
        print("3. Change Output Filename")
        print("4. Exit")
        print("-" * 60)

def view_saved_data(filename='output.json'):
    # reads and displays data from the saved JSON file
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"\n Reading from {filename}...")
        display_summary(data)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found. Try fetching data first.")
    except json.JSONDecodeError:
        print(f"Error: {filename} contains invalid JSON data")        

def main():
    output_filename = 'output.json'  #the default filename
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # fetch new questions
            print("\n🔄 Fetching new data...")
            raw_data = fetch_stackoverflow_questions()
            
            if raw_data:
                processed_data = process_data(raw_data)
                
                if processed_data:
                    save_to_file(processed_data, output_filename)
                    display_summary(processed_data)
                else:
                    print("No Data to Process")
            else:
                print("Failed to Fetch Data")
        
        elif choice == '2':
            # view saved data
            view_saved_data(output_filename)
        
        elif choice == '3':
            # change output filename
            new_filename = input("Enter new filename (e.g., data.json): ").strip()
            if new_filename:
                if not new_filename.endswith('.json'):
                    new_filename += '.json'
                output_filename = new_filename
                print(f"✓ Output filename changed to: {output_filename}")
            else:
                print("Filename cannot be empty!")
        
        elif choice == '4':
            # Exit
            print("\nThanks for using the program! Goodbye! <3")
            break
        
        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()