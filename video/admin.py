from django.contrib import admin
from .models import Comments,History,Video,Channel,Library

admin.site.register(Comments)
admin.site.register(History)
admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Library)

