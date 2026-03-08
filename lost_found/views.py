from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Claim, Item


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _visible_items():
    return Item.objects.filter(moderation_status='approved').select_related('user', 'reviewed_by').order_by('-date_reported')


def _redirect_next(request, fallback):
    next_target = request.POST.get('next') or fallback
    if next_target.startswith('/'):
        return redirect(next_target)
    return redirect(next_target)


def _report_queue_context(report_status, status_filter):
    items = Item.objects.filter(status=report_status).select_related('user', 'reviewed_by').order_by('-date_reported')
    if status_filter in {'pending', 'approved', 'rejected'}:
        items = items.filter(moderation_status=status_filter)
    else:
        status_filter = 'all'

    kind_slug = report_status.lower()
    page_title = 'Lost Item Reports Overview' if report_status == 'Lost' else 'Found Item Reports Overview'
    page_copy = (
        'Review lost-item reports, publish verified reports, or hide entries that should not appear publicly.'
        if report_status == 'Lost'
        else 'Review found-item reports, decide whether they should be published, and confirm whether each item is already with OSA.'
    )

    context = _admin_nav_context()
    context.update({
        'items': items,
        'current_filter': status_filter,
        'report_nav_key': 'lost_reports' if report_status == 'Lost' else 'found_reports',
        'report_kind': kind_slug,
        'report_status': report_status,
        'page_title': page_title,
        'page_kicker': 'Admin Reports',
        'page_copy': page_copy,
        'report_list_url_name': f'{kind_slug}_reports_overview',
        'all_count': Item.objects.filter(status=report_status).count(),
        'pending_count': Item.objects.filter(status=report_status, moderation_status='pending').count(),
        'approved_count': Item.objects.filter(status=report_status, moderation_status='approved').count(),
    })
    return context


def _claim_queue_context(status_filter):
    claims = Claim.objects.select_related('item', 'reviewed_by').order_by('-created_at')
    if status_filter in {'pending', 'approved', 'rejected'}:
        claims = claims.filter(status=status_filter)
    else:
        status_filter = 'all'

    context = _admin_nav_context()
    context.update({
        'claims': claims,
        'current_filter': status_filter,
        'page_title': 'Claims Overview',
        'page_kicker': 'Admin Claims',
        'page_copy': 'Keep ownership requests in one review queue so approval, rejection, and cleanup happen in the same place.',
        'all_count': Claim.objects.count(),
        'pending_count': Claim.objects.filter(status='pending').count(),
        'approved_count': Claim.objects.filter(status='approved').count(),
        'rejected_count': Claim.objects.filter(status='rejected').count(),
    })
    return context


def _admin_nav_context():
    return {
        'current_nav': 'dashboard',
        'pending_reports_count': Item.objects.filter(moderation_status='pending').count(),
        'approved_reports_count': Item.objects.filter(moderation_status='approved').count(),
        'pending_claims_count': Claim.objects.filter(status='pending').count(),
        'completed_claims_count': Claim.objects.filter(status='approved').count(),
    }


def home(request):
    visible_items = _visible_items()
    return render(request, 'lost_found/home.html', {
        'lost_items': visible_items.filter(status='Lost'),
        'found_items': visible_items.filter(status='Found'),
    })


def search_results(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    date_lost = request.GET.get('date_lost', '')

    items = _visible_items().filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query),
        location__icontains=location,
    )

    if category:
        items = items.filter(category=category)

    if date_lost:
        items = items.filter(date_lost=date_lost)

    return render(request, 'lost_found/home.html', {
        'lost_items': items.filter(status='Lost'),
        'found_items': items.filter(status='Found'),
    })


def admin_login(request):
    if request.method != 'POST':
        return redirect('home')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and is_admin(user):
        login(request, user)
        return redirect('admin_dashboard')

    messages.error(request, 'Invalid admin credentials.')
    return redirect('home')


@user_passes_test(is_admin)
def admin_dashboard(request):
    context = _admin_nav_context()
    context['recent_items'] = Item.objects.order_by('-date_reported')[:5]
    return render(request, 'lost_found/admin_dashboard.html', context)


@user_passes_test(is_admin)
def reports_overview(request):
    context = _admin_nav_context()
    context.update({
        'lost_total_count': Item.objects.filter(status='Lost').count(),
        'lost_pending_count': Item.objects.filter(status='Lost', moderation_status='pending').count(),
        'found_total_count': Item.objects.filter(status='Found').count(),
        'found_pending_count': Item.objects.filter(status='Found', moderation_status='pending').count(),
    })
    return render(request, 'lost_found/reports_overview.html', context)


@user_passes_test(is_admin)
def lost_reports_overview(request):
    return render(request, 'lost_found/report_queue.html', _report_queue_context('Lost', request.GET.get('status', 'all')))


@user_passes_test(is_admin)
def found_reports_overview(request):
    return render(request, 'lost_found/report_queue.html', _report_queue_context('Found', request.GET.get('status', 'all')))


@user_passes_test(is_admin)
def claims_overview(request):
    return render(request, 'lost_found/claims_overview.html', _claim_queue_context(request.GET.get('status', 'all')))


def report_lost(request):
    if request.method != 'POST':
        return render(request, 'lost_found/lost_item.html')

    reporter_name = request.POST.get('name', '').strip()
    reporter_contact = request.POST.get('contact', '').strip()
    moderation_status = 'approved' if is_admin(request.user) else 'pending'

    Item.objects.create(
        title=request.POST.get('title'),
        category=request.POST.get('category'),
        location=request.POST.get('location'),
        description=request.POST.get('description'),
        date_lost=request.POST.get('date_lost') or None,
        time_lost=request.POST.get('time_lost') or None,
        image=request.FILES.get('image'),
        status='Lost',
        moderation_status=moderation_status,
        reporter_name=reporter_name,
        reporter_contact=reporter_contact,
        user=request.user if request.user.is_authenticated else None,
        reviewed_by=request.user if is_admin(request.user) else None,
        reviewed_at=timezone.now() if is_admin(request.user) else None,
    )

    if moderation_status == 'approved':
        messages.success(request, 'Lost Item Reported!')
        return redirect('admin_dashboard')

    messages.success(request, 'Lost item report submitted. OSA will review it before publishing.')
    return redirect('home')


def report_found(request):
    if request.method != 'POST':
        return redirect('home')

    is_staff_submission = is_admin(request.user)
    moderation_status = 'approved' if is_staff_submission else 'pending'

    Item.objects.create(
        title=request.POST.get('title'),
        category=request.POST.get('category'),
        location=request.POST.get('location'),
        description=request.POST.get('description'),
        date_lost=request.POST.get('date_found') or None,
        time_lost=request.POST.get('time_found') or None,
        image=request.FILES.get('image'),
        status='Found',
        moderation_status=moderation_status,
        reporter_name=request.POST.get('name', '').strip(),
        reporter_contact=request.POST.get('contact', '').strip(),
        is_surrendered_to_osa=True if is_staff_submission else bool(request.POST.get('is_surrendered_to_osa')),
        user=request.user if request.user.is_authenticated else None,
        reviewed_by=request.user if is_staff_submission else None,
        reviewed_at=timezone.now() if is_staff_submission else None,
    )

    if moderation_status == 'approved':
        messages.success(request, 'Found item report published and marked as already with OSA.')
        return redirect('admin_dashboard')

    messages.success(request, 'Found item report submitted. OSA will review it before publishing.')
    return redirect('home')


def claim_item(request):
    if request.method != 'POST':
        return redirect('home')

    item_id = request.POST.get('item_id')
    if not item_id:
        messages.error(request, 'Please choose a found item first before sending a claim request.')
        return redirect('home')

    item = get_object_or_404(Item, id=item_id, moderation_status='approved', status='Found')
    claim_status = 'approved' if is_admin(request.user) else 'pending'

    Claim.objects.create(
        item=item,
        claimant_name=request.POST.get('name', '').strip(),
        claimant_contact=request.POST.get('contact', '').strip(),
        reason=request.POST.get('reason', '').strip(),
        image=request.FILES.get('image'),
        user=request.user if request.user.is_authenticated else None,
        status=claim_status,
        reviewed_by=request.user if is_admin(request.user) else None,
        reviewed_at=timezone.now() if is_admin(request.user) else None,
    )

    if claim_status == 'approved':
        messages.success(request, 'Request for Claim is sent')
    else:
        messages.success(request, 'Request for Claim is sent')
    return redirect('item_detail', item_id=item.id)


@user_passes_test(is_admin)
def approve_report(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.moderation_status = 'approved'
    item.reviewed_by = request.user
    item.reviewed_at = timezone.now()
    item.save(update_fields=['moderation_status', 'reviewed_by', 'reviewed_at'])
    messages.success(request, 'Report approved and published.')
    return _redirect_next(request, 'reports_overview')


@user_passes_test(is_admin)
def reject_report(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.moderation_status = 'rejected'
    item.reviewed_by = request.user
    item.reviewed_at = timezone.now()
    item.save(update_fields=['moderation_status', 'reviewed_by', 'reviewed_at'])
    messages.info(request, 'Report hidden from public listings.')
    return _redirect_next(request, 'reports_overview')


@user_passes_test(is_admin)
def approve_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    claim.status = 'approved'
    claim.reviewed_by = request.user
    claim.reviewed_at = timezone.now()
    claim.save(update_fields=['status', 'reviewed_by', 'reviewed_at'])
    messages.success(request, 'Claim approved.')
    return _redirect_next(request, 'claims_overview')


@user_passes_test(is_admin)
def reject_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    claim.status = 'rejected'
    claim.reviewed_by = request.user
    claim.reviewed_at = timezone.now()
    claim.save(update_fields=['status', 'reviewed_by', 'reviewed_at'])
    messages.info(request, 'Claim rejected.')
    return _redirect_next(request, 'claims_overview')


@user_passes_test(is_admin)
def delete_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    claim.delete()
    messages.success(request, 'Claim deleted.')
    return _redirect_next(request, 'claims_overview')


def logout_view(request):
    if request.method == 'POST':
        django_logout(request)
    return redirect('home')


@user_passes_test(is_admin)
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully.')
    return _redirect_next(request, 'home')


def item_detail(request, item_id):
    item_queryset = Item.objects.select_related('user', 'reviewed_by') if is_admin(request.user) else _visible_items()
    item = get_object_or_404(item_queryset, id=item_id)
    related_queryset = item_queryset if is_admin(request.user) else _visible_items()
    related_items = related_queryset.filter(status=item.status).exclude(id=item.id)[:3]
    return render(request, 'lost_found/item_detail.html', {
        'item': item,
        'related_items': related_items,
        'is_admin_view': is_admin(request.user),
        'back_to_url': 'found_reports_overview' if is_admin(request.user) and item.status == 'Found' else 'lost_reports_overview' if is_admin(request.user) else 'home',
    })


def about(request):
    return render(request, 'lost_found/about.html')


def instructions(request):
    return render(request, 'lost_found/instructions.html')
