from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Produs, Categorie
from django.http import HttpResponse
from datetime import datetime
import locale
from django.conf import settings

class Accesare:
    contor=1
    def __init__(self, ip_client, url="", parametri={}):
        self.id=Accesare.contor
        Accesare.contor+=1
        self.ip_client=ip_client
        self._url=url
        self._data=datetime.now()
        self.parametri=parametri
    def __str__(self):
        return f"url: {self.url()}\npagina: {self.pagina()}\ncalculeaza_data: {self.calculeaza_data()}\nlista_parametri: {self.lista_parametri()}\nAccesare ID: {self.id}\nIP: {self.ip_client}"
    def lista_parametri(self):
        if hasattr(self.parametri, "lists"):
            return [(key, value) for key, values in self.parametri.lists() for value in values]
        return [(key, self.parametri[key]) for key in self.parametri]
    def url(self):
        if not self.parametri:
            return self._url
        if hasattr(self.parametri, "urlencode"):
            return self._url + "?" + self.parametri.urlencode()
        return self._url+"?"+"&".join(f"{key}={value}" for key,value in self.lista_parametri())
    def pagina(self):
        pagina = self._url.replace("/aplicatie_accesorii_pc", "", 1)
        return pagina.rstrip("/") or "/"
    def calculeaza_data(self, format="%A, %#d %B %Y",tip=""):
        locale.setlocale(locale.LC_TIME, "ro")
        match tip:
            case "zi":
                format="%#d %B %Y"
            case "timp":
                format="%H:%M:%S"                
        return f"{self._data.strftime(format).title()}"

accesari=[]
def access(request):
    a=Accesare(ip_client=request.ip,url=request.path,parametri=request.GET)
    print(a)
    accesari.append(a)
    return a

def index(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/index.html")

def info(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/info.html",
        {"data":a.calculeaza_data(tip=a.parametri.get("data"))}
    )

def istoric(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/istoric.html")

def despre(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/despre.html")

def afis_produse(request,nume_categorie=None):
    a=access(request)
    nrPagina=request.GET.get("pagina",1)
    coloana=request.GET.get("coloana", "denumire")
    ordine=request.GET.get("ordine", "a")
    if coloana not in ["denumire", "pret", "stoc"]:
        coloana="denumire"
    if ordine=="d":
        produse=Produs.objects.order_by("-"+coloana)
    else:
        produse=Produs.objects.order_by(coloana)
    taguri=request.GET.getlist("tag")
    if taguri:
        produse=produse.filter(taguri__contains=taguri)
    if nume_categorie:
        produse=produse.filter(categorie__nume=nume_categorie)
    paginator=Paginator(produse, settings.PROD_PER_PAG)
    mesajEroare=None
    try:
        obPagina = paginator.page(nrPagina)
    except EmptyPage:
        obPagina=None
        mesajEroare = "Nu mai sunt produse"
    except PageNotAnInteger: 
        obPagina=None
        mesajEroare = "Numarul paginii trebuie sa fie un numar intreg"
    parametri=request.GET.copy()
    parametri.pop("pagina",None)
    butoane=[]
    for tag in taguri:
        params=parametri.copy()
        params.setlist("tag", [t for t in taguri if t!=tag])
        butoane.append((tag, params.urlencode()))
    categorie=None
    if nume_categorie:
        try:
            categorie=Categorie.objects.get(nume=nume_categorie)
        except Categorie.DoesNotExist:
            return HttpResponse("Categoria nu exista.", status=404)
    return render(request, 'aplicatie_accesorii_pc/produse.html',
                    {
                        'pagina': obPagina,
                        'eroare': mesajEroare,
                        'parametri': parametri.urlencode(),
                        'butoane' : butoane,
                        'categorie': categorie
                    }
    )
def afis_produs(request, id):
    a=access(request)
    try:
        produs = Produs.objects.get(pk=id)
    except Produs.DoesNotExist:
        return HttpResponse("Produsul nu exista.", status=404)
    similare = Produs.objects.raw("""
        SELECT *
        FROM aplicatie_accesorii_pc_produs
        WHERE id_categorie = %s AND id_produs != %s
        ORDER BY RANDOM()
        LIMIT 3
    """, [produs.categorie_id, produs.pk])
    return render(request, "aplicatie_accesorii_pc/produs.html", {"produs": produs, "similare": similare})

def contact(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/in_lucru.html")

def cos_virtual(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/in_lucru.html")

def faq(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/in_lucru.html")

def termeni(request):
    a=access(request)
    return render(request,"aplicatie_accesorii_pc/in_lucru.html")

def accesare(request,id):
    a=access(request)
    for obiect in accesari:
        if obiect.id==int(id):
            return render(request,"aplicatie_accesorii_pc/accesare.html",{"obiect":str(obiect).replace('\n','<br>')})
    return render(request,"aplicatie_accesorii_pc/accesare.html",{"obiect":"Accesarea nu exista"})

def log(request):
    a=access(request)
    ultimele=a.parametri.get("ultimele")
    acces=a.parametri.get("accesari")
    tabel=a.parametri.get("tabel","")
    pagina=""
    mesaj=""
    frecventa={}
    for ac in accesari:
        pag=ac.pagina()
        if pag not in frecventa:
            frecventa[pag]=1
        else:
            frecventa[pag]+=1
    minim=min(frecventa, key=frecventa.get)
    maxim=max(frecventa, key=frecventa.get)
    mesaj=f"<p>Pagina cea mai putin accesata: {minim}</p>\n"
    mesaj+=f"<p>Pagina cea mai des accesata: {maxim}</p>\n"
    if ultimele==None:
        lista=accesari
    elif ultimele.isnumeric() and int(ultimele)!=0:
        ult=int(ultimele)
        if(ult>len(accesari)):
            lista=accesari
            mesaj+=f"<p>Exista doar {len(accesari)} accesari fata de {ult} accesari cerute</p>"
        else:
            lista=accesari[-ult:]
    else:
        return render(request,"aplicatie_accesorii_pc/log.html",{"pagina":"<p>Eroare: ultimele trebuie sa fie un numar intreg nenul</p>"})
    if "iduri" in a.parametri:
        iduri=[]
        for grup in a.parametri.getlist("iduri"):
            for id in grup.split(","):
                if not id.isdecimal():
                    return render(request,"aplicatie_accesorii_pc/log.html",{"pagina":"<p>Eroare: iduri trebuie sa contina numere intregi separate prin virgula</p>"})
                iduri.append(int(id))
        dubluri=a.parametri.get("dubluri","false")
        selectate=[]
        vazute=[]
        for id in iduri:
            if id in vazute and dubluri!="true":
                continue
            for obiect in lista:
                if obiect.id==id:
                    selectate.append(obiect)
                    vazute.append(id)
                    break
        lista=selectate
    permise=["id","url","pagina","data","parametri","ip"]
    if tabel=="tot":
        lista_tabel=permise
    else:
        lista_tabel=[coloana for coloana in tabel.split(",") if coloana in permise]
    if lista_tabel:
        pagina+="<table border=1>\n<tr>\n"
        for cap in lista_tabel:
            pagina+=f"<th>{cap}</th>\n"
        pagina+="</tr>\n"
        for obiect in lista:
            valori = {
                "id": obiect.id,
                "url": obiect.url(),
                "pagina": obiect.pagina(),
                "data": obiect.calculeaza_data(),
                "parametri": obiect.lista_parametri(),
                "ip": obiect.ip_client
            }
            pagina+="<tr>\n"
            for value in lista_tabel:
                pagina+=f"<td>{valori[value]}</td>\n"
            pagina+="</tr>\n"
        pagina+="</table>"
    else:    
        for obiect in lista:
            pagina+=f"<div>{str(obiect).replace('\n','<br>')}</div><br>"
    pagina+=mesaj
    if acces=="nr":
        pagina+=f"<div> Numar accesari: {len(accesari)}</div>"
    elif acces=="detalii":
        pagina+="<h2>Detalii accesari</h2><ul>"
        for obiect in lista:
            pagina+=f"<li>{obiect.calculeaza_data(format='%A, %#d %B %Y %H:%M:%S')}</li>"
        pagina+="</ul>"
    pagina+=f"<h2>Parametri</h2><p>Numar parametri: {len(a.parametri)}</p><ul>"
    for nume in a.parametri:
        pagina+=f"<li>{nume}</li>"
    pagina+="</ul>"
    return render(request,"aplicatie_accesorii_pc/log.html",{"pagina":pagina})