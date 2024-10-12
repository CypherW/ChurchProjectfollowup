from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import service_counts
from groups.models import session_attendance
from visitors.models import visit_details
from SalvationFollowUps.models import salvations
from django.contrib.auth.models import User
from .forms import service_count_form
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta



# Create your views here.
@login_required
def service_countspage(request):
    date = timezone.now().date()
    try:
        previous_submission = service_counts.objects.get(service_date=date)
    except:
        previous_submission = False
    if request.method=='POST':
        if previous_submission == False:
            form = service_count_form(request.POST)
        else:
            form = service_count_form(request.POST, instance=previous_submission)
        if form.is_valid():
            instance = form.save(commit=False)
            counter = request.user.id
            instance.counter = User.objects.get(id=counter)
            instance.save()
            print(instance.first_service_count)
            messages.success(request, f'Count has been updated. 1st servce:{instance.first_service_count} 2nd Service:{instance.second_service_count}')
            return redirect('service_counts')
    else:
        if previous_submission == False:
            form = service_count_form()
        else:
            form = service_count_form(instance=previous_submission)
    

    context = {
        'form': form,
    }
    return render(request, 'services/service_counts.html', context)

@login_required
def stats(request):
    def get_previous_sunday(weeks_ago=0):
        today = timezone.localtime()
        if today.strftime('%A') == 'Sunday':
            previous_sunday = today.date()
            print('today')
            print(previous_sunday)
        else:
            offset = (today.weekday() + 1) % 7
            previous_sunday = today - timezone.timedelta(days=offset)
            print('error')
        return previous_sunday - timezone.timedelta(weeks=weeks_ago)

    def get_next_saturday(sunday_date):
        next_saturday = sunday_date + timezone.timedelta(days=6)
        return next_saturday
    
    today = timezone.localtime()
    print("Current date and time:", today)
    print("Day of the week:", today.strftime('%A'))


    # Get the most recent Sunday and the following Saturday
    most_recent_sunday = get_previous_sunday()
    print(most_recent_sunday)
    most_recent_saturday = get_next_saturday(most_recent_sunday)

    # Get the Sunday and Saturday from one week ago
    one_week_ago_sunday = get_previous_sunday(weeks_ago=1)
    one_week_ago_saturday = get_next_saturday(one_week_ago_sunday)

    # Get the Sunday and Saturday from two weeks ago
    two_weeks_ago_sunday = get_previous_sunday(weeks_ago=2)
    two_weeks_ago_saturday = get_next_saturday(two_weeks_ago_sunday)

    # Get the Sunday and Saturday from three weeks ago
    three_weeks_ago_sunday = get_previous_sunday(weeks_ago=3)
    three_weeks_ago_saturday = get_next_saturday(three_weeks_ago_sunday)

    
    
    try:
        sunday_counts = service_counts.objects.get(service_date=most_recent_sunday)
        first_service = sunday_counts.first_service_count
        second_service = sunday_counts.second_service_count
        
        
    except:
        first_service = 0
        second_service = 0

    sunday_total = first_service + second_service
    try:
        previous_Sunday_counts = service_counts.objects.get(service_date=one_week_ago_sunday)
        previous_first_service = previous_Sunday_counts.first_service_count
        previous_second_service = previous_Sunday_counts.second_service_count

    except:
        previous_first_service = 0
        previous_second_service = 0
        
    previous_sunday_total = previous_first_service + previous_second_service

    try:
        two_Sunday_ago_counts = service_counts.objects.get(service_date=two_weeks_ago_sunday)
        two_Sunday_ago_first_service = two_Sunday_ago_counts.first_service_count
        two_Sunday_ago_second_service = two_Sunday_ago_counts.second_service_count

    except:
        two_Sunday_ago_first_service = 0
        two_Sunday_ago_second_service = 0
        
    two_sunday_ago_total = two_Sunday_ago_first_service + two_Sunday_ago_second_service

    group_attendance_total = session_attendance.objects.filter(dateofvisit__gte=most_recent_sunday, dateofvisit__lte=most_recent_saturday).count
    group_attendance_total_unique = session_attendance.objects.filter(dateofvisit__gte=most_recent_sunday, dateofvisit__lte=most_recent_saturday).distinct('attendee_id').count
    salvations_count = salvations.objects.filter(dateofcommitment__gte=most_recent_sunday, dateofcommitment__lte=most_recent_saturday).count
    visitors_count = visit_details.objects.filter(dateofvisit__gte=most_recent_sunday, dateofvisit__lte=most_recent_saturday).count

    previous_group_attendance_total = session_attendance.objects.filter(dateofvisit__gte=one_week_ago_sunday, dateofvisit__lte=one_week_ago_saturday).count
    previous_group_attendance_total_unique = session_attendance.objects.filter(dateofvisit__gte=one_week_ago_sunday, dateofvisit__lte=one_week_ago_saturday).distinct('attendee_id').count
    previous_salvations_count = salvations.objects.filter(dateofcommitment__gte=one_week_ago_sunday, dateofcommitment__lte=one_week_ago_saturday).count
    previous_visitors_count = visit_details.objects.filter(dateofvisit__gte=one_week_ago_sunday, dateofvisit__lte=one_week_ago_saturday).count

    two_sunday_ago_group_attendance_total = session_attendance.objects.filter(dateofvisit__gte=two_weeks_ago_sunday, dateofvisit__lte=two_weeks_ago_saturday).count
    two_sunday_ago_group_attendance_total_unique = session_attendance.objects.filter(dateofvisit__gte=two_weeks_ago_sunday, dateofvisit__lte=two_weeks_ago_saturday).distinct('attendee_id').count
    two_sunday_ago_salvations_count = salvations.objects.filter(dateofcommitment__gte=two_weeks_ago_sunday, dateofcommitment__lte=two_weeks_ago_saturday).count
    two_sunday_ago_visitors_count = visit_details.objects.filter(dateofvisit__gte=two_weeks_ago_sunday, dateofvisit__lte=two_weeks_ago_saturday).count

    sunday_date_format = most_recent_sunday.strftime('%d %B %Y')
    saturday_date_format = most_recent_saturday.strftime('%d %B %Y')
    previous_sunday_date_format = one_week_ago_sunday.strftime('%d %B %Y')
    previous_saturday_date_format = one_week_ago_saturday.strftime('%d %B %Y')
    two_sunday_ago_date_format = two_weeks_ago_sunday.strftime('%d %B %Y')
    two_saturday_ago_date_format = two_weeks_ago_saturday.strftime('%d %B %Y')

    

    context = {
        'first_service': first_service,
        'second_service': second_service,
        'sunday_total': sunday_total,
        'sunday_date_format': sunday_date_format,
        'saturday_date_format': saturday_date_format,
        'group_attendance_total': group_attendance_total,
        'group_attendance_total_unique': group_attendance_total_unique,
        'previous_first_service': previous_first_service,
        'previous_second_service': previous_second_service,
        'previous_sunday_date_format': previous_sunday_date_format,
        'previous_saturday_date_format': previous_saturday_date_format,
        'previous_sunday_total': previous_sunday_total,
        'previous_group_attendance_total': previous_group_attendance_total,
        'previous_group_attendance_total_unique': previous_group_attendance_total_unique,
        'salvations_count': salvations_count,
        'previous_salvations_count': previous_salvations_count,
        'visitors_count': visitors_count,
        'previous_visitors_count': previous_visitors_count,
        'two_Sunday_ago_first_service': two_Sunday_ago_first_service,
        'two_Sunday_ago_second_service': two_Sunday_ago_second_service,
        'two_sunday_ago_total': two_sunday_ago_total,
        'two_sunday_ago_group_attendance_total': two_sunday_ago_group_attendance_total,
        'two_sunday_ago_group_attendance_total_unique': two_sunday_ago_group_attendance_total_unique,
        'two_sunday_ago_salvations_count': two_sunday_ago_salvations_count,
        'two_sunday_ago_visitors_count': two_sunday_ago_visitors_count,
        'two_sunday_ago_date_format': two_sunday_ago_date_format,
        'two_saturday_ago_date_format': two_saturday_ago_date_format, 



    }
    return render(request, 'services/stats.html', context)