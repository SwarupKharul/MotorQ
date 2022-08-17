from django.contrib import admin
from .models import event_type, attendee, waiting_list

admin.site.register(event_type)
admin.site.register(attendee)
admin.site.register(waiting_list)
