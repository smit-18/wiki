from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

from . import util
from markdown2 import Markdown
import random

markdowner = Markdown()

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    return render(request, "encyclopedia/title.html", {
        "title": title.upper(),
        "entry": markdowner.convert(util.get_entry(title))
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form":form
            })
    else:
        return render(request, "encyclopedia/add.html",{
        "form": NewTaskForm
        })

def random_select(request):
    return render(request, "encyclopedia/title.html", {
        "entry": markdowner.convert(util.get_entry(random.choice(util.list_entries())))
    })

def edit(request):
    if request.method == "POST":
        entry = request.POST['title']
        return render(request, "encyclopedia/edit.html",{
            "title":entry,
            "content": util.get_entry(entry),
    })

def edit_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "encyclopedia.edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        entries = util.list_entries()
        if query in entries:
            return render(request, "encyclopedia/title.html", {
                "entry": markdowner.convert(util.get_entry(query)),
                "title": query
            })
        else:
            return render(request, "encyclopedia/pagenotfound.html")
