from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def main(request):
    return render(request,'base.html')

def code(request):
    return render(request,'code.html')

def bigdata(request):
    return render(request,'bigdata.html')

def ii(request):
    return render(request,'ii.html')

def cloud(request):
    return render(request,'cloud.html')

def secure(request):
    return render(request,'secure.html')