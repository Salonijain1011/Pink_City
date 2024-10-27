from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from society.models import Event
from society.views import messages
from django.db.models import Q
from society.models import RSVP
from society.forms import RSVPForm
from society.Controller.Checker import check_session
from django.utils import timezone
from django.contrib import messages


@check_session
def events(request):
    if not request.user.is_authenticated:
        return redirect('login')
    events = Event.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        events= events.filter(
            Q(title__icontains=search_query) 
        ) 

    paginator = Paginator(events, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

   

    context = {
        'page_obj': page_obj,  
        'paginator': paginator,
        'page_number': page_number,
        'search_query': search_query 
} # Get all events from the database # Set cache control headers
    response = render(request, 'events.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@check_session
@login_required
def edit_event(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')
    event = get_object_or_404(Event, id=event_id)

    if event.user != request.user and not request.user.is_superuser:
        return redirect('events')  

    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.location = request.POST.get('location')
        event.date = request.POST.get('date')
        event.description = request.POST.get('description')
        event.save()
        return redirect('events')  
    context = {'event': event}
    # return render(request, 'edit_event.html', {'event': event})
    response = render(request, 'edit_event.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


@check_session
@login_required
def delete_event(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')
    event = get_object_or_404(Event, id=event_id)

    if event.user != request.user and not request.user.is_superuser:
        return redirect('events')  

    if request.method == 'POST':
        event.delete()
        return redirect('events')  

    context = {'event': event}
    response = render(request, 'delete_event.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        location = request.POST.get('location')
        description = request.POST.get('description')

        # Ensure the date is not in the past
        if date and date < timezone.now().date().isoformat():
            messages.error(request, 'You cannot select a past date.')
            return redirect('events')

        new_event = Event.objects.create(
            title=title,
            date=date,
            location=location,
            description=description,
            user=request.user  
        )
        messages.success(request, 'Event created successfully!')
        return redirect('events')  
    else:
        return render(request, 'event.html', {'today': timezone.now().date()})


@check_session
def rsvp(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')
    event = get_object_or_404(Event, id=event_id)
    rsvps = event.rsvps.filter(attending=True)  # Only those attending

    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp, created = RSVP.objects.update_or_create(
                user=request.user,
                event=event,
                defaults={'attending': form.cleaned_data['attending']}
            )
            return redirect('rsvp', event_id=event_id)
    else:
        form = RSVPForm()

    context = {'event': event, 'form': form, 'rsvps': rsvps}

    # Set cache control headers
    response = render(request, 'rsvp.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response