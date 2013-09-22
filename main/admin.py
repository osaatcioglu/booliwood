from django.contrib import admin
from booliwood.main.models import Bosta, Location, Source

class BostaAdmin(admin.ModelAdmin):
    pass

class LocationAdmin(admin.ModelAdmin):
    pass

class SourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bosta, BostaAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Source, SourceAdmin)