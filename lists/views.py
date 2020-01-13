from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse


from .models import Item
# Create your views here.


def index(request):
	'''Домашняя страница'''
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('view_list')
	items = Item.objects.all()
	return render(request, 'lists/index.html')

def view_list(request):
	'''Предствалние списка'''
	items = Item.objects.all()
	return render(request, 'lists/list.html', {'items': items})


