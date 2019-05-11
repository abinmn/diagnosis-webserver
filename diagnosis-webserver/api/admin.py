from django.contrib import admin
from api.models import Profile, SerialData, Data, Endpoint_Check

# Register your models here.
admin.site.register(Profile)
admin.site.register(SerialData)
admin.site.register(Data)
admin.site.register(Endpoint_Check)