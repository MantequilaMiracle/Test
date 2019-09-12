#django staff import
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


#forms import
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm, UserProfileForm#, SearchForm


#models import
from .models import ProfileHistory
from django.contrib.auth.models import User


#other lib import
import requests, time
from .app_token import app_token, app_version


#constants
ONE_DAY_SECONDS = 86400


def mainpage(request):
	#TODO: show suggestions what domains to use
	context = {"text": '''Web site
	Trying to create web site with purpose to practice and get knowledge how does it work.
	Also I want to study Django how the most popular framework for site creature.'''}
	return render(request, "newapp/mainpage.html", context)


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
	#TODO: need to add some features
	form = UserProfileForm()
	current_user = User.objects.get(username=request.user.username)
	if request.method == "POST":
		print("berfore valid")
		form = UserProfileForm(request.POST)
		if form.is_valid():
			print("after valid")
			if not current_user.first_name:
				current_user.first_name = form.cleaned_data['first_name']
			if not current_user.last_name:
				current_user.last_name = form.cleaned_data['last_name']
			if not current_user.email:
				current_user.email = form.cleaned_data['email']
			current_user.save()
			return HttpResponseRedirect("/accounts/profile/")
	welcome_text = "Hello and welcome to mySite, "
	context = {"welcome_text": welcome_text, "form": form}
	return render(request, "registration/profile.html", context)

@login_required
def history(request):
	'''shows history to an authenticated user'''
	history_user = ProfileHistory.objects.filter(username=request.user.username)
	history_domains = [ph.domains for ph in history_user]
	history_date = [ph.date for ph in history_user]
	context = {"history": dict(zip(history_domains, history_date))}
	return render(request, "registration/history.html", context)


@login_required
def history_flush(request):
	ProfileHistory.objects.filter(username=request.user.username).delete()
	return HttpResponseRedirect("/accounts/profile/history")


@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")


#TODO: User authorization over VK form
'''
def publicSearch(request):
	form = SearchForm()
	type = "group"
	sort = 0
	count = 10
	offset = 0
	q = ""
	context = {"data": [], "form": form}
	data_list = []
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			q = form.cleaned_data["q"]
			response = requests.get("https://api.vk.com/method/groups.search?",
				{"q": q,
				"type": type,
				"sort": sort,
				"count": count,
				"offset": offset,
				"access_token": app_token,
				"v": app_version
				})
			print(response)
			json_data = response.json()
			print(json_data)
			if "error" in json_data:
				context = {"err": "Error code: %i. "%json_data["error"]["error_code"] + json_data["error"]["error_msg"]}
				return context
			json_data = json_data["response"]["items"]
			for data in json_data:
				search_data = {"name": data["name"], "domain": data["screen_name"],
				"photo": data["photo_100"]}
				data_list.append(search_data)
			print(data_list)
			context = {"data": data_list, "form": form}
		else:
			context = {"err": "something wrong with form"}
	return render(request, "newapp/search_results.html", context)
'''

def post(domain, today_posts):
	'''
	#the method using VK API method "wall.get" to get a json response with
	#wall posts attachments.
	#Returns dictionary with data_list and domain.
	#data_list contains text_data, photo_url, doc_url, video_url.
	'''
	count = 10
	offset = 0
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
	json_data = response.json()
	if "error" in json_data:
		data_list.append({"text_data": "Error code: %i. "%
		json_data["error"]["error_code"] + json_data["error"]["error_msg"]})

		context = {"data": data_list}
		return context
	json_data = json_data["response"]["items"]
	owner_id = str(json_data[0]["owner_id"])
	for data in json_data:
		if today_posts:
			if data["date"] < (int(time.time())-ONE_DAY_SECONDS):
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
		data_list.append({"text_data": text_str, "photo_url": photo_list,
							"doc_url": doc_list, "video_url": video_list})
	context = {"data": data_list, "domain": domain}
	return context


def multipost(request):
	form = PostForm()
	context = {}
	total_context = []
	request.session.set_expiry(1200)
	if request.method == "GET":
		if "domains" in request.session:
			for domain in request.session["domains"]:
				total_context.append(post(domain, request.session["today_posts"]))
			return render(request, "newapp/content.html",
							{"total_context": total_context, "form": form})
	if request.method == "POST":
		total_context = []
		form = PostForm(request.POST)
		if form.is_valid():
			domains = [domain for domain in [form.cleaned_data["public%i"%i].replace(' ', '') for i in range(1,4)] if domain != '']
			request.session["domains"] = domains
			today_posts = form.cleaned_data["today_posts"]
			request.session["today_posts"] = today_posts
			if request.user.is_authenticated:
				loggedUserObject = User.objects.get(username=request.user.username)
				ProfileHistory.objects.create(user_id=loggedUserObject,
				username=loggedUserObject.username, domains=', '.join(domains), filters=today_posts)
			for domain in domains:
				total_context.append(post(domain, today_posts))
	return render(request, "newapp/content.html", {"total_context": total_context, "form": form})
