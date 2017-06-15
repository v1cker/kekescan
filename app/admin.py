from django.contrib import admin
from app import models

class DomainBeian(admin.ModelAdmin):
    pass

 

admin.site.register(models.DomainBeian, DomainBeian)
 