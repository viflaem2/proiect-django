import csv
import json
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Producator, Categorie, Furnizor, TipConexiune, Produs, ImagineProdus

class ProducatorAdmin(admin.ModelAdmin):
    search_fields = ("denumire", "tara_origine")
    search_help_text = "Cauta dupa denumire sau tara de origine."

class CategorieAdmin(admin.ModelAdmin):
    search_fields = ("nume", "descriere")
    search_help_text = "Cauta dupa nume sau descriere."

class FurnizorAdmin(admin.ModelAdmin):
    search_fields = ("denumire", "tara")
    search_help_text = "Cauta dupa denumire sau tara."

class TipConexiuneAdmin(admin.ModelAdmin):
    search_fields = ("denumire", "tip_conector")
    search_help_text = "Cauta dupa denumire sau tipul conectorului."

class ImagineProdusAdmin(admin.ModelAdmin):
    search_fields = ("produs__denumire", "text_alternativ")
    search_help_text = "Cauta dupa denumirea produsului sau textul alternativ."

class ProdusAdmin(admin.ModelAdmin):
    search_fields = ("denumire", "descriere")
    search_help_text = "Cauta dupa denumire sau descriere."
    @admin.display(description="Pret", ordering="pret")
    def pret_formatat(self, obj):
        return format_html('<b style="color: #009b84;">{} lei</b>',obj.pret)
    list_display = ("denumire", "categorie", "pret_formatat", "stoc")
    list_per_page = 5
    list_filter = ("wireless", "furnizor")
    ordering = ("stoc",)
    actions = ['export_csv_produse', 'export_json_produse']
    fieldsets = (
        ('Campuri obligatorii', {
            'fields': ('denumire', 'categorie', 'furnizor', 'pret', 'stoc', 'wireless', 'garantie_luni', 'conexiuni')
        }),
        ('Campuri optionale', {
            'fields': ('descriere', 'greutate_g', 'culori_disponibile', 'taguri'),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description="Exporta produsele selectate in format CSV")
    def export_csv_produse(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="produse.csv"'
        writer = csv.writer(response)
        writer.writerow(['Denumire', 'Pret', 'Stoc', 'Greutate', 'Wireless'])
        for produs in queryset: writer.writerow([produs.denumire,produs.pret,produs.stoc,produs.greutate_g,produs.wireless])
        return response

    @admin.action(description="Exporta produsele selectate in format JSON")
    def export_json_produse(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="produse.json"'
        produse = []
        for produs in queryset:produse.append({'denumire': produs.denumire,'pret': str(produs.pret),'stoc': produs.stoc,'wireless': produs.wireless})
        json.dump(produse, response, ensure_ascii=False, indent=4)
        return response

admin.site.site_header = "Conectel Database"
admin.site.site_title = "Conectel Database"
admin.site.index_title = "Conectel Administration"
admin.site.site_url = "/aplicatie_accesorii_pc/"
admin.site.register(Producator, ProducatorAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Furnizor, FurnizorAdmin)
admin.site.register(TipConexiune, TipConexiuneAdmin)
admin.site.register(Produs, ProdusAdmin)
admin.site.register(ImagineProdus, ImagineProdusAdmin)