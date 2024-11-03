from django.shortcuts import get_object_or_404, redirect, render
from society.models import Ad 
from django.contrib.auth.decorators import login_required
from society.models import Ad, Message
from society.Controller.Checker import check_session


@check_session
@login_required
def message_seller(request, ad_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    ad = get_object_or_404(Ad, pk=ad_id)
    success_message = None

    if ad.user == request.user:
        return redirect('classified') 
    
    if request.method == 'POST':
        message_content = request.POST.get('message')

        Message.objects.create(
            sender=request.user,
            receiver=ad.user,  
            ad=ad,
            content=message_content,
        )

        success_message = "Your message has been sent successfully!"
    
    context = {
        'ad': ad,
        'success_message': success_message
    }

    response = render(request, 'message_seller.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


@check_session
@login_required
def messages(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    ads_with_messages = Ad.objects.filter(message__receiver=request.user).distinct()

    selected_ad_id = request.GET.get('ad_id')
    selected_ad = None
    ad_messages = []

    if selected_ad_id:
        selected_ad = get_object_or_404(Ad, id=selected_ad_id)
        ad_messages = Message.objects.filter(ad=selected_ad, receiver=request.user).order_by('-timestamp')

    context = {
        'ads_with_messages': ads_with_messages,
        'selected_ad': selected_ad,
        'ad_messages': ad_messages,
    }

    response = render(request, 'messages.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response



