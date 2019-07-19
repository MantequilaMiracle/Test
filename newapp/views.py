from django.shortcuts import render
from django.http import HttpResponse
from .forms import WishForm
from .models import Wish
# Create your views here.

def newview(request):
	wishes = Wish.objects.all()
	if request.method == "POST":
		form = WishForm(request.POST)
		if form.is_valid():
			post = form.save(request.POST)
	form = WishForm()
	context = {"form": form, "wishes": wishes}
	return render(request, 'index.html', context)

def deleterecord(request, pk):
	Wish.objects.filter(pk=pk).delete()
	wishes = Wish.objects.all()
	form = WishForm()
	context = {"number": 1, "form": form, "wishes": wishes}
	return render(request, 'index.html', context)
