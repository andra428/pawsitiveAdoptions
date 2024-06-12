from django.contrib import admin
from .models import Contact,Animal,CustomUser, CustomUserIdleId
# Register your models here.
admin.site.register(Contact)
admin.site.register(Animal)
admin.site.register(CustomUser)
admin.site.register(CustomUserIdleId)