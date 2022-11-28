from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import City
from .forms import CityForm

def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=29596879d1fd8cce09818b03b7368e66'
	weather_data = []
	cities = City.objects.all()
	form = CityForm()
	

	if request.method == 'POST': # only true if form is submitted
		form = CityForm(request.POST) # add actual request data to form for processing
		if form.is_valid():
			form.save() # will validate and save if validate

	try:
		for city in cities:
			city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

			weather = {
				'city' : city,
				'temperature' : city_weather['main']['temp'],
				'description' : city_weather['weather'][0]['description'],
				'icon' : city_weather['weather'][0]['icon']
			}
		weather_data.append(weather)

	except:
		return HttpResponse("<h5>Not Found</h5>")


   

	# print(city_weather)
	context = {'weather_data':weather_data, 'form':form, 'cities':cities}#add the data for the current city into our list
	return render(request, 'weatherapp/index.html', context)
