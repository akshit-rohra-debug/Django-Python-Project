from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
from . import models

def index(request):
    return render(request, 'classify/index.html')

def amazon(request):
    a, c_mat = models.accuracy_amazon()
    context={
        "accuracy" : a,
        "w": c_mat[0][0],
        "x": c_mat[0][1],
        "y": c_mat[1][0],
        "z": c_mat[1][1]
    }
    if request.method=="POST":
        comment=request.POST.get('comment')
        if comment=="":
            return render(request, 'classify/amazon.html', context)
        context={
            "result" : models.predict_amazon(comment),
            "comment" : comment
        }
        return render(request,'classify/predict.html',context)
    return render(request,'classify/amazon.html', context)

def imdb(request):
    a, c_mat = models.accuracy_imdb()
    context = {
        "accuracy": a,
        "w": c_mat[0][0],
        "x": c_mat[0][1],
        "y": c_mat[1][0],
        "z": c_mat[1][1]
    }
    if request.method == "POST":
        comment = request.POST.get('comment')
        if comment=="":
            return render(request, 'classify/imdb.html', context)
        context = {
            "result": models.predict_imdb(comment),
            "comment": comment
        }
        return render(request, 'classify/predict.html', context)
    return render(request,'classify/imdb.html',context)

def yelp(request):
    a, c_mat = models.accuracy_yelp()
    context = {
        "accuracy": a,
        "w": c_mat[0][0],
        "x": c_mat[0][1],
        "y": c_mat[1][0],
        "z": c_mat[1][1]
    }
    if request.method == "POST":
        comment = request.POST.get('comment')
        if comment=="":
            return render(request, 'classify/yelp.html', context)
        context = {
            "result": models.predict_yelp(comment),
            "comment": comment
        }
        return render(request, 'classify/predict.html', context)
    return render(request,'classify/yelp.html',context)