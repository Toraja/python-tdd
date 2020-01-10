from django.views.generic import View
from django.shortcuts import redirect, render
from lists.models import Item, List


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class ListView(View):

    def post(self, request, *args, **kwargs):
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')


class ItemView(View):

    def get(self, request, list_id):
        list_ = List.objects.get(id=list_id)
        items = Item.objects.filter(list=list_)
        return render(request, 'list.html', {'items': items})

    def post(self, request, list_id):
        list_to_add = List.objects.get(id=list_id)
        Item.objects.create(text=request.POST['item_text'], list=list_to_add)
        return redirect(f'/lists/{list_to_add.id}/')
