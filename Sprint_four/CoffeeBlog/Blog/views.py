from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def blog_list(request):
    blogs = [
        {
            "id": 1,
            "title": "Arabica Beans",
            "content": "Arabica coffee beans are known for their smooth and complex flavor profile..."
        },
        {
            "id": 2,
            "title": "Robusta Beans",
            "content": "Robusta beans are stronger, more bitter, and contain more caffeine..."
        },
        {
            "id": 3,
            "title": "Single Origin Coffee",
            "content": "Single origin coffee comes from one region and offers unique taste notes..."
        }
    ]

    return render(request, "pages/blog_list.html", {"blogs": blogs})


def blog_detail(request, blog_id):
    blogs = [
        {
            "id": 1,
            "title": "Arabica Beans",
            "content": "Arabica coffee beans are smooth and aromatic...",
            "author": "Yousef"
        },
        {
            "id": 2,
            "title": "Robusta Beans",
            "content": "Robusta beans are stronger and more bitter...",
            "author": "Yousef"
        },
    ]

    blog = None
    for b in blogs:
        if b["id"] == blog_id:
            blog = b
            break

    return render(request, "pages/blog_detail.html", {"blog": blog})
def home(request):
    return render(request, 'pages/home.html')