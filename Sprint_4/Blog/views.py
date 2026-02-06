import json
import random
from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import requests as req
from django.http import HttpResponse
# Create your views here.


def index(request):
    file_path = Path(settings.BASE_DIR) / "Blog"/"poems.json"

    if not file_path.exists():
        return HttpResponse("File not found!", status=404)

    with open(file_path , 'r' ,encoding='utf-8' )as file:
        data = json.load(file)

    id = int(random.random() * 8) + 1
    poem = None
    for i in data:
        if i['id'] == id:
            poem = i

    context = {'content': poem['content'],
               'title': poem['title']
        ,'meter': poem['meter'] , 'rhyme': poem['rhyme'] , 'theme': poem['theme']}
    return render(request, 'Blog/index.html' , context)



def poets (request):
    file_path = Path(settings.BASE_DIR) / "Blog"/"Poets.json"

    if not file_path.exists():
        return HttpResponse("File not found!", status=404)

    with open(file_path , 'r' ,encoding='utf-8' )as file:
        data = json.load(file)

    context = {'poets': data}
    return render(request, 'Blog/Poets.html' , context)