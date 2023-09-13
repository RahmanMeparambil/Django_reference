from django.shortcuts import render ,get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm,EditItemForm
from .models import Item,Category
from django.db.models import Q

# Create your views here.
def detail(request,pk):
    item = get_object_or_404(Item, pk=pk)
    rel_items = Item.objects.filter(category = item.category,quantity__gt=0).exclude(pk=pk)
    return render(request,'item/detail.html',{
        'item': item,
        'rel_items':rel_items,
        })  


def items(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category',0)
    print(category_id)

    items = Item.objects.all()
    categories = Category.objects.all()

    if query:
        query = query.strip()
        items = items.filter(Q(name__icontains=query)|Q(description__icontains=query))
    
    if category_id :
        items = items.filter(category_id = category_id)

    return render(request,'item/items.html',{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id)
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST,request.FILES)

        if form.is_valid() :
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail',pk = item.id)
    else:
        form = NewItemForm()
    return render(request,'item/form.html',{
        'form': form
    })


@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST,request.FILES,instance=item)

        if form.is_valid() :
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail',pk = item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request,'item/form.html',{
        'form': form
    })


@login_required
def delete(request,pk):
    item = get_object_or_404(Item,pk = pk,created_by = request.user)
    item.delete()
    return redirect('dashboard:index')


    