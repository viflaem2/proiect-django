from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

class Producator(models.Model):
    id_producator = models.AutoField(primary_key=True)
    denumire = models.CharField(max_length=255, unique=True, error_messages={"unique": "Exista deja un producator cu aceasta denumire."})
    tara_origine = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True, error_messages={"invalid": "URL-ul introdus este invalid"})
    class Meta:
        ordering = ["denumire"]
        verbose_name_plural = "Producatori"
    def __str__(self):
        return self.denumire

class Categorie(models.Model):
    class TipUtilizareChoices(models.TextChoices):
        GAMING = 'gaming', 'Gaming'
        OFFICE = 'office', 'Office'
        TRAVEL = 'travel', 'Travel'
    id_categorie = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=255, unique=True)
    descriere = models.TextField(blank=True, null=True)
    culoare = models.CharField(max_length=50, blank=True, null=True, help_text="Culoarea categoriei in format hexazecimal, de exemplu #009b84.")
    sigla = models.ImageField(upload_to="categorii/", max_length=255, blank=True, null=True, help_text="Imagine reprezentativa pentru categorie.")
    tip_utilizare = models.CharField(max_length=50, choices=TipUtilizareChoices.choices)
    class Meta:
        indexes = [
            models.Index(fields=["tip_utilizare"]),
        ]
        ordering = ["nume"]
        verbose_name_plural = "Categorii"
    def __str__(self):
        return self.nume

class Furnizor(models.Model):
    id_furnizor = models.AutoField(primary_key=True)
    producator = models.ForeignKey(Producator, on_delete=models.SET_NULL, null=True, db_column='id_producator')
    denumire = models.CharField(max_length=255, unique=True, error_messages={"unique": "Exista deja un furnizor cu aceasta denumire."})
    tara = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True, error_messages={"invalid": "URL-ul introdus este invalid"})
    class Meta:
        ordering = ["denumire"]
        verbose_name_plural = "Furnizori"
    def __str__(self):
        return self.denumire

class TipConexiune(models.Model):
    id_tip_conexiune = models.AutoField(primary_key=True)
    denumire = models.CharField(max_length=100)
    versiune = models.CharField(max_length=50, blank=True, null=True)
    tip_conector = models.CharField(max_length=100, blank=True, null=True, help_text="Forma conectorului fizic, de exemplu USB-A sau USB-C.")
    class Meta:
        ordering = ["denumire"]
        verbose_name_plural = "Tipuri de conexiune"
    def __str__(self):
        return self.denumire

class Produs(models.Model):
    id_produs = models.AutoField(primary_key=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, db_column='id_categorie')
    furnizor = models.ForeignKey(Furnizor, on_delete=models.SET_NULL, null=True, db_column='id_furnizor')
    denumire = models.CharField(max_length=255)
    descriere = models.TextField(blank=True, null=True)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    stoc = models.IntegerField(default=0)
    wireless = models.BooleanField(default=False)
    data_lansare = models.DateTimeField(default=timezone.now, blank=True, null=True)
    garantie_luni = models.SmallIntegerField(default=12)
    greutate_g = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    culori_disponibile = ArrayField(models.CharField(max_length=50), blank=True, null=True, help_text="Introduceti culorile separate prin virgula, de exemplu negru,alb,rosu.")
    taguri = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    conexiuni = models.ManyToManyField(TipConexiune)
    class Meta:
        indexes = [
            models.Index(fields=["pret"]),
            models.Index(fields=["categorie"]),
            models.Index(fields=["wireless"]),
        ]
        ordering = ["denumire"]
        verbose_name_plural = "Produse"
        constraints = [
            models.CheckConstraint(condition=models.Q(pret__gte=0), name="pret_nenegativ"),
            models.CheckConstraint(condition=models.Q(stoc__gte=0), name="stoc_nenegativ"),
            models.CheckConstraint(condition=models.Q(greutate_g__gte=0), name="greutate_nenegativa"),
            models.CheckConstraint(condition=models.Q(garantie_luni__gte=0), name="garantie_nenegativa"),
        ]
    def __str__(self):
        return self.denumire
    def get_absolute_url(self):
            return reverse("produs", kwargs={"id": self.pk}) #self.pk e primary key

class ImagineProdus(models.Model):
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, db_column='id_produs')
    nr_imagine = models.IntegerField(unique=True, error_messages={"unique": "Exista deja o imagine cu acest numar."}, help_text="Numarul imaginii in cadrul produsului.")
    cale_imagine = models.ImageField(upload_to="produse/", max_length=255)
    text_alternativ = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering = ["nr_imagine"]
        unique_together = ('produs', 'nr_imagine')
        verbose_name_plural = "Imagini produse"
        constraints = [
            models.CheckConstraint(condition=models.Q(nr_imagine__gte=1), name="nr_imagine_pozitiv"),
        ]
    def __str__(self):
        return f"{self.produs.denumire} - Img {self.nr_imagine}"