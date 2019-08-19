from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm
import requests, time
from .app_token import app_token, app_version
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def mainpage(request):
	welcome_text = "Hello and welcome to mySite. Add more text to see what happened. Теперь пишу по русски потому что можу"
	context = {"welcome_text": welcome_text}
	return render(request, "newapp/welcome.html", context)


def registerview(request):
	form = UserCreationForm()
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		try:
			if form.is_valid:
				form.save()
				return HttpResponseRedirect("/accounts/login/")
		except ValueError as e:
			err_message = "{}: ".format(e)
			context = {'form': form, "err": err_message}
	context = {'form': form, "err": ''}
	return render(request, 'registration/register.html', context)


def posts(request, form):
	one_day_seconds = 86400
	total_context = []
	if form.is_valid():
		# max count of domain is 3
		domains = {domain.replace(' ','') for domain in form.cleaned_data["public"].split(',') if domain != ''}#[:3]
		offset = 0 if form.cleaned_data["offset"] == None else form.cleaned_data["offset"]
		count = 10 if form.cleaned_data["count"] == None else form.cleaned_data["count"]
		if form.cleaned_data["today_posts"]:
			count = 100
		for domain in domains:
			data_list = []
			response = requests.get("https://api.vk.com/method/wall.get?",
				{"domain": domain,
				"count": count,
				"offset": offset,
				"access_token": app_token,
				"v": app_version
				})
			try:
				json_data = response.json()["response"]["items"]
			except KeyError:
				#TODO: do nothing if some troubles with json
				text_str = "KeyError in " + domain
				data_list.append({"text_data": text_str, "photo_url": [], "doc_url": [], "video_url": []})
				context = {"data": data_list}
				total_context.append(context)
				continue
			owner_id = str(json_data[0]["owner_id"])
			for data in json_data:
				if form.cleaned_data["today_posts"]:
					if data["date"] < (int(time.time())-one_day_seconds):
						continue
				text_str = data["text"]
				photo_list = []
				video_list = []
				doc_list = []
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
			context = {"data": data_list, "domain": domain}
			total_context.append(context)
	return total_context


def multipost(request):
	form = PostForm()
	context = {}
	if request.method == "POST":
		form = PostForm(request.POST)
		context = posts(request, form)
	return render(request, "newapp/content.html", {"total_context": context, "form": form})
