from django.contrib import admin
from .models import File, UploadFile

# Register your models here.
admin.site.site_header = "Tashkhees Admin"
admin.site.site_title = "Tashkhees Admin Portal"
admin.site.index_title = "Welcome to Tashkhees Admin Portal"

admin.site.register(File)
admin.site.register(UploadFile)
