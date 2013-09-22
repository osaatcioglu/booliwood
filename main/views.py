from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed
from booli import booliwood
from models import add_bosta, get_all_bostas, Bosta
from django import forms
import time

class BostaForm(forms.Form):
    maxPrice = forms.IntegerField()
    livingArea = forms.IntegerField()
    room = forms.IntegerField()

class BostaIdForm(forms.Form):
    bostaId = forms.IntegerField()

class SearchBosta(forms.Form):
    search_query = forms.CharField()

def show(request):
	if request.method == 'POST':
		form = BostaForm(request.POST)
		if form.is_valid():
			maxPrice = form.cleaned_data['maxPrice']
			livingArea = form.cleaned_data['livingArea']
			room = form.cleaned_data['room']
			bostas = Bosta.objects \
			.filter(listPrice__lte=maxPrice) \
			.filter(livingArea__gte=livingArea) \
			.filter(rooms__gte=room) \
			.exclude(listPrice=0) \
			.order_by('soldDate') 
	else:
		form = BostaForm()
		bostas = get_all_bostas()
	for bosta in bostas:
		if bosta.livingArea == 0:
			bosta.sek_m2 = 0
		elif bosta.soldPrice == 0:
			bosta.sek_m2 = bosta.listPrice / bosta.livingArea
		else:
			bosta.sek_m2 = bosta.soldPrice / bosta.livingArea

	data = { 
	'bostas': bostas,
	'form': form,
	}
	return render(request, 'main.html', data)

def update(request):
	totalListing = 0
	totalSold = 0
	form = SearchBosta()
	data = {
	'totalListing': totalListing,
	'totalSold': totalSold,
	'countListing': 0,
	'countSold': 0,
	'form': form
	}
	if request.method == 'POST':
		form = SearchBosta(request.POST)
		if form.is_valid():
			q = form.cleaned_data['search_query'].encode('utf8')
			d1 = search("listings", q)
			if d1:
				data['totalListing'] = d1['total']
				data['countListing'] = d1['count']
			d1 = search("sold", q)
			if d1:
				data['totalSold'] = d1['total']
				data['countSold'] = d1['count']

	return render(request, 'update.html', data)

def search(type_search, q):
	total = 0
	while True:
		result = booliwood(q, total, 50, type_search)
		for listing in result[type_search]:
			add_bosta(listing)
		total = total + result['count']
		if total >= result['totalCount']:
			break
		time.sleep(1)
	data = {
	'total': total,
	'count': result['totalCount'],
	}
	return data

