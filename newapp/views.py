#django staff import
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


#forms import
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm


#models import
from .models import ProfileHistory
from django.contrib.auth.models import User


#other lib import
import requests, time
from .app_token import app_token, app_version


def mainpage(request):
	#TODO: show suggestions what domains to use
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
			err_message = "Error: {}".format(e)
			context = {'form': form, "err": err_message}
	context = {'form': form, "err": ''}
	return render(request, 'registration/register.html', context)


@login_required
def profile(request):
	#TODO: need to show history to an authenticated user
	welcome_text = "Hello and welcome to mySite, "
	#history = ProfileHistory.objects.get(history=request.user)
	context = {"welcome_text": welcome_text}
	return render(request, "registration/profile.html", context)


def post(domain, today_posts):
	'''
	#the method using VK API method "wall.get" to get a json response with
	#wall posts attachments.
	#Returns dictionary with data_list and domain.
	#data_list contains text_data, photo_url, doc_url, video_url.
	'''
	count = 10
	offset = 0
	one_day_seconds = 86400
	context = {}
	if today_posts:
		count = 100
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
	except KeyError as e:
		#print(e)
		data_list.append({"text_data": "Check the domain name", "photo_url": [], "doc_url": [], "video_url": []})
		context = {"data": data_list}
		return context
	owner_id = str(json_data[0]["owner_id"])
	for data in json_data:
		if today_posts:
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
		except KeyError as e:
			#print(e)
			continue
		data_list.append({"text_data": text_str, "photo_url": photo_list, "doc_url": doc_list, "video_url": video_list})
	context = {"data": data_list, "domain": domain}
	return context


def multipost(request):
	form = PostForm()
	context = {}
	total_context = []
	request.session.set_expiry(600)
	if request.method == "GET":
		try:
			if request.session["domains"]:
				for domain in request.session["domains"]:
					total_context.append(post(domain, request.session["today_posts"]))
				return render(request, "newapp/content.html", {"total_context": total_context, "form": form})
		except KeyError:
			pass
	if request.method == "POST":
		total_context = []
		form = PostForm(request.POST)
		if form.is_valid():
			domains = [domain for domain in [form.cleaned_data["public%i"%i].replace(' ', '') for i in range(1,4)] if domain != '']
			request.session["domains"] = domains
			today_posts = form.cleaned_data["today_posts"]
			request.session["today_posts"] = today_posts
			if request.user.is_authenticated:
				ph = ProfileHistory(request.user, domains=', '.join(domains), filters=today_posts)
				ph.save()
			for domain in domains:
				total_context.append(post(domain, today_posts))
	return render(request, "newapp/content.html", {"total_context": total_context, "form": form})
#TODO: something goes wrong with ProfileHistory
