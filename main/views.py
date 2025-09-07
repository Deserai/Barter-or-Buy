from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.timezone import now, timedelta
from main.forms import CropSearchForm, Compare, FeedbackForm
from .generate_pricelist import get_matching_crops, priceOf, compare
from .models import Feedback, FeatureUsage



def index(request):
    FeatureUsage.objects.create(
        feature_name='Site visit',
        details= 1)
    return render(request, 'main/index.html')


@require_GET
def autocomplete(request):
    crop = request.GET.get('term', '').upper()
    result = get_matching_crops(crop)
    return JsonResponse(result, safe=False)


def buy(request):
    result = None
    form = CropSearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        crop = form.cleaned_data['crop']
        FeatureUsage.objects.create(
            feature_name='Buy',
            details=crop
        )
        result = [crop, priceOf(crop.upper())]
    return render(request, 'main/buy.html', {'form': form, 'result': result})
    

def barter(request):
    result = None
    form = Compare(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        crop1 = form.cleaned_data['crop1']
        crop2 = form.cleaned_data['crop2']
        FeatureUsage.objects.create(
            feature_name='Barter',
            details= f'Crop1 - {crop1}, Crop2 - {crop2}'
        )
        result = compare(crop1.upper(), crop2.upper())
    return render(request, 'main/barter.html', {'form': form, 'result': result})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FeedbackForm()
    
    return render(request, 'main/feedback.html', {'form': form})


@login_required
def inbox_view(request):
    messages = Feedback.objects.order_by('-created_at')
    total_usage = FeatureUsage.objects.count()
    feature_counts = FeatureUsage.objects.values('feature_name').annotate(count=Count('id'))
    last_week = now() - timedelta(days=7)
    daily_counts = (
        FeatureUsage.objects.filter(used_at__gte=last_week)
        .extra(select={'day': 'date(used_at)'})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    return render(request, 'main/inbox.html', {        
        'messages': messages,
        'total_usage': total_usage,
        'feature_counts': feature_counts,
        'daily_counts': list(daily_counts),
        })
