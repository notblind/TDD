from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
	'''Домашняя страница'''
	return HttpResponse('<html><title>Список дел</title></html>')

