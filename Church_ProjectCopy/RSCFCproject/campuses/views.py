from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import campus_meetings, campuses_details
from django.contrib.auth.models import User
from .forms import campus_meeting_Form
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.core.mail import send_mail

# Create your views here.
@login_required
def view_campus_feedback(request):
    feedback = campus_meetings.objects.all()
    print(feedback)

    context = {
        'feedback': feedback
    }
    return render(request, 'campuses/view_campus_feedback.html', context)

@login_required
def campus_meetings_feedback(request):
    date = timezone.now().date()
    if request.method=='POST':
        form = campus_meeting_Form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            campus_leader = request.user.id
            instance.campus_leader = User.objects.get(id=campus_leader)
            instance.save()
            messages.success(request, f'Thank you. Your feedback has been saved.')
            campus_leader = campuses_details.objects.get(campus_leader=request.user.id)
            send_mail("CAMPUS MEETING FEEDBACK",
f"""Dear Pastor {campus_leader.overseer}, 
    
Pastor {campus_leader} had a meeting and has submitted feedback.
     
 """,
    "shodandevstesting@gmail.com",
    [campus_leader.overseer.email],
    fail_silently=False,
)
            return redirect('campus_meetings')
    else:
            form = campus_meeting_Form()
    

    context = {
        'form': form,
    }
    return render(request, 'campuses/campus_meeting_feedback.html', context)

