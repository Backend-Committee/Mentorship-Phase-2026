# 📜 Random Poetry – Django Web Application

## 📌 Project Overview

**Random Poetry** is a Django-based web application that displays:

- 🎲 A randomly selected poem on the homepage
- 👤 A dedicated page listing poets with detailed information

The project demonstrates essential Django concepts such as:

- URL routing and views
- Template rendering
- Reading external JSON files
- Passing dynamic context data
- Using Python’s `random` module

To keep the project lightweight and beginner-friendly, no database is used. All data is stored and managed using JSON files.

---

## 🎯 Project Goals

- Practice Django fundamentals
- Learn how to read and parse JSON files in Django
- Understand dynamic content rendering
- Build a simple content-driven web application

---

## 🛠 Technologies Used

- Python

- Django

- HTML / CSS

- JSON

## 📂 Data Storage

### 1️⃣ poems.json

Stores poetry content and metadata:

```json
{
  "id": 1,
  "title": "Poem Title",
  "poet": "Poet Name",
  "era": "Era",
  "meter": "Poetic Meter",
  "rhyme": "Rhyme",
  "theme": "Theme",
  "content": [
    "Verse 1",
    "Verse 2"
  ]
}
```
### Poets.json
```
{
  "id": 1,
  "name": "Poet Name",
  "full_name": "Full Name",
  "birth_date": "YYYY-MM-DD",
  "death_date": "YYYY-MM-DD",
  "bio": "Short biography",
  "era": "Era",
  "notable_works": []
}
```

### Application logic
⚙️ Application Logic
Homepage – Random Poem

The homepage loads a random poem each time it is visited.

How it works:

- The poems.json file is loaded.

- A random poem ID is generated.

- The matching poem is selected.

- Poem data is passed to the template and rendered dynamically.

```python
def index(request):
    file_path = Path(settings.BASE_DIR) / "Blog" / "poems.json"

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    random_id = int(random.random() * len(data)) + 1
    poem = next(item for item in data if item["id"] == random_id)

    context = {
        "title": poem["title"],
        "content": poem["content"],
        "meter": poem["meter"],
        "rhyme": poem["rhyme"],
        "theme": poem["theme"]
    }

    return render(request, "Blog/index.html", context)

```

### Poets Page – List of Poets

The poets page displays all poets stored in Poets.json.

How it works:

- The file is read and parsed.

- The full list of poets is passed to the template.

- The data is rendered using loops in HTML.

```python
def poets(request):
    file_path = Path(settings.BASE_DIR) / "Blog" / "Poets.json"

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return render(request, "Blog/Poets.html", {"poets": data})
```

### URL Configuration

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('Poets.html', views.poets, name='poets'),
]
```