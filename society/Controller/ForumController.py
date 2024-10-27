from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib import messages
from society.forms import  ForumCommentForm, ForumReplyForm
from society.models import Forum 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from society.Controller.Checker import check_session
from django.utils import timezone
from django.contrib import messages


@check_session
def forum(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    selected_category = request.GET.get('category')
    if selected_category:
        forums = Forum.objects.filter(category=selected_category)  
    else:
        forums = Forum.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        forums = forums.filter(
            Q(title__icontains=search_query) 
        )    

    paginator = Paginator(forums, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  
        'paginator': paginator,
        'page_number': page_number,
        'selected_category': selected_category,
        'search_query': search_query 
    }

    # Set cache control headers
    response = render(request, 'forum.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@check_session
@login_required
def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Forum, id=post_id)

    if post.user != request.user and not request.user.is_superuser:
        return redirect('forum')  
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.category = request.POST.get('category')
        # post.name = request.POST.get('name')
        post.date = request.POST.get('date')
        post.description = request.POST.get('description')
        post.save()
        return redirect('forum')  

    # return render(request, 'edit_post.html', {'post': post})
    context = {'post': post}
    response = render(request, 'edit_post.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@check_session
@login_required
def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Forum, id=post_id)

    if post.user != request.user and not request.user.is_superuser:
        return redirect('forum')  

    if request.method == 'POST':
        post.delete()
        return redirect('forum')  

    # return render(request, 'delete_post.html', {'post': post})
    context = {'post': post}
    response = render(request, 'delete_post.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')        
        date = request.POST.get('date')
        description = request.POST.get('description')

        # Ensure the date is not in the past
        if date and date < timezone.now().date().isoformat():
            messages.error(request, 'You cannot select a past date.')
            return redirect('forum')

        new_post = Forum.objects.create(
            title=title,
            category=category,         
            date=date,
            description=description,
            user=request.user  
        )
        messages.success(request, 'Post created successfully!')
        return redirect('forum')
    else:
        return render(request, 'forum.html', {'today': timezone.now().date()})
    
@check_session
def forum_detail(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    forum = get_object_or_404(Forum, id=post_id)
    comments = forum.comments.all()
    comment_form = ForumCommentForm()
    reply_form = ForumReplyForm()

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = ForumCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.forum = forum
                comment.user = request.user
                comment.save()
                return redirect('forum_detail', post_id=post_id)
        elif 'reply_form' in request.POST:
            reply_form = ForumReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.comment_id = request.POST.get('comment_id')  # Get the comment being replied to
                reply.user = request.user
                reply.save()
                return redirect('forum_detail', post_id=post_id)

    context = {
        'forum': forum,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    # return render(request, 'forum_detail.html', context)
    # context = {'post': post}
    response = render(request, 'forum_detail.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response




    