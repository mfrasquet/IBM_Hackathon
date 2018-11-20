from django.contrib import admin
from .models import Contract
# Register your models here.


# Re-register UserAdmin
admin.site.register(Contract)