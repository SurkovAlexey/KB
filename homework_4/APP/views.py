from django.shortcuts import render
from django.http import HttpResponse, FileResponse
# Create your views here.

def index(request):
    return HttpResponse('<h1>Welcome to my site!</hq>')

def file_1(request):
    return FileResponse(open('APP/Images/file1.jpg','rb'))
def file_2(request):
    return FileResponse(open('APP/Images/file2.jpg','rb'))
def file_3(request):
    return FileResponse(open('APP/Images/file3.jpg','rb'))

def help_to_choice(request,age):
    try:
        age = int(age)
        if 1 <= age <= 14:
            return HttpResponse(f'Вам {age} лет, Вам подходит курс Scratch ')
        elif 15 <= age <= 18:
            return HttpResponse(f'Вам {age} лет, Вам подходит курс Python Basic ')
        elif 19 <= age <= 25:
            return HttpResponse(f'Вам {age} лет, Вам подходит курс Python Advanced ')
        elif 26 <= age <= 40:
            return HttpResponse(f'Вам {age} лет, Вам подходит курс Python Data Science ')
        elif 41 <= age <= 100:
            return HttpResponse(f'Вам {age} лет, Вам не нужно учиться, Вы уже сами можете обучать ')
        else:
            return HttpResponse('Введите корректный возраст')
    except ValueError:
        return HttpResponse('Введите возраст в формате десятичного числа ')