from django.contrib import admin
from models import UploadFile, TranslatedFile, Language

# Register your models here.
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'upload_time')
    list_filter = ('upload_time',)
    date_hierarchy = 'upload_time'
    ordering = ('-upload_time',)
    
class TranslatedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'trans_time')
    list_filter = ('trans_time',)
    date_hierarchy = 'trans_time'
    ordering = ('-trans_time',)
    
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language','language_chinese', 'language_code')
    
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(TranslatedFile, TranslatedFileAdmin)
admin.site.register(Language, LanguageAdmin)
