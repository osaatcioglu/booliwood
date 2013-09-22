from django.db import models
import time
import dateutil.parser

class Location(models.Model):
	namedAreas = models.CharField(max_length=250)
	municipalityName = models.CharField(max_length=250)
	countyName = models.CharField(max_length=250)
	streetAddress = models.CharField(max_length=250)
	lat = models.DecimalField(max_digits=10, decimal_places=8)
	lon = models.DecimalField(max_digits=10, decimal_places=8)

class Source(models.Model):
	name = models.CharField(max_length=250)
	url = models.CharField(max_length=250)
	type_source = models.CharField(max_length=250)

class Bosta(models.Model):
	booliId = models.IntegerField()
	listPrice = models.IntegerField()
	published = models.DateField()
	location = models.ForeignKey('Location')
	objectType = models.CharField(max_length=250)
	source = models.ForeignKey('Source')
	rooms = models.PositiveSmallIntegerField()
	floor = models.PositiveSmallIntegerField()
	livingArea = models.PositiveSmallIntegerField()
	rent = models.PositiveIntegerField()
	constructionYear = models.PositiveSmallIntegerField()
	url = models.CharField(max_length=250)
	soldPrice = models.IntegerField()
	soldDate = models.DateField()


def add_bosta(listing):
	bostas = Bosta.objects.filter(booliId=listing['booliId'])
	if not bostas:
		bosta = Bosta()
		bosta.booliId = listing['booliId']
		bosta.listPrice = listing['listPrice'] if 'listPrice' in listing else 0
		bosta.published = dateutil.parser.parse(listing['published']) if 'published' in listing else dateutil.parser.parse('1453')
		bosta.location = add_location(listing['location'])
		bosta.objectType = listing['objectType'] if 'rooms' in listing else 0
		bosta.source = add_source(listing['source'])
		bosta.rooms = listing['rooms'] if 'rooms' in listing else 0
		bosta.floor = listing['floor'] if 'floor' in listing else 0
		bosta.livingArea = listing['livingArea'] if 'livingArea' in listing else 0
		bosta.rent = listing['rent'] if 'rent' in listing else 0
		bosta.constructionYear = listing['constructionYear'] if 'constructionYear' in listing else "1453"
		bosta.url = listing['url']
		bosta.soldPrice = listing['soldPrice'] if 'soldPrice' in listing else 0
		bosta.soldDate = dateutil.parser.parse(listing['soldDate']) if 'soldDate' in listing else dateutil.parser.parse('1453')
		bosta.save()
	else:
		bosta = bostas[0]
		if bosta.soldPrice == 0:
			bosta.soldPrice = listing['soldPrice'] if 'soldPrice' in listing else 0
			bosta.soldDate = dateutil.parser.parse(listing['soldDate']) if 'soldDate' in listing else dateutil.parser.parse('1453')
			bosta.save()
	return bosta

def add_source(source_json):
	source = Source.objects.filter(name=source_json['name'])
	if source and len(source) > 0:
		return source[0]
	else:
		source = Source()
		source.name = source_json['name']
		source.url = source_json['url']
		source.type_source = source_json['type']
		source.save()
		return source

def add_location(location_json):
	location = Location.objects.filter(lat=location_json['position']['latitude']).filter(lon=location_json['position']['longitude'])
	if location and len(location) > 0:
		return location[0]
	else:
		location = Location()
		location.namedAreas = location_json['namedAreas']
		location.municipalityName = location_json['region']['municipalityName']
		location.countyName = location_json['region']['countyName']
		location.streetAddress = location_json['address']['streetAddress']
		location.lat = location_json['position']['latitude']
		location.lon = location_json['position']['longitude']
		location.save()
		return location

def get_all_bostas():
	return Bosta.objects.all()
