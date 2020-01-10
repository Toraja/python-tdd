from django.views.generic import View
from django.shortcuts import redirect, render
from lists.models import Item, List


class HomePageView(View):
    """description"""
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

    def post(self, request, *args, **kwargs):
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/the-only-list-in-the-world/')


class ListPageView(View):
    """description"""
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        return render(request, 'list.html', {'items': items})
