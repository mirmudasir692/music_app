from django.shortcuts import render, HttpResponse

# Create your views here.


def artists(request):
    return HttpResponse("you are at artists page")
