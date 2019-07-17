from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def newview(request):
	context = {"number": 1}
	return render(request, 'index.html', context)
