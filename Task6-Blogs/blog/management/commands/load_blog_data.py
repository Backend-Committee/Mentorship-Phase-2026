from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from blog.models import Category, BlogPost, Comment

class Command(BaseCommand):
    help = 'Load initial blog data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading blog data...')
        
        # Clear existing data
        Comment.objects.all().delete()
        BlogPost.objects.all().delete()
        Category.objects.all().delete()
        
        # Create Users (authors)
        users_data = [
            {'username': 'john_doe',     'email': 'john@example.com',   'password': 'pass1234!', 'first_name': 'John',   'last_name': 'Doe'},
            {'username': 'jane_smith',   'email': 'jane@example.com',   'password': 'pass1234!', 'first_name': 'Jane',   'last_name': 'Smith'},
            {'username': 'mike_johnson', 'email': 'mike@example.com',   'password': 'pass1234!', 'first_name': 'Mike',   'last_name': 'Johnson'},
            {'username': 'sarah_w',      'email': 'sarah@example.com',  'password': 'pass1234!', 'first_name': 'Sarah',  'last_name': 'Williams'},
            {'username': 'david_brown',  'email': 'david@example.com',  'password': 'pass1234!', 'first_name': 'David',  'last_name': 'Brown'},
            {'username': 'emily_chen',   'email': 'emily@example.com',  'password': 'pass1234!', 'first_name': 'Emily',  'last_name': 'Chen'},
            {'username': 'robert_m',     'email': 'robert@example.com', 'password': 'pass1234!', 'first_name': 'Robert', 'last_name': 'Martinez'},
            {'username': 'lisa_a',       'email': 'lisa@example.com',   'password': 'pass1234!', 'first_name': 'Lisa',   'last_name': 'Anderson'},
        ]
        
        users = {}
        for user_data in users_data:
            # get_or_create avoids crashing if user already exists
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            else:
                self.stdout.write(f'User already exists: {user.username}')
            users[user_data['username']] = user

        # Create Categories
        categories_data = [
            {'name': 'Tutorial',       'description': 'Step-by-step guides and tutorials for learning'},
            {'name': 'Technical',      'description': 'Technical deep dives and advanced topics'},
            {'name': 'Comparison',     'description': 'Comparisons between different technologies'},
            {'name': 'Best Practices', 'description': 'Industry best practices and guidelines'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[category.name] = category
            self.stdout.write(f'Created category: {category.name}')
        
        # Create Blog Posts (author is now a User FK)
        blog_posts_data = [
            {
                'title': 'Getting Started with Django',
                'author': users['john_doe'],
                'content': '''Django is a high-level Python web framework that encourages rapid development 
                and clean, pragmatic design. Built by experienced developers, it takes care of much of the 
                hassle of web development, so you can focus on writing your app without needing to reinvent 
                the wheel. It's free and open source.
                
                In this comprehensive guide, we'll explore the fundamentals of Django and how to get started 
                with your first project. Django follows the MTV (Model-Template-View) pattern, which is 
                similar to MVC but with some differences.
                
                The framework provides a robust ORM (Object-Relational Mapping) system that allows you to 
                interact with your database using Python code instead of SQL. It also includes a powerful 
                authentication system, an admin interface that's automatically generated from your models, 
                and a template engine for rendering HTML.''',
                'category': categories['Tutorial'],
                'published_date': timezone.now().date() - timedelta(days=30),
            },
            {
                'title': 'Understanding Django Templates',
                'author': users['jane_smith'],
                'content': '''Django's template system is powerful and flexible. Templates are text files 
                that define the structure of an HTML page. They use special syntax to insert dynamic content 
                and implement logic.
                
                Template inheritance is one of the most powerful features, allowing you to build a base 
                skeleton template that contains all the common elements of your site and defines blocks 
                that child templates can override.
                
                Django templates support variables, filters, tags, and comments. Variables are surrounded 
                by {{ and }}, tags by {% and %}, and comments by {# and #}.''',
                'category': categories['Tutorial'],
                'published_date': timezone.now().date() - timedelta(days=25),
            },
            {
                'title': 'Django URL Routing Explained',
                'author': users['mike_johnson'],
                'content': '''URL routing in Django is handled through URLconf (URL configuration). 
                The URLconf maps URL patterns to views. When a user requests a page, Django goes through 
                each URL pattern in order and stops at the first one that matches.
                
                Named URLs and namespaces help you avoid hardcoding URLs in your templates and make 
                refactoring easier. Django also supports reverse URL resolution, which means you can 
                refer to URLs by their name rather than hardcoding them.''',
                'category': categories['Technical'],
                'published_date': timezone.now().date() - timedelta(days=20),
            },
            {
                'title': 'Working with Static Files in Django',
                'author': users['sarah_w'],
                'content': '''Static files (CSS, JavaScript, images) are an essential part of web applications. 
                Django provides a flexible system for managing static files. During development, Django can 
                serve static files automatically when DEBUG is True.
                
                For production, you'll need to collect all static files into a single directory using the 
                collectstatic command. The {% static %} template tag helps you reference static files 
                in a portable way.''',
                'category': categories['Tutorial'],
                'published_date': timezone.now().date() - timedelta(days=15),
            },
            {
                'title': 'Function-Based vs Class-Based Views',
                'author': users['david_brown'],
                'content': '''Django offers two ways to write views: function-based views (FBVs) and 
                class-based views (CBVs). Function-based views are simple Python functions that take a 
                request and return a response. They're straightforward and easy to understand.
                
                Class-based views provide more structure and reusability through inheritance. They're more 
                powerful for complex scenarios but have a steeper learning curve. For simple applications 
                and learning purposes, function-based views are often the better choice.''',
                'category': categories['Comparison'],
                'published_date': timezone.now().date() - timedelta(days=10),
            },
            {
                'title': 'Django ORM Best Practices',
                'author': users['emily_chen'],
                'content': '''The Django ORM is one of its most powerful features, allowing you to interact 
                with your database using Python code. Use select_related() for foreign key relationships 
                and prefetch_related() for many-to-many relationships to avoid the N+1 query problem.
                
                The Django Debug Toolbar is an invaluable tool for identifying slow queries. Database 
                indexing is another critical aspect — add indexes to fields that you frequently filter by.''',
                'category': categories['Best Practices'],
                'published_date': timezone.now().date() - timedelta(days=5),
            },
            {
                'title': 'Building RESTful APIs with Django',
                'author': users['robert_m'],
                'content': '''Django REST Framework (DRF) is a powerful toolkit for building Web APIs. 
                Serializers handle converting complex data types like Django models into JSON. DRF provides 
                several types of views: function-based views, APIView classes, and ViewSets.
                
                Authentication and permissions are built-in, supporting everything from basic authentication 
                to OAuth and custom schemes.''',
                'category': categories['Technical'],
                'published_date': timezone.now().date() - timedelta(days=2),
            },
            {
                'title': 'Django Security Best Practices',
                'author': users['lisa_a'],
                'content': '''Security should be a top priority in any web application. Django provides 
                excellent security features out of the box, protecting against SQL injection, XSS, CSRF, 
                and clickjacking.
                
                Always use Django's template system to render user input. Use environment variables for 
                sensitive data like SECRET_KEY — never commit them to version control.''',
                'category': categories['Best Practices'],
                'published_date': timezone.now().date(),
            },
        ]
        
        posts = {}
        for i, post_data in enumerate(blog_posts_data, 1):
            post = BlogPost.objects.create(**post_data)
            posts[i] = post
            self.stdout.write(f'Created blog post: {post.title}')
        
        # Create Comments
        comments_data = [
            {'post': posts[1], 'name': 'Alice Johnson', 'email': 'alice@example.com', 'content': 'Great introduction to Django! This really helped me get started.'},
            {'post': posts[1], 'name': 'Bob Smith',     'email': 'bob@example.com',   'content': 'Could you explain more about the ORM in future posts?'},
            {'post': posts[2], 'name': 'Carol White',   'email': 'carol@example.com', 'content': 'Template inheritance is such a powerful feature. Thanks for explaining it so clearly!'},
            {'post': posts[3], 'name': 'David Lee',     'email': 'david@example.com', 'content': 'URL routing was confusing me, but this post cleared it up. Excellent work!'},
            {'post': posts[4], 'name': 'Eve Taylor',    'email': 'eve@example.com',   'content': 'The explanation about collectstatic was very helpful. Thank you!'},
            {'post': posts[5], 'name': 'Frank Miller',  'email': 'frank@example.com', 'content': 'I prefer FBVs for their simplicity, but CBVs are great for complex scenarios.'},
            {'post': posts[6], 'name': 'Grace Chen',    'email': 'grace@example.com', 'content': 'The ORM tips are gold! This will definitely improve my app performance.'},
        ]
        
        for comment_data in comments_data:
            comment = Comment.objects.create(**comment_data)
            self.stdout.write(f'Created comment by {comment.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all blog data!'))
        self.stdout.write(f'Created {User.objects.count()} users')
        self.stdout.write(f'Created {Category.objects.count()} categories')
        self.stdout.write(f'Created {BlogPost.objects.count()} blog posts')
        self.stdout.write(f'Created {Comment.objects.count()} comments')
        self.stdout.write('------- Login credentials -------')
        self.stdout.write('All users have password: pass1234!')