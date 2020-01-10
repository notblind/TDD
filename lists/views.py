from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
	'''Домашняя страница'''
	return render(request, 'lists/index.html')

