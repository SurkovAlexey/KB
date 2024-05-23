from django.shortcuts import render
from APP.forms import ClientPostForm
# Create your views here.

def index(request):
    return render(request, 'main.html')

def contacts(request):
    if request.method == 'POST':
        form = ClientPostForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Ошибка заполнения')
    else:
        form = ClientPostForm()
    return render(request, 'contacts.html', {'form':form})

def about_us(request):
    return render(request, 'about_us.html')