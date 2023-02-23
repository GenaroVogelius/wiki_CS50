from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


# Formularios universales
class SearchForm(forms.Form):
    busqueda = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "search",
                "placeholder": "Search Encyclopedia",
            }
        ),
    )


class CreateForms(forms.Form):
    description = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "description",
                "placeholder": "Insert content here",
            }
        ),
    )

    title = forms.CharField(
        max_length=100,
        widget=forms.Textarea(
            attrs={
                "class": "create_title",
                "placeholder": "Insert title here",
            }
        ),
    )

class FormEdit(forms.Form):
        contentForm = forms.CharField(
            max_length=1000,
            widget=forms.Textarea(
                attrs={
                    "class": "description",
                }
            ),
            # initial="",
        )

# variables universales
form = SearchForm()
paginas = util.list_entries()


# esta es una función que no es llamada por un path, sino es que es llamada por la función page.
def convertidor_html(title):
    content = util.get_entry(title)
    mark = markdown2.Markdown()
    if content == None:
        return None
    else:
        return mark.convert(content)


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": form},
    )


def page(request, entry):
    HTML = convertidor_html(entry)
    if HTML == None:
        return render(
            request,
            "encyclopedia/error.html",
            {"error": "Could not find entry", "title": entry, "form": form},
        )
    else:
        return render(
            request,
            "encyclopedia/result.html",
            {"title": entry, "entries": HTML, "form": form},
        )


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            entry_search = form.cleaned_data["busqueda"]
            HTML = convertidor_html(entry_search)
            if HTML is not None:
                return HttpResponseRedirect(
                    reverse("encyclopedia:page", args=[entry_search])
                )
            else:
                recomendaciones = []
                for page in paginas:
                    if entry_search.upper() in page.upper():
                        recomendaciones.append(page)
                if recomendaciones == []:
                    return render(
                        request,
                        "encyclopedia/error.html",
                        {
                            "error": "Could not find entry",
                            "title": entry_search,
                            "form": form,
                        },
                    )
                else:
                    return render(
                        request,
                        "encyclopedia/search.html",
                        {"recomend": recomendaciones, "form": form},
                    )
        else:
            return render(request, "encyclopedia/error.html", {"error": form})


def create(request):
    createForm = CreateForms() 
    # instanciaste la clase formulario en la variable createForm
    formBody = createForm["description"]
    formTitle = createForm["title"]
    # accedes a los formularios que tiene dentro con el nombre de la variable[ " " ] dentro de los parentesis pones el nombre del formulario que esta dentro de la clase a la cual queres acceder.

    return render(
        request,
        "encyclopedia/new.html",
        {
            "entries": util.list_entries(),
            "form": form,
            "formBody": formBody,
            "formTitle": formTitle,
        },
    )


def check(request):
    if request.method == "POST":
        formulario = CreateForms(request.POST)
        if formulario.is_valid():
            title = formulario.cleaned_data["title"]
            for pagina in paginas:
                if pagina.upper() == title.upper():
                    return render(
                        request,
                        "encyclopedia/error.html",
                        {"error": f"{title} already exist", "form": form},
                    )
            content = request.POST["description"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:page", args=[title]))
        else:
            return render(request, "encyclopedia/error.html", {"error": formulario})


def edit(request, entry):
    contenidoEscrito = util.get_entry(entry)
    formEdicion = FormEdit(initial={"contentForm": contenidoEscrito})
    # Para pasarle un valor a initial, tenes que poner key, value, donde la key seria el nombre del formulario y el value lo que queres que diga.
    return render(
        request,
        "encyclopedia/edit.html",
        {"formEdicion": formEdicion, "entry": entry, "form": form},
    )


def changes(request, entry):
    if request.method == "POST":
        contentModif = FormEdit(request.POST)
        if contentModif.is_valid():
            contentModif = contentModif.cleaned_data["contentForm"]
            contentModif = request.POST["contentForm"].strip()
            util.save_entry(entry, contentModif)
            return HttpResponseRedirect(reverse("encyclopedia:page", args=[entry]))
        


def randomPage(request):
    rand_choice = random.choice(paginas)
    return HttpResponseRedirect(reverse("encyclopedia:page", args=[rand_choice]))
