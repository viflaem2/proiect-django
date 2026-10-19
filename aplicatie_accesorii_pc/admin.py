from django.contrib import admin
from .models import Producator, Categorie, Furnizor, TipConexiune, Produs, ImagineProdus

admin.site.register(Producator)
admin.site.register(Categorie)
admin.site.register(Furnizor)
admin.site.register(TipConexiune)
admin.site.register(Produs)
admin.site.register(ImagineProdus)