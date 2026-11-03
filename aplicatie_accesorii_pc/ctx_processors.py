from django.conf import settings
from .models import Categorie

def procesare(request):
    return {
        "detalii_firma": settings.DETALII_FIRMA,
        "stoc_min": settings.STOC_MIN,
        "categorii_meniu": Categorie.objects.filter(produs__isnull=False).distinct(),
    }
