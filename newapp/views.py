from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm
import requests
from .app_token import app_token, app_version
# Create your views here.
def mainpage(request):
	welcome_text = "Hello and welcome to mySite. Add more text to see what happened. Теперь пишу по русски потому что можу"
	context = {"welcome_text": welcome_text}
	return render(request, "newapp\welcome.html", context)

def pikabutake(request):
	domain = "pikabu"
	count = 10
	offset = 0
	response = requests.get("https://api.vk.com/method/wall.get?",
		{"domain": domain,
		"count": count,
		"offset": offset,
		"access_token": app_token,
		"v": app_version
		})
	json_data = response.json()["response"]["items"]
	data_list = []
	for data in json_data:
		text_str = data["text"]
		photo_list = []
		try:
			for attachment in data["attachments"]:
				if attachment["type"] == "photo":
					photo_for_the_text = attachment["photo"]["sizes"][-1]["url"]
					photo_list.append(photo_for_the_text)
				else:
					continue
		except KeyError:
			continue
		data_list.append({"text_data": text_str, "photo_url": photo_list})

	context = {"data": data_list}
	return render(request, "newapp/content.html", context)

def posts(request):
	data_list = []
	first_enter = True
	if request.method == "POST":
		first_enter = False
		form = PostForm(request.POST)
		if form.is_valid():
			if form.cleaned_data["today_posts"]:
				pass #TODO today posts
			domain = form.cleaned_data["public"]
			offset = form.cleaned_data["offset"]
			count= form.cleaned_data["count"]
			response = requests.get("https://api.vk.com/method/wall.get?",
				{"domain": domain,
				"count": count,
				"offset": offset,
				"access_token": app_token,
				"v": app_version
				})
			json_data = response.json()["response"]["items"]
			for data in json_data:
				text_str = data["text"]
				photo_list = []
				try:
					for attachment in data["attachments"]:
						if attachment["type"] == "photo":
							photo_for_the_text = attachment["photo"]["sizes"][-1]["url"]
							photo_list.append(photo_for_the_text)
						else:
							continue
				except KeyError:
					continue
				data_list.append({"text_data": text_str, "photo_url": photo_list})
	form = PostForm()
	context = {"data": data_list, "form": form, "first_enter": first_enter}
	return render(request, "newapp/alt_content.html", context)
