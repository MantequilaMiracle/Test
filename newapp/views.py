from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import WishForm
from .models import Wish
import requests
# Create your views here.
def mainpage(request):
	welcome_text = "Hello and welcome to mySite. Add more text to see what happened. Теперь пишу по русски потому что можу"
	context = {"welcome_text": welcome_text}
	return render(request, "newapp\welcome.html", context)

def pikabutake(request):
	app_token = "1e732df61e732df61e732df6c61e18fb5b11e731e732df6434546886b716328dd5fd619"
	domain = "pikabu"
	count = 10
	offset = 0
	v = 5.101
	response = requests.get("https://api.vk.com/method/wall.get?",
		{"domain": domain,
		"count": count,
		"offset": offset,
		"access_token": app_token,
		"v": v
		})
	json_data = response.json()["response"]["items"]
	#text_data = []
	#photo_url = []
	data_list = []
	for data in json_data:
		text_str = data["text"]
		photo_list = []
		#photo_for_text = []
		try:
			for attachment in data["attachments"]:
				if attachment["type"] == "photo":
					photo_for_the_text = attachment["photo"]["sizes"][-1]["url"]
					photo_list.append(photo_for_the_text)
				else:
					continue
		except KeyError:
			continue
		#photo_url.append(photo_for_text)
		data_list.append({"text_data": text_str, "photo_url": photo_list})

	#context = {"text_data": text_data, "photo_url": photo_url, "amount_of_data": amount_of_data}
	context = {"data": data_list}
	return render(request, "newapp/content.html", context)
