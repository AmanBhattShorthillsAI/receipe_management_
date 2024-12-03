# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    peoples = [
        {"name": "John", "age": 30},
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 35},
        {"name": "Charlie", "age": 28},
        {"name": "David", "age": 32},
        {"name": "Eve", "age": 33},
    ]
    # return HttpResponse("""
    #                     <h1>Django Tutorial</h1>
    # <p>Welcome to the Django tutorial!</p>
    # <p>Hi this is the sample django project</p>
    #                     """)
    
    vegetables = [
        'potato', 'tomato', 'onion', 'carrot', 'cabbage',
    ]
    
    
    return render(request, "home/index.html", context={"peoples": peoples, "vegetables": vegetables})


def success(request):
    return HttpResponse("<h1>You have successfully logged in.</h1>")

def about(request):
    return render(request, "home/about.html")

def contact(request):
    return render(request, "home/contact.html")
