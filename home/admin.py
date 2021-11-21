from django.contrib import admin

from .models import *
from martor.widgets import AdminMartorWidget

class NewFeedAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': AdminMartorWidget},
	}

# Register your models here.
admin.site.register(TKB)
admin.site.register(NewFeed, NewFeedAdmin)