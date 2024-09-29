from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import service_counts
from groups.models import session_attendance
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
    def get_previous_sunday(): # Determine if today is a Sunday. If not get previous Sunday's day else use today's date.
        today = timezone.now()
        if today.strftime('%A') == 'Sunday':
            return today.date()
        else:
            offset = (today.weekday() + 1) % 7
            previous_sunday = today - timezone.timedelta(days=offset)
            return previous_sunday.date()
    
    def get_next_saturday(sunday_date):  # Determine when the next Saturday will be from above determined Sunday.
        next_saturday = sunday_date + timezone.timedelta(days=6)
        return next_saturday

    
    Sunday = get_previous_sunday()
    Saturday = get_next_saturday(Sunday)
    
    try:
        sunday_counts = service_counts.objects.get(service_date=Sunday)
        first_service = sunday_counts.first_service_count
        second_service = sunday_counts.second_service_count
        
    except:
        first_service = 0
        second_service = 0
        
    sunday_total = first_service + second_service
    group_attendance_total = session_attendance.objects.filter(dateofvisit__gte=Sunday, dateofvisit__lte=Saturday).count
    group_attendance_total_unique = session_attendance.objects.filter(dateofvisit__gte=Sunday, dateofvisit__lte=Saturday).distinct('attendee_id').count


    sunday_date_format = Sunday.strftime('%d %B %Y')
    saturday_date_format = Saturday.strftime('%d %B %Y')


    

    context = {
        'first_service': first_service,
        'second_service': second_service,
        'sunday_total': sunday_total,
        'sunday_date_format': sunday_date_format,
        'saturday_date_format': saturday_date_format,
        'group_attendance_total': group_attendance_total,
        'group_attendance_total_unique': group_attendance_total_unique,
    }
    return render(request, 'services/stats.html', context)