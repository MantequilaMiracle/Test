from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm
import requests, time
from .app_token import app_token, app_version
# Create your views here.
def mainpage(request):
	welcome_text = "Hello and welcome to mySite. Add more text to see what happened. Теперь пишу по русски потому что можу"
	context = {"welcome_text": welcome_text}
	return render(request, "newapp\welcome.html", context)

def posts(request):
	data_list = []
	one_day_seconds = 86400
	first_enter = True
	if request.method == "POST":
		first_enter = False
		form = PostForm(request.POST)
		if form.is_valid():
			domain = form.cleaned_data["public"]
			offset = 0 if form.cleaned_data["offset"] == None else form.cleaned_data["offset"]
			count = 10 if form.cleaned_data["count"] == None else form.cleaned_data["count"]
			if form.cleaned_data["today_posts"]:
				count = 100
			response = requests.get("https://api.vk.com/method/wall.get?",
				{"domain": domain,
				"count": count,
				"offset": offset,
				"access_token": app_token,
				"v": app_version
				})
			json_data = response.json()["response"]["items"]
			owner_id = str(json_data[0]["owner_id"])
			for data in json_data:
				if form.cleaned_data["today_posts"]:
					if data["date"] < (int(time.time())-one_day_seconds):
						continue
				text_str = data["text"]
				photo_list = []
				video_list = []
				doc_list = []
				temp = ""
				try:
					for attachment in data["attachments"]:
						if attachment["type"] == "photo":
							temp = attachment["photo"]["sizes"][-1]["url"]
							photo_list.append(temp)
						elif attachment["type"] == "doc":
							temp = attachment["doc"]["url"]
							doc_list.append(temp)
						elif attachment["type"] == "video":
							#https://vk.com/video+owner_id+_+456288678
							video_id = str(attachment["video"]["id"])
							temp = "https://vk.com/video" + owner_id + "_" + video_id
							video_list.append(temp)
						#TODO: VIDEO
						else:
							continue
				except KeyError:
					continue
				data_list.append({"text_data": text_str, "photo_url": photo_list, "doc_url": doc_list, "video_url": video_list})
	form = PostForm()
	context = {"data": data_list, "form": form, "first_enter": first_enter}
	return context

def multipost(request):
	number_of_domain = 0
	context = []

	context = posts(request)
	return render(request, "newapp/content.html", context)
