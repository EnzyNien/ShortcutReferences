from django.contrib import admin
from django.utils.html import format_html
import datetime
from mainapp.models import ReferencesToLinks, ShortcutRef


class ReferencesToLinksInlines (admin.TabularInline):
    model = ReferencesToLinks
    extra = 3


class ShortcutRefAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_date'
    list_filter = ['real_url', 'short_url',]
    search_fields = ['real_url', 'short_url',]
    readonly_fields = ('short_url','real_url',)
    inlines = [
       ReferencesToLinksInlines,]


admin.site.register(ShortcutRef, ShortcutRefAdmin)



