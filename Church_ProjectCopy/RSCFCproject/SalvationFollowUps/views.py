import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import salvations, Converts, Followups, Requests_Feedback, Link_Church, ATTENDCHURCH, Followed_Up_by, new_convert_first_followup, new_convert_followup_call, new_convert_referral_finalize
from .forms import ConvertsForm, PrayerRequestForm, FollowupForm, LinkchurchForm, convertForm, new_convert_First_FollowupForm, new_convert_Followup_call_Form, new_convert_referral_finalize_form
from django.contrib.auth.models import User
from django.contrib import messages
from .filters import ConvertsFilter
from user.models import Profile
from people.forms import Person_Form

# Create your views here.

@login_required
def add_new_convert(request):
    if request.method=='POST':
        form = Person_Form(request.POST)
        form1 = convertForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = User.objects.get(pk=request.user.pk)
            instance.save()
            if form1.is_valid():
                salvationDetails = form1.save(commit=False)
                salvationDetails.convert_id = instance.id
                salvationDetails.save()
            return redirect('add_new_convert')
    else:
        form = Person_Form() 
        form1 = convertForm()
    context= {
        'form': form,
        'form1': form1,
    }
    return render(request, 'SalvationFollowUps/Add_New_Convert.html', context)

@login_required
def new_convert_followup(request):
    Followups_due = salvations.objects.all()
    due_count = Followups_due.count()
    context = {
        'Followups_due': Followups_due,
        'due_count': due_count,
    }
    return render(request, 'SalvationFollowUps/new_Convert_Followup.html', context)

@login_required
def new_Convert_feedback(request, pk):
    followup_convert_new = salvations.objects.get(id=pk)
    try:
        submitted_feedback = new_convert_first_followup.objects.get(convert=pk)
    except:
        submitted_feedback = False
    if request.method=='POST':
        followup_convert_new = salvations.objects.get(id=followup_convert_new.id)
        if submitted_feedback == False:
            form = new_convert_First_FollowupForm(request.POST)
        else:
            form = new_convert_First_FollowupForm(request.POST, instance=submitted_feedback)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.followedup_up_by = request.user
            instance.convert = salvations.objects.get(id=pk)
            instance.save()
            return redirect('new_convert_followup')
    else:
        if submitted_feedback == False:
            form = new_convert_First_FollowupForm()
        else:
            form = new_convert_First_FollowupForm(instance=submitted_feedback)
    

    context = { 
        'followup_convert_new': followup_convert_new,
        'form': form,
    }
    return render(request, 'SalvationFollowUps/new_Convert_feedback.html', context)

@login_required
def new_Convert_feedback_call(request):
    convert = request.GET.get('myVal')
    try:
        submitted_feedback = new_convert_followup_call.objects.get(convert=convert)
    except:
        submitted_feedback = False
    if request.method=='POST':
        submitted_feedback = request.POST.get('submitted_feedback')
        convert = request.POST.get('convert')
        if submitted_feedback == '':
            form = new_convert_Followup_call_Form(request.POST)
        else:
            submitted_feedback = new_convert_followup_call.objects.get(id=submitted_feedback)
            form = new_convert_Followup_call_Form(request.POST, instance=submitted_feedback)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.followedup_up_by = request.user
            instance.convert = salvations.objects.get(id=convert)
            instance.save()
            return redirect('new_convert_followup')
    else:
        if submitted_feedback == False:
            form = new_convert_Followup_call_Form()
        else:
            form = new_convert_Followup_call_Form(instance=submitted_feedback)

    context = {
        'form': form,
        'convert': convert,
        'submitted_feedback': submitted_feedback,
    }
    return render(request, 'SalvationFollowUps/new_Convert_feedback_call.html', context)


@login_required()
def new_convert_referral_finalize_view(request):
    convert = request.GET.get('myVal')
    try:
        submitted_feedback = new_convert_referral_finalize.objects.get(convert=convert)
    except:
        submitted_feedback = False
    if request.method=='POST':
        convert = request.POST.get('convert')
        submitted_feedback = request.POST.get('submitted_feedback')
        print(submitted_feedback)
        if submitted_feedback == "False":
            form = new_convert_referral_finalize_form(request.POST)
        else:
            submitted_feedback = new_convert_referral_finalize.objects.get(convert=convert)
            form = new_convert_referral_finalize_form(request.POST, instance=submitted_feedback)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.followedup_up_by = request.user
            instance.convert = salvations.objects.get(id=convert)
            instance.save()
            return redirect('new_convert_followup')
    if submitted_feedback == False:
        form = new_convert_referral_finalize_form()
    else:
        form = new_convert_referral_finalize_form(instance=submitted_feedback)
    context = {
        'convert': convert,
        'form': form,
        'submitted_feedback': submitted_feedback,
    }
    return render(request, 'SalvationFollowups/new_Convert_feedback_refer_finalize.html', context)

##### OLD VIEWS NEED TO BE REMOVED
@login_required
def index(request):
    followUps = Followups.objects.all()
    converts = Converts.objects.all()
    venues = Converts.conversionVenues(converts)
    totalCatConversions = Converts.catConversionTotal(converts, venues)
    attendCat = Followups.AttendChurchCat(followUps)
    attendCatTotal = Followups.churchAttendCatTotals(followUps, attendCat)
    volunteers = User.objects.all()
    volunteers_count = volunteers.count()
    converts_count = converts.count()
    followUpdue = Followups.objects.filter(next_followUpdate__lte=datetime.date.today())
    FollowUpdue_count = followUpdue.count()
    connect_church = Followups.objects.filter(AttendChurch='Away: want to be connected')
    connect_church_count = connect_church.count()
        
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = User.objects.get(pk=request.user.pk)         
            instance.save()
            return redirect('dashboard-index')
    else:
        form = PrayerRequestForm()
    context = {
        'followUps': followUps,
        'form': form,
        'converts': converts,
        'venues': venues,
        'totalCatConversions': totalCatConversions,
        'attendCat': attendCat,
        'attendCatTotal': attendCatTotal,
        'converts_count': converts_count,
        'volunteers_count': volunteers_count,
        'FollowUpdue_count': FollowUpdue_count,
        'connect_church_count': connect_church_count,

    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    volunteers = User.objects.all()
    volunteers_count = volunteers.count()
    converts = Converts.objects.all()
    converts_count = converts.count()
    followUpdue = Followups.objects.filter(next_followUpdate__lte=datetime.date.today())
    FollowUpdue_count = followUpdue.count()
    connect_church = Followups.objects.filter(AttendChurch='Away: want to be connected')
    connect_church_count = connect_church.count()

    context = {
        'volunteers': volunteers,
        'volunteers_count': volunteers_count,
        'converts_count': converts_count,
        'FollowUpdue_count': FollowUpdue_count,
        'connect_church_count': connect_church_count
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    workers =  User.objects.get(id=pk)
    volunteers = User.objects.all()
    volunteers_count = volunteers.count()
    converts = Converts.objects.all()
    converts_count = converts.count()
    FollowUp = Followups.objects.all()
    FollowUpdue_count = FollowUp.count()
    connect_church = Followups.objects.filter(AttendChurch='Away: want to be connected')
    connect_church_count = connect_church.count()

    context = {
        'workers': workers,
        'volunteers_count': volunteers_count,
        'converts_count': converts_count,
        'FollowUpdue_count': FollowUpdue_count,
        'connect_church_count': connect_church_count
    }
    return render(request, 'dashboard/staff_detail.html', context)


@login_required
def converts_delete(request, pk):
    convert = Converts.objects.get(id=pk)
    if request.method=='POST':
        convert.delete()
        return redirect('dashboard-salvations')
    return render(request, 'dashboard/salvations_delete.html')

@login_required
def converts_update(request, pk):
    convert = Converts.objects.get(id=pk)
    if request.method=='POST':
        form = ConvertsForm(request.POST, instance=convert)
        if form.is_valid():
            form.save()
            return redirect('dashboard-salvations')
    else:
        form = ConvertsForm(instance=convert)
    context= {
        'form': form
    }
    return render(request, 'dashboard/salvations_update.html', context)


@login_required
def Followup_due(request):
    FollowUp = Followups.objects.all()
    Feedback = Requests_Feedback.objects.all()
    volunteers = User.objects.all()
    volunteers_count = volunteers.count()
    converts = Converts.objects.all()
    converts_count = converts.count()
    followUpdue = Followups.objects.filter(next_followUpdate__lte=datetime.date.today())
    FollowUpdue_count = followUpdue.count()
    connect_church = Followups.objects.filter(AttendChurch='Away: want to be connected')
    connect_church_count = connect_church.count()
    followed_up = Followed_Up_by.objects.select_related('convert').all()

    

    context= {
        'FollowUp': FollowUp,
        'Feedback': Feedback,
        'volunteers_count': volunteers_count,
        'converts_count': converts_count,
        'FollowUpdue_count': FollowUpdue_count,
        'followUpdue': followUpdue,
        'connect_church_count': connect_church_count,
        'followed_up': followed_up,
        
    }
    return render(request, 'dashboard/followup_due.html', context)

@login_required
def followup(request, pk):
    connect = Followups.objects.get(convert_id=pk)
    name = connect.convert
    if request.method=='POST':
        form = FollowupForm(request.POST, instance=connect)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = User.objects.get(pk=request.user.pk)
            instance.save()
            obj = Followed_Up_by.objects.latest('id')
            obj.createdby = User.objects.get(pk=request.user.pk)
            obj.save()
            return redirect('dashboard-followup_due')
    else:
        form = FollowupForm(instance=connect)
    context= {
        'form': form,
        'name': name
    }
    return render(request, 'dashboard/followup.html', context)

@login_required
def church_connect(request):
    volunteers = User.objects.all()
    volunteers_count = volunteers.count()
    converts = Converts.objects.all()
    converts_count = converts.count()
    connect_church = Followups.objects.filter(AttendChurch='Away: want to be connected')
    connect_church_count = connect_church.count()
    FollowUps = Followups.objects.all()
    followUpdue = Followups.objects.filter(next_followUpdate__lte=datetime.date.today())
    FollowUpdue_count = followUpdue.count()
    context = {
        'FollowUps': FollowUps,
        'volunteers_count': volunteers_count,
        'converts_count': converts_count,
        'FollowUpdue_count': FollowUpdue_count,
        'connect_church': connect_church,
        'connect_church_count': connect_church_count
    }
    return render(request, 'dashboard/find_church.html', context)

@login_required
def church_connect_link(request, pk):
    connect = Followups.objects.get(convert_id=pk)
    name = connect.convert
    if request.method=='POST':
        form = LinkchurchForm(request.POST, connect)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = User.objects.get(pk=request.user.pk)
            instance.convert = connect
            obj = connect
            obj.AttendChurch = 'Connected'
            obj.save()
            instance.save()
            return redirect('dashboard-church-connect')
    else:
        form = LinkchurchForm(instance=connect)
    context= {
        'form': form,
        'name': name,
    }
    return render(request, 'dashboard/church_connect.html', context)