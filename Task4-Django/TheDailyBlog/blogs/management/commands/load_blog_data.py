from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from blogs.models import Category, BlogPost, Comment

class Command(BaseCommand):
    help = 'Load initial blog data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading blog data...')
        
        # Clear existing data
        Comment.objects.all().delete()
        BlogPost.objects.all().delete()
        Category.objects.all().delete()
        
        # Create Categories
        categories_data = [
            {
                'name': 'Tutorial',
                'description': 'Step-by-step guides and tutorials for learning'
            },
            {
                'name': 'Technical',
                'description': 'Technical deep dives and advanced topics'
            },
            {
                'name': 'Comparison',
                'description': 'Comparisons between different technologies'
            },
            {
                'name': 'Best Practices',
                'description': 'Industry best practices and guidelines'
            },
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[category.name] = category
            self.stdout.write(f'Created category: {category.name}')
        
        blog_posts_data = [
            {
                'title': 'Getting Started with Django',
                'author': 'John Doe',
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
                and a template engine for rendering HTML.
                
                Django emphasizes reusability and "pluggability" of components, rapid development, and the 
                principle of don't repeat yourself (DRY). It also provides security features to help 
                developers avoid common security mistakes.''',
                'category': categories['Tutorial'],
                'published_date': timezone.now().date() - timedelta(days=30),
            },
            {
                'title': 'Understanding Django Templates',
                'author': 'Jane Smith',
                'content': '''Django's template system is powerful and flexible. Templates are text files 
                that define the structure of an HTML page. They use special syntax to insert dynamic content 
                and implement logic.
                
                The template language is designed to strike a balance between power and ease. It's designed 
                to feel comfortable to those used to working with HTML. If you have any exposure to other 
                text-based template languages, you should feel right at home with Django's templates.
                
                Template inheritance is one of the most powerful features, allowing you to build a base 
                "skeleton" template that contains all the common elements of your site and defines blocks 
                that child templates can override. This makes it easy to maintain consistent design across 
                your entire application while allowing flexibility where needed.
                
                Django templates support variables, filters, tags, and comments. Variables are surrounded 
                by {{ and }}, tags by {% and %}, and comments by {# and #}. Filters allow you to modify 
                variables for display, and tags provide arbitrary logic in the rendering process.''',
                'category': categories['Tutorial'],
                'published_date': timezone.now().date() - timedelta(days=25),
            },
            {
                'title': 'Django URL Routing Explained',
                'author': 'Mike Johnson',
                'content': '''URL routing in Django is handled through URLconf (URL configuration). 
                The URLconf maps URL patterns to views. When a user requests a page, Django goes through 
                each URL pattern in order and stops at the first one that matches.
                
                You can use both project-level and app-level URL configurations to organize your routes 
                effectively. This separation of concerns makes your code more maintainable and reusable. 
                Named URLs and namespaces help you avoid hardcoding URLs in your templates and make 
                refactoring easier.
                
                URL patterns use Python's regular expressions or simplified path converters to match 
                URLs. Path converters like <int:id> make it easy to capture parts of the URL and pass 
                them as arguments to your views.
                
                Django also supports reverse URL resolution, which means you can refer to URLs by their 
                name rather than hardcoding them. This is extremely useful for maintaining your codebase 
                as your application grows and URLs might change.''',
                'category': categories['Technical'],
                'published_date': timezone.now().date() - timedelta(days=20),
            },
            {
                'title': 'Working with Static Files in Django',
                'author': 'Sarah Williams',
                'content': '''Static files (CSS, JavaScript, images) are an essential part of web applications. 
                Django provides a flexible system for managing static files. During development, Django can 
                serve static files automatically when DEBUG is True.
                
                For production, you'll need to collect all static files into a single directory using the 
                collectstatic command. This command gathers static files from each of your applications 
                (and any other places you specify) into a single location that can easily be served in 
                production.
                
                The {% static %} template tag helps you reference static files in a portable way. This 
                tag uses the STATIC_URL setting to construct the URL for the given relative path. 
                
                Organizing your static files properly and understanding the STATIC_URL, STATIC_ROOT, and 
                STATICFILES_DIRS settings is crucial for maintaining a professional Django project. You 
                should also consider using a CDN (Content Delivery Network) for serving static files in 
                production to improve performance.''',
                'category': categories['Tutorial'],
                'published_date': timezone.now().date() - timedelta(days=15),
            },
            {
                'title': 'Function-Based vs Class-Based Views',
                'author': 'David Brown',
                'content': '''Django offers two ways to write views: function-based views (FBVs) and 
                class-based views (CBVs). Function-based views are simple Python functions that take a 
                request and return a response. They're straightforward and easy to understand, making them 
                perfect for beginners.
                
                Function-based views give you complete control over the request/response cycle. You write 
                explicit code for handling different HTTP methods (GET, POST, etc.) and processing form data. 
                This explicitness makes the code easy to read and understand.
                
                Class-based views provide more structure and reusability through inheritance. They're more 
                powerful for complex scenarios but have a steeper learning curve. CBVs are organized around 
                HTTP methods as class methods, and Django provides many generic views that handle common 
                patterns.
                
                For simple applications and learning purposes, function-based views are often the better 
                choice. As your application grows, you might find class-based views more maintainable, 
                especially when you need to reuse similar logic across multiple views.''',
                'category': categories['Comparison'],
                'published_date': timezone.now().date() - timedelta(days=10),
            },
            {
                'title': 'Django ORM Best Practices',
                'author': 'Emily Chen',
                'content': '''The Django ORM (Object-Relational Mapping) is one of its most powerful features, 
                allowing you to interact with your database using Python code. However, it's easy to write 
                inefficient queries that can slow down your application.
                
                Understanding query optimization is crucial. Use select_related() for foreign key relationships 
                and prefetch_related() for many-to-many and reverse foreign key relationships to avoid the 
                N+1 query problem. Always use .only() and .defer() when you don't need all fields.
                
                The Django Debug Toolbar is an invaluable tool for identifying slow queries. It shows you 
                exactly what SQL queries are being executed and how long they take. Use it during development 
                to catch performance issues early.
                
                Database indexing is another critical aspect. Add indexes to fields that you frequently query 
                or filter by. Django makes it easy to add indexes through the Meta class in your models. 
                Remember that while indexes speed up reads, they can slow down writes, so use them judiciously.''',
                'category': categories['Best Practices'],
                'published_date': timezone.now().date() - timedelta(days=5),
            },
            {
                'title': 'Building RESTful APIs with Django',
                'author': 'Robert Martinez',
                'content': '''Django REST Framework (DRF) is a powerful toolkit for building Web APIs. It's 
                built on top of Django and provides features like serialization, authentication, permissions, 
                and viewsets that make API development much faster and easier.
                
                Serializers in DRF are similar to Django forms - they handle converting complex data types 
                like Django models into JSON, XML, or other content types. They also handle deserialization, 
                validation, and saving data back to the database.
                
                DRF provides several types of views: function-based views with API decorators, APIView classes 
                for more control, and ViewSets for the most common CRUD operations. ViewSets combined with 
                routers can dramatically reduce the amount of code you need to write.
                
                Authentication and permissions are built-in, supporting everything from basic authentication 
                to OAuth and custom schemes. You can easily control who can access your API and what actions 
                they can perform. The framework also includes throttling to prevent abuse and support for 
                versioning your API.''',
                'category': categories['Technical'],
                'published_date': timezone.now().date() - timedelta(days=2),
            },
            {
                'title': 'Django Security Best Practices',
                'author': 'Lisa Anderson',
                'content': '''Security should be a top priority in any web application. Django provides 
                excellent security features out of the box, but you need to use them correctly and follow 
                best practices to keep your application secure.
                
                Django protects against many common security threats including SQL injection, cross-site 
                scripting (XSS), cross-site request forgery (CSRF), and clickjacking. However, these 
                protections only work if you use Django's features correctly.
                
                Always use Django's template system to render user input - never use string formatting or 
                concatenation. Use parameterized queries through the ORM instead of raw SQL. Enable HTTPS 
                in production and use Django's security middleware.
                
                Keep Django and all dependencies up to date. Use environment variables for sensitive data 
                like SECRET_KEY and database passwords - never commit them to version control. Implement 
                proper authentication and authorization, and use Django's built-in password validation. 
                Regular security audits and staying informed about security bulletins is also crucial.''',
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
            {
                'post': posts[1],
                'name': 'Alice Johnson',
                'email': 'alice@example.com',
                'content': 'Great introduction to Django! This really helped me get started.',
                'is_approved': True,
            },
            {
                'post': posts[1],
                'name': 'Bob Smith',
                'email': 'bob@example.com',
                'content': 'Could you explain more about the ORM in future posts?',
                'is_approved': True,
            },
            {
                'post': posts[2],
                'name': 'Carol White',
                'email': 'carol@example.com',
                'content': 'Template inheritance is such a powerful feature. Thanks for explaining it so clearly!',
                'is_approved': True,
            },
            {
                'post': posts[3],
                'name': 'David Lee',
                'email': 'david@example.com',
                'content': 'URL routing was confusing me, but this post cleared it up. Excellent work!',
                'is_approved': True,
            },
            {
                'post': posts[4],
                'name': 'Eve Taylor',
                'email': 'eve@example.com',
                'content': 'The explanation about collectstatic was very helpful. Thank you!',
                'is_approved': True,
            },
            {
                'post': posts[5],
                'name': 'Frank Miller',
                'email': 'frank@example.com',
                'content': 'I prefer FBVs for their simplicity, but CBVs are great for complex scenarios.',
                'is_approved': False,
            },
            {
                'post': posts[6],
                'name': 'Grace Chen',
                'email': 'grace@example.com',
                'content': 'The ORM tips are gold! This will definitely improve my app performance.',
                'is_approved': True,
            },
        ]
        
        for comment_data in comments_data:
            comment = Comment.objects.create(**comment_data)
            self.stdout.write(f'Created comment by {comment.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all blog data!'))
        self.stdout.write(f'Created {Category.objects.count()} categories')
        self.stdout.write(f'Created {BlogPost.objects.count()} blog posts')
        self.stdout.write(f'Created {Comment.objects.count()} comments')