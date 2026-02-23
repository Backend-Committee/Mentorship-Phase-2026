# Advanced Blog with Polls & Rich Text Editor

An advanced multi-author blog platform built with Django. This project features rich content creation, user interaction (likes/comments), a complete polling system, and robust search capabilities, all implemented using Class-Based Views (CBVs).

## Features

### Advanced Content Management
*   **Rich Text Editor (CKEditor):** Authors can format posts with bold text, headings, colors, and more.
*   **Image Support:** Upload and embed multiple images directly within post content.
*   **CRUD Operations:** Full Create, Read, Update, and Delete capabilities for authors.
*   **Preview & Edit:** Clean interface for editing and previewing rich content.

### User Interaction
*   **Multiple Authors:** Users can register, log in, and manage their own posts.
*   **Comments & Likes:** Registered users can like posts and leave comments to engage with content.
*   **Search:** Search functionality scans both post titles and rich text body content.

### Polling System
*   **Create Polls:** Users can create custom polls with dynamic options.
*   **Voting:** Registered users can vote on active polls.
*   **Poll Comments:** Dedicated comment section for discussing poll topics.
*   **Real-time Results:** View poll results immediately after voting.

### Authentication & Security
*   **User Accounts:** Registration, Login, and Logout functionality.
*   **Role-Based Access:** 
    *   Only registered users can create content, vote, or comment.
    *   Only authors can edit or delete their own posts.

## Technologies Used
*   **Backend:** Django 5.x / 6.x
*   **Views:** Class-Based Views (ListView, DetailView, CreateView, UpdateView, DeleteView)
*   **Editor:** Django CKEditor (Rich Text Field)
*   **Frontend:** Bootstrap 5, HTML5, CSS3
*   **Database:** SQLite (Default)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Blog2
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install django django-ckeditor pillow
    ```

4.  **Apply Migrations:**
    ```bash
    cd Blog
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a Superuser (Optional):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application:**
    Open your browser and navigate to `http://127.0.0.1:8000/`

## Project Structure
```
Blog/
├── Blog/               # Project settings & configuration
├── post/               # Blog posts, comments, likes, and polling system
├── user/               # User authentication and profiles
├── templates/          # HTML templates (Bootstrap 5)
├── static/             # Static files (CSS, JS, Images)
├── media/              # User-uploaded content (Images)
└── manage.py           # Django management script
```

## author 
    - ** name **: Mahmoud Adam
    - ** email **: mahmoudadam5555@gmail.com 

 
