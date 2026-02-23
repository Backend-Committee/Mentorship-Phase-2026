# U+0600 Social Media

A Django-based social media application that allows users to create, view, edit, and delete posts.

## Setup & Installation

### 1. Migrate and Load Fixture Data

To set up the database and load initial data:

```bash
python manage.py migrate
python manage.py loaddata initial_data
```


### 2. Test Account

you now have an account, and you can explore the application with it:

- **Username:** `testing`
- **Password:** `password`

## Features

### 1. **User Authentication**
- User registration with username and password
- Secure login and logout functionality
- Protected views requiring login
- **Implementation:** Django's built-in `LoginRequiredMixin` and authentication system

### 2. **User Profile & Timezone**
- Each user has an associated profile with timezone settings
- Application automatically guesses the user's timezone during account creation
- All timestamps (post creation, updates) are displayed in the user's local timezone
- **Implementation:** One-to-one `Profile` model linked to Django's User model with timezone field; `TimezoneMiddleware` activates the user's timezone on each request

### 3. **Post Listing & Pagination**
- View all posts from all users in paginated format
- Posts displayed in reverse chronological order (newest first)
- **Implementation:** Django `ListView` class-based view with pagination

### 4. **Post Detail View**
- Click on any post to view its full content
- Shows post title, content, creation/update timestamps, and owner information
- Displays ownership indicator (shows edit/delete buttons only if you're the post owner)
- **Implementation:** Django `DetailView`

### 5. **Create Posts**
- Authenticated users can create new posts with title and content
- Automatically associates post with the logged-in user
- **Implementation:** Django `CreateView` that sets the post owner to the current user on form submission

### 6. **Edit Posts**
- Users can edit only their own posts
- Access edit button only on posts they own
- **Implementation:** Django `UpdateView` with `UserPassesTestMixin` for ownership verification

### 7. **Delete Posts**
- Users can delete only their own posts
- Confirmation dialog before deletion
- **Implementation:** Django `DeleteView` with `UserPassesTestMixin` for ownership verification
