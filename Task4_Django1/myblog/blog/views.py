from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    data = {
        'name': 'Habiba'
    }
    return render(request, 'blog/home.html', data)
from django.shortcuts import render
from django.http import HttpResponse

POSTS_DATA = [
    {
        'id': 1,
        'title': 'The Blue Sea',
        'content': 'The ocean is vast and beautiful, full of life and mystery.',
        'details': 'The ocean is a vast world covering 70% of Earth. It is home to the Blue Whale, the largest animal ever, and the Great Barrier Reef, the largest living structure visible from space. It regulates our climate and produces half of the worlds oxygen through marine plants.'
    },
    {
        'id': 2,
        'title': 'The Green Forest',
        'content': 'Forests are the heart of nature, filled with trees and wildlife.',
        'details': 'Forests are the Earths lungs. The Amazon Rainforest alone provides 20% of our oxygen. They house 80% of terrestrial biodiversity. From giant Redwoods to tiny mosses, forests are complex ecosystems that protect soil, regulate water cycles, and provide medicine.'
    },
    {
        'id': 3,
        'title': 'The Golden Desert',
        'content': 'Deserts may look empty, but they are rich with unique life.',
        'details': 'Deserts are vibrant ecosystems covering one-fifth of Earths land. The Sahara is the largest hot desert, while Antarctica is the largest cold desert. Creatures like camels and cacti have evolved incredible ways to store water and survive extreme temperature shifts between day and night.'
    },
    {
        'id': 4,
        'title': 'The Snowy Mountains',
        'content': 'Mountains stand tall and proud, touching the clouds.',
        'details': 'Mountains cover 24% of Earths land and are vital water towers, providing fresh water to half of humanity. Mount Everest stands at 8,848 meters, and these peaks influence weather patterns globally, creating unique climates for rare species like the Snow Leopard and Mountain Gorilla.'
    },
    {
        'id': 5,
        'title': 'The Silent River',
        'content': 'Rivers flow gently, connecting lands and people together.',
        'details': 'Rivers are the lifeblood of civilizations. The Nile is historically the longest, while the Amazon carries the most water. They carve landscapes over millions of years, provide transport, and are essential for agriculture, supporting thousands of unique fish species and providing drinking water.'
    }
]

def BlogList(request):
    return render(request, 'blog/blog_list.html', {'posts': POSTS_DATA})

def BlogDetails(request, id):
    post = None
    for p in POSTS_DATA:
        if p['id'] == id:
            post = p
            break

    if post is None:
        return HttpResponse("Post not found")
        
    return render(request, 'blog/blog_details.html', {'post': post})