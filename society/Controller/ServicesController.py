from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from society.models import Services
from django.contrib import messages
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from society.models import Services, Comment, Reply
from society.forms import CommentForm, ReplyForm
from society.Controller.Checker import check_session


@check_session
def services(request):
    if not request.user.is_authenticated:
        return redirect('login')
    selected_category = request.GET.get('service_category') 
    if selected_category:
        services = Services.objects.filter(service_category=selected_category)  
    else:      
        services = Services.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        services = services.filter(     
            Q(description__icontains=search_query)          
        )
    paginator = Paginator(services, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'page_number': page_number,
        'selected_category': selected_category,
        'search_query': search_query 
    } # Get all events from the database # Set cache control headers
    response = render(request, 'services.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Services, id=service_id)

    if  service.user != request.user and not request.user.is_superuser:
        return redirect('services')  


    if request.method == 'POST':
        service.service_type = request.POST.get('service_type')
        service.service_category = request.POST.get('service_category')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.save()
        return redirect('services')  

    return render(request, 'edit_service.html', {'service': service})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Services, id=service_id)

    if service.user != request.user and not request.user.is_superuser:
        return redirect('services')  

    if request.method == 'POST':
        service.delete()
        return redirect('services')  

    return render(request, 'delete_service.html', {'service': service})


def post_service(request):   
    if request.method=="POST":
        service_type=request.POST.get('service_type')
        service_category=request.POST.get('service_category')
        description=request.POST.get('description')
        price=request.POST.get('price')
        data=Services.objects.create(service_type=service_type,service_category=service_category,description=description,price=price,user=request.user  
)
        messages.success(request, 'Service created successfully!')
        return redirect('services') 
    else:  
        return render(request,'services.html')
    
def service_detail(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    comments = service.comments.all()
    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.service = service
                comment.user = request.user
                comment.save()
                return redirect('service_detail', service_id=service_id)
        elif 'reply_form' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.comment_id = request.POST.get('comment_id')  # ID of the comment being replied to
                reply.user = request.user
                reply.save()
                return redirect('service_detail', service_id=service_id)

    context = {
        'service': service,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    return render(request, 'service_detail.html', context)

