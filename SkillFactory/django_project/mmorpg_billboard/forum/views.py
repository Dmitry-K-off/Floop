"""
Project views
"""
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail

from mmorpg_billboard.settings import DEFAULT_FROM_EMAIL as host_email

from .models import Announcement, Response, Category
from .forms import AnnouncementForm, ResponseForm

# Main view for displaying the homepage
def index(request):
 categories = Category.objects.all()
 latest_announcements = Announcement.objects.order_by('-created_at')[:10]

 # Set up pagination for latest announcements
 paginator = Paginator(latest_announcements, 5)
 page_number = request.GET.get('page')
 latest_announcements = paginator.get_page(page_number)

 return render(request, 'index.html', {
 'categories': categories,
 'latest_announcements': latest_announcements
 })

# View for displaying announcements within a specific category
def category_announcements(request, category_id):
    # Retrieve category or return 404 error if not found
    category = get_object_or_404(Category, pk=category_id)

    # Fetch all announcements for the selected category
    announcements = Announcement.objects.filter(category=category).order_by('-created_at')

    # Implement pagination (5 announcements per page)
    paginator = Paginator(announcements, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'category_announcements.html', {
        'category': category,
        'page_obj': page_obj
    })

# View for creating a new announcement (requires login)
@login_required
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.save()
            return redirect('announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form})

# View for displaying a single announcement and handling responses
def announcement_detail(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.announcement = announcement
            response.save()
            # Send notification email to announcement author
            send_mail(
                f'Новый отклик на ваше объявление "{announcement.title}"',
                f'Пользователь {request.user.username} оставил отклик: {response.text}\n'
                f'\nС уважением,\n'
                f'Администрация Портала [MMORPG_BillBoard]',
                host_email,
                [announcement.user.email],
                fail_silently=False,
            )
            return redirect('announcement_detail', pk=pk)
    else:
        form = ResponseForm()
    return render(request, 'announcement_detail.html', {'announcement': announcement, 'form': form})

# View for editing an existing announcement (requires login)
@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    # Check if the announcement author and the user is the same (only author can edit the announcement)
    if announcement.user != request.user:
        return redirect('announcement_detail', pk=pk)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_detail', pk=pk)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'edit_announcement.html', {
        'form': form,
        'announcement': announcement
    })

# View for displaying user responses
@login_required
def user_responses(request):
    # Fetch all responses for user's announcements
    responses = Response.objects.filter(announcement__user=request.user)
    announcements = Announcement.objects.filter(user=request.user)

    # Filter responses by announcement if specified in query parameters
    if 'announcement_id' in request.GET:
        announcement_id = request.GET.get('announcement_id')
        if announcement_id == 'all':
            responses = responses
        else:
            responses = responses.filter(announcement_id=announcement_id)

    return render(request, 'user_responses.html', {
        'responses': responses,
        'announcements': announcements
    })

# View for accepting a response
@login_required
def accept_response(request, announcement_pk, response_pk):
    # Retrieve announcement and response objects
    announcement = get_object_or_404(Announcement, pk=announcement_pk)
    response = get_object_or_404(Response, pk=response_pk)

    # Check if user is the author of the announcement
    if request.user != announcement.user:
        messages.error(request, "У вас нет прав на выполнение этого действия")
        return redirect('announcement_detail', pk=announcement_pk)

    # Mark response as accepted
    response.is_accepted = True
    response.save()

    # Send notification email to response author
    send_mail(
        'Ваш отклик принят',
        f'Ваш отклик на объявление "{announcement.title}" был принят автором {response.user.username}.\n'
        f'\nС уважением\n'
        f'Администрация Портала [MMORPG_BillBoard]',
        host_email,
        [response.user.email],
        fail_silently=False,
    )

    messages.success(request, "Отклик принят")
    return redirect('announcement_detail', pk=announcement_pk)

# View for deleting a response
@login_required
def delete_response(request, response_id):
    # Retrieve response object
    response = get_object_or_404(Response, pk=response_id)

    # Check if user is the author of the announcement
    if request.user != response.announcement.user:
        messages.error(request, "У вас нет прав на удаление этого отклика")
        return redirect('announcement_detail', pk=response.announcement.pk)

    # Delete the response
    announcement_pk = response.announcement.pk
    response.delete()
    messages.success(request, "Отклик успешно удален")
    return redirect('announcement_detail', pk=announcement_pk)
