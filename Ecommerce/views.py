from django.shortcuts import render

# Create your view;s here.
def index(request):
    return render(request,"index.html")