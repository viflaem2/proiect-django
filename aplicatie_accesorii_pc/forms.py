from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Utilizator, Profil  

class ContactForm(forms.Form):
    nume = forms.CharField(max_length=100, label='Nume', required=True)
    email = forms.EmailField(label='Email', required=True)
    mesaj = forms.CharField(widget=forms.Textarea, label='Mesaj', required=True)

class LoginForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat'
    )

    def clean(self):        
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data


class RegisterForm(UserCreationForm):
    telefon = forms.CharField(required=True)
    tara = forms.CharField(initial="Romania", required=True)
    localitate = forms.CharField(required=True)
    abonat_newsletter = forms.BooleanField(label="Abonare la newsletter",required=False)
    judet = forms.CharField(required=False)
    strada = forms.CharField(required=False)
    numar = forms.CharField(required=False)
    bloc = forms.CharField(required=False)
    apartament = forms.CharField(required=False)
    cod_postal = forms.CharField(label="Cod postal", required=False)
    class Meta:
        model = Utilizator
        fields = ("username", "first_name", "last_name", "email", "tara", "telefon", "localitate", "abonat_newsletter", "password1", "password2")
    def clean_telefon(self):
        telefon = self.cleaned_data.get("telefon")
        tara = self.cleaned_data.get("tara","").lower()
        if telefon and tara=="romania":
            if telefon.startswith("+4"):
                telefon = telefon[2:]
            if len(telefon) != 10:
                raise forms.ValidationError("Telefon invalid")
            else:
                telefon = "+4" + telefon
        return telefon
    def clean_tara(self):
        tara = self.cleaned_data.get("tara")
        if len(tara) < 2:
            raise forms.ValidationError("Nu folositi abrevieri pentru tara.")
        return tara
    def clean_localitate(self):
        localitate = self.cleaned_data.get("localitate")
        if len(localitate) < 2:
            raise forms.ValidationError("Nu folositi abrevieri pentru localitate.")
        return localitate
    def save(self, commit=True):
        user = super().save(commit=False)
        user.telefon = self.cleaned_data["telefon"]
        user.tara = self.cleaned_data["tara"]
        user.localitate = self.cleaned_data["localitate"]
        user.abonat_newsletter = self.cleaned_data["abonat_newsletter"]
        if commit:
            user.save()
            campuri_profil = ("judet", "strada", "numar", "bloc", "apartament", "cod_postal")
            if any(self.cleaned_data[camp] for camp in campuri_profil):
                Profil.objects.create(
                utilizator=user,
                judet=self.cleaned_data["judet"],
                strada=self.cleaned_data["strada"],
                numar=self.cleaned_data["numar"],
                bloc=self.cleaned_data["bloc"],
                apartament=self.cleaned_data["apartament"],
                cod_postal=self.cleaned_data["cod_postal"]
                )
        return user


class EditareDateForm(forms.ModelForm):
    telefon = forms.CharField(required=True)
    tara = forms.CharField(initial="Romania", required=True)
    localitate = forms.CharField(required=True)
    abonat_newsletter = forms.BooleanField(label="Abonare la newsletter",required=False)
    judet = forms.CharField(required=False)
    strada = forms.CharField(required=False)
    numar = forms.CharField(required=False)
    bloc = forms.CharField(required=False)
    apartament = forms.CharField(required=False)
    cod_postal = forms.CharField(label="Cod postal", required=False)
    class Meta:
        model = Utilizator
        fields = ("username", "first_name", "last_name", "email", "tara", "telefon", "localitate", "abonat_newsletter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            profil = self.instance.profil
        except Profil.DoesNotExist:
            profil = None
        if profil:
            for camp in ("judet", "strada", "numar", "bloc", "apartament", "cod_postal"):
                self.fields[camp].initial = getattr(profil, camp)

    def clean_telefon(self):
        telefon = self.cleaned_data.get("telefon")
        tara = self.cleaned_data.get("tara","").lower()
        if telefon and tara=="romania":
            if telefon.startswith("+4"):
                telefon = telefon[2:]
            if len(telefon) != 10:
                raise forms.ValidationError("Telefon invalid")
            else:
                telefon = "+4" + telefon
        return telefon
    def clean_tara(self):
        tara = self.cleaned_data.get("tara")
        if len(tara) < 2:
            raise forms.ValidationError("Nu folositi abrevieri pentru tara.")
        return tara
    def clean_localitate(self):
        localitate = self.cleaned_data.get("localitate")
        if len(localitate) < 2:
            raise forms.ValidationError("Nu folositi abrevieri pentru localitate.")
        return localitate
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            campuri_profil = ("judet", "strada", "numar", "bloc", "apartament", "cod_postal")
            date_profil = {camp: self.cleaned_data[camp] for camp in campuri_profil}
            if any(date_profil.values()) or Profil.objects.filter(utilizator=user).exists():
                Profil.objects.update_or_create(utilizator=user, defaults=date_profil)
        return user
