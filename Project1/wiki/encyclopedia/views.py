from django.shortcuts import render
import random
import markdown2

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    
    if content is None:
        return None
    else:
        return markdown2.markdown(content)

def entry(request, title):
    html_content = convert_md_to_html(title)
    
    if html_content is None:
        return render(request, "encyclopedia/error.html",{
            'ms': "page dose not exsist..."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": html_content,
            "title": title
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
           return render(request, "encyclopedia/entry.html", {
              "content": html_content,
              "title": entry_search
           })
        else:
            recomdation = []
            allEntry = util.list_entries()
            for entry in allEntry:
                if entry_search.lower() in entry.lower():
                    recomdation.append(entry)
            return render(request, "encyclopedia/search.html", {
                 "entries": recomdation
                })

def new_page(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new.html")    
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error.html",{
                'ms': "page is already exiest.."
            })  
        else:
            util.save_entry(title,content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
              "content": html_content,
              "title": title
              })
                  
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
              "content": content,
              "title": title
              })
        
def save_edit(request):
    if request.method == "POST":
         title = request.POST['title']
         content = request.POST['content']
         util.save_entry(title,content)
         html_content = convert_md_to_html(title)
         return render(request, "encyclopedia/entry.html", {
              "content": html_content,
              "title": title
              })
         
def rand(request):
    allList = util.list_entries()
    title = random.choice(allList)
    html_content = convert_md_to_html(title)    
    return render(request, "encyclopedia/entry.html", {
              "content": html_content,
              "title": title
              })     