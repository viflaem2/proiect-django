from django.conf import settings

def procesare(request):
    return {"detalii_firma": settings.DETALII_FIRMA}
