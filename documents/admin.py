from django.contrib import admin
from documents.models import Document, Note

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Document, DocumentAdmin)
admin.site.register(Note)
