from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse


from .models import Item
# Create your views here.


def index(request):
	'''Домашняя страница'''
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('index')
	items = Item.objects.all()
	return render(request, 'lists/index.html', {'items': items})

