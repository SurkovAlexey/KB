from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

import random
import requests

def index(request):
    return HttpResponse('<h1>Welcome!</h1>')

def current_time(request):
    url = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_time = data['datetime']
        return HttpResponse(f'{current_time}')
    else:
        return HttpResponse(f'error')
    
def random_num(request):
    num1 = random.randint(0,9)
    num2 = random.randint(0,9)
    num3 = random.randint(0,9)

    if num1 == num2 == num3:
        return HttpResponse(f'Победа! Все числа равны: {num1} {num2} {num3}')
    elif num1 == num2 != num3 or num2 == num3 != num1 or num3 == num1 != num2:
        return HttpResponse(f'Ура! Два числа равны: {num1} {num2} {num3}')
    else:
        return HttpResponse(f'Все числа разные, повезет в следующий раз! {num1} {num2} {num3}')

