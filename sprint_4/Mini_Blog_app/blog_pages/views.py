from django.shortcuts import render

# Create your views here.

blogs = [
    {
        'id': 1,
        'title': 'The Future of Remote Work: Strategies for 2026',
        'content': 'As we navigate through 2026, remote work has evolved from a temporary solution to a permanent lifestyle for many professionals. The key to thriving in this environment is establishing a rigid boundary between your workspace and personal life. Investing in an ergonomic setup and utilizing asynchronous communication tools can drastically improve both your mental health and daily output.',
        'author': 'Sarah Jenkins',
        'date': 'Feb 10, 2026'
    },
    {
        'id': 2,
        'title': 'Embracing Minimalism in Modern Web Design',
        'content': 'In an era of information overload, minimalist web design offers a breath of fresh air. By stripping away unnecessary elements and focusing on core functionality, developers can create faster, more accessible, and highly intuitive user interfaces. A minimalist approach does not mean boring; it means purposeful design where every pixel serves the user\'s journey.',
        'author': 'David Chen',
        'date': 'Feb 12, 2026'
    },
    {
        'id': 3,
        'title': 'The Power of Continuous Learning in the Tech Industry',
        'content': 'The technology landscape shifts rapidly, and the skills that got you hired yesterday might not be sufficient tomorrow. Cultivating a habit of continuous learning—whether through reading documentation, contributing to open-source projects, or taking online courses—is essential. It is not just about staying relevant; it is about maintaining a sense of curiosity and passion for your craft.',
        'author': 'Elena Rodriguez',
        'date': 'Feb 14, 2026'
    },
    {
        'id': 4,
        'title': 'Cybersecurity Best Practices for Modern Developers',
        'content': 'As digital threats become more sophisticated, security can no longer be an afterthought in software development. Implementing robust authentication, encrypting sensitive data, and regularly updating dependencies are non-negotiable practices. A proactive approach to cybersecurity not only protects user privacy but also preserves the integrity and reputation of your organization.',
        'author': 'Michael Chang',
        'date': 'Feb 16, 2026'
    },
    {
        'id': 5,
        'title': 'Integrating AI into Everyday Applications',
        'content': 'Artificial Intelligence is transitioning from specialized research labs to mainstream consumer applications. By leveraging accessible APIs and pre-trained models, developers can easily add features like natural language processing and predictive analytics to their projects. The challenge now lies in creating intuitive user experiences that harness this power without overwhelming the end-user.',
        'author': 'Sophia Patel',
        'date': 'Feb 18, 2026'
    },
    {
        'id': 6,
        'title': 'Why Effective Code Reviews Matter',
        'content': 'Code reviews are more than just a bug-catching mechanism; they are a vital tool for knowledge sharing and maintaining code quality. A positive review culture encourages constructive feedback, mentorship, and collective ownership of the codebase. By taking the time to thoroughly review peer contributions, teams can significantly reduce technical debt and build more resilient software.',
        'author': 'James Wilson',
        'date': 'Feb 20, 2026'
    }
]

def Home(request):
    return render(request, 'blog_pages/home.html')

def BlogList(request):
    return render(request, 'blog_pages/Blog list.html', {'blogs': blogs})

def BlogDetail(request, blog_id):
    return render(request, 'blog_pages/Blog details.html', {'blog': blogs[blog_id-1]})


# def BlogDetail(request, blog_id):
#     return render()


