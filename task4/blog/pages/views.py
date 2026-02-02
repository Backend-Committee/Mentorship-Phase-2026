from django.shortcuts import render

def home(request):
    home = {'name' :'home'}
    return render(request, 'pages/home.html',home)
def blogList(request):
    bloglist = {
        'name':'blogList',
        'blogs':[
            {'title':'Blog Post 1', 'author':'Author 1'},
            {'title':'Blog Post 2', 'author':'Author 2'},
            {'title':'Blog Post 3', 'author':'Author 3'},]
                }
    return render(request, 'pages/blogList.html',bloglist)
def blogDetails(request):
    blogdetails = {'name':'blogDetails'}
    return render(request,'pages/blogDetails.html',blogdetails)
# Create your views here.
