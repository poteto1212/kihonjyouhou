from django.contrib import admin
from .models import Zone,Subject,Field,Detail


class ZoneAdmin(admin.ModelAdmin):
    list_display=('zones','num')
    list_editable=('num',)
    ordering=('num',)
    save_as=True
    search_fields=['zones','num']
    
class SubjectAdmin(admin.ModelAdmin):
    list_display=('zone','subjcs','subjctsnum')
    list_editable=('subjcs','subjctsnum')
    ordering=('subjctsnum',)
    save_as=True
    list_filter=('zone__zones',)
    search_fields=['zone','subjcs','subjctsnum']
    raw_id_fields=('zone',)
    
class FieldAdmin(admin.ModelAdmin):
    list_display=('subjct','subjct_zone_zones','fields','fieldnum')
    list_editable=('fields','fieldnum')
    list_filter=('subjct__zone__zones','subjct__subjcs')
    save_as=True
    ordering=('fieldnum',)
    search_fields=['subjct','fields','fieldnum']
    raw_id_fields=('subjct',)
    
    
    #foringkey表示メソッド
    def subjct_zone_zones(self,obj):
        return obj.subjct.zone.zones
        
class DetailAdmin(admin.ModelAdmin):
    list_display=('field_subjct_subjcs','field','title','questionnum','answernum1','answernum2','answernum3')
    list_editable=('field','title','questionnum','answernum1','answernum2','answernum3')
    list_filter=('field__subjct__zone__zones','field__subjct__subjcs','field__fields')
    save_as=True
    ordering=('questionnum',)
    search_fields=['field__subjct__zone__zones','field__subjct__subjcs','field__fields']
    raw_id_fields=('field',)
    filter_horizontal=('relation',)
    
    def field_subjct_subjcs(self,obj):
        return obj.field.subjct.subjcs
    
# Register your models here.
admin.site.register(Zone,ZoneAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Field,FieldAdmin)
admin.site.register(Detail,DetailAdmin)