from django.shortcuts import render,HttpResponse,redirect
from .models import City
import requests
from .forms import CityForm

def home(request):
    return render(request,'wapp/home.html')


def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=fe410fd02ccde5e77bc383f2fc2f2f0b'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new = form.cleaned_data['name']
            existing = City.objects.filter(name=new).count()
            if existing == 0:
                r = requests.get(url.format(new)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    try:
        for city in cities:
            r = requests.get(url.format(city)).json()

            city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'humidity' :r['main']['humidity'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
                }
            weather_data.append(city_weather)

        print (weather_data)
    except KeyError:
        pass
    except EXCEPTION as e:
        pass
    context = {'weather_data' : weather_data, 'form' : form, 'message' :message, 'message_class' :message_class}
    return render(request, 'wapp/weather.html', context)


def delete(request,city_name):
        City.objects.get(name=city_name).delete()
        return redirect('weather')