from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from society.models import Ad
from society.views import messages
from django.db.models import Q
from society.Controller.Checker import check_session


@check_session
def classified(request):
    if not request.user.is_authenticated:
        return redirect('login')
    ad=Ad.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        ad= ad.filter(
            Q(title__icontains=search_query)                          
        )
    paginator = Paginator(ad, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,  
        'paginator': paginator,
        'page_number': page_number,
        'search_query': search_query 
}
    response = render(request, 'classified.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'    
    return response

@check_session
@login_required
def edit_ad(request, ad_id):
    if not request.user.is_authenticated:
        return redirect('login')
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user and not request.user.is_superuser:
        return redirect('classified')  
    if request.method == 'POST':
        ad.title = request.POST.get('title')
        ad.price = request.POST.get('price')
        ad.description = request.POST.get('description')
        ad.save()
        return redirect('classified')  
    # return render(request, 'edit_ad.html', {'ad': ad})
    context = {'ad': ad}
    response = render(request, 'edit_ad.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@check_session
@login_required
def delete_ad(request, ad_id):
    if not request.user.is_authenticated:
        return redirect('login')
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user and not request.user.is_superuser:
        return redirect('classified')  
    if request.method == 'POST':
        ad.delete()
        return redirect('classified')  
    # return render(request, 'delete_ad.html', {'ad': ad})
    context = {'ad': ad}
    response = render(request, 'delete_ad.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def create_ad(request):
    if request.method == 'POST':
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']        
        new_ad = Ad.objects.create(title=title, price=price, description=description,user=request.user  
)
        messages.success(request, 'Ad created successfully!')

        return redirect('classified')  
    else:
        return render(request, 'classified.html')
