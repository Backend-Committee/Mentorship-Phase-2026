from django.http import HttpResponse
from django.shortcuts import render

# Blogs is a list of (title, content) tuples
blogs = [
    (
        "Koshary",
        "Koshary is Egypt’s most famous street food. It’s made from a mix of rice, lentils, pasta, and chickpeas, topped with spicy tomato sauce, garlic vinegar, and crispy fried onions. It’s filling, cheap, and completely vegetarian.",
    ),
    (
        "Ful Medames",
        "Ful Medames is a traditional Egyptian breakfast dish made from slow-cooked fava beans. It’s usually seasoned with olive oil, lemon juice, garlic, and cumin, and served with bread, eggs, or falafel.",
    ),
    (
        "Taameya (Egyptian Falafel)",
        "Taameya is the Egyptian version of falafel, made from ground fava beans instead of chickpeas. The mixture is flavored with herbs like parsley and coriander, then deep-fried until crispy on the outside and soft inside.",
    ),
    (
        "Molokhia",
        "Molokhia is a green leafy soup made from jute leaves, cooked with garlic and coriander in chicken or meat broth. It’s usually served with rice and chicken or rabbit, and is known for its unique texture.",
    ),
    (
        "Mahshi",
        "Mahshi refers to vegetables like zucchini, peppers, grape leaves, or cabbage stuffed with rice, herbs, and spices. The stuffed vegetables are slowly cooked in tomato sauce or broth until tender.",
    ),
    (
        "Hawawshi",
        "Hawawshi is a popular Egyptian street food made of spiced minced meat stuffed inside baladi bread. It’s baked or grilled until the bread is crispy and the meat is fully cooked.",
    ),
    (
        "Fattah",
        "Fattah is a traditional dish often served on special occasions. It consists of layers of rice, toasted bread, meat, and garlic vinegar tomato sauce. It’s rich, hearty, and very filling.",
    ),
    (
        "Basbousa",
        "Basbousa is a classic Egyptian dessert made from semolina, sugar, yogurt, and butter. After baking, it’s soaked in sugar syrup and often topped with almonds or coconut.",
    ),
]


def home(request):
    return render(request, "home.html", {"blogs": blogs})

def blog(request, id):
    return render(request, "blog.html", {"blog_title": blogs[id][0], "blog_content": blogs[id][1]})