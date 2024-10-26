from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import service_counts, childrensChurch_classes, childrensChurch_class_member, service_attended, class_attendance
from people.models import People, guardianRelation
from groups.models import session_attendance
from visitors.models import visit_details
from SalvationFollowUps.models import salvations
from django.contrib.auth.models import User
from .forms import service_count_form, Person_Form, Parent_Form, childrensChurchAttendanceForm
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django_htmx.http import trigger_client_event



# Create your views here.
@login_required
def service_countspage(request):
    date = timezone.now().date()
    try:
        previous_submission = service_counts.objects.get(dateofmeeting=date)
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
        else:
            offset = (today.weekday() + 1) % 7
            previous_sunday = today - timezone.timedelta(days=offset)
        return previous_sunday - timezone.timedelta(weeks=weeks_ago)

    def get_next_saturday(sunday_date):
        next_saturday = sunday_date + timezone.timedelta(days=6)
        return next_saturday
    
    today = timezone.localtime()


    # Get the most recent Sunday and the following Saturday
    most_recent_sunday = get_previous_sunday()
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
        childrens_church_count_1st = class_attendance.objects.filter(dateofclass=most_recent_sunday, service='1').values_list('child')
        childrens_church_count_1st = childrens_church_count_1st.count()
       
    except:
        childrens_church_count_1st = 0

    try:
        childrens_church_count_2nd = class_attendance.objects.filter(dateofclass=most_recent_sunday, service='2').values_list('child')
        childrens_church_count_2nd = childrens_church_count_2nd.count()
       
    except:
        childrens_church_count_2nd = 0
        
    childrens_church_total = childrens_church_count_1st + childrens_church_count_2nd
    
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
        'childrens_church_count_1st': childrens_church_count_1st,
        'childrens_church_count_2nd': childrens_church_count_2nd,
        'childrens_church_total': childrens_church_total,
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


@login_required
def childrens_church_attendance(request):
    form = childrensChurchAttendanceForm('request.user.pk')
    user_id = request.user.pk
    context = {
        'form': form,
        'user_id': user_id,

    }
    return render(request, 'services/childrens_church_attendance.html', context)

@login_required
def addPerson_childrens_church(request):
    form = Person_Form(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.createdBy = User.objects.get(pk=request.user.pk)
        instance.save()
        obj = People.objects.latest('id')
        obj.createdby = User.objects.get(pk=request.user.pk)
        obj.save()
        checks = request.POST.getlist('checks[]')
        for check in checks:
            newMember = People.objects.get(pk=obj.id)
            classAddedto = childrensChurch_classes.objects.get(pk=check)
            class_membership_instance = childrensChurch_class_member(child=newMember)
            class_membership_instance.class_attending = classAddedto
            class_membership_instance.active = True
            class_membership_instance.save()
        newMember = People.objects.get(pk=obj.id)
        redirect_url = f'/services/addPerson_Parent/{newMember.id}'
        return redirect(redirect_url)
    else:
        form = Person_Form()
        class_options = childrensChurch_classes.objects.all()
    context = {
        'form':form, 
        'class_options': class_options,
    }
    return render(request, 'services/addPerson_childrens_church.html', context)

@login_required    
def addPerson_Parent(request, pk):
    if request.method=='POST':
        form = Parent_Form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = User.objects.get(pk=request.user.pk)
            instance.save()
            obj = People.objects.latest('id')
            obj.createdby = User.objects.get(pk=request.user.pk)
            obj.save()
            parent = People.objects.get(pk=obj.id)
            child = get_object_or_404(People, pk=pk)
            guardianRelation_instance = guardianRelation(parent=parent)
            guardianRelation_instance.child = child
            guardianRelation_instance.save()
            
                
            return redirect('addPerson_childrens_church')
    else:
        form = Parent_Form()
        child = pk
        child_detail = People.objects.get(id=pk)
    context= {
        'form': form,
        'child': child,
        'child_detail': child_detail,
    }
    return render(request, 'services/addPerson_Parent.html', context)

@login_required()
def check_person_exists(request):
    if request.method=='POST':
        checks = request.POST.getlist('checks[]')
        person_id = request.POST.get('person')
        for check in checks:
                newMember = People.objects.get(pk=person_id)
                classAddedto = childrensChurch_classes.objects.get(pk=check)
                exists = childrensChurch_class_member.objects.filter(child=newMember, class_attending=classAddedto).exists()
                if exists == False:
                    childrensChurch_class_member_instance = childrensChurch_class_member(child=newMember)
                    childrensChurch_class_member_instance.class_attending = classAddedto
                    childrensChurch_class_member_instance.active = True
                    childrensChurch_class_member_instance.save()
        add_guardian = request.POST.get('add_guardian')
        guardian_entered = request.POST.get('guardian_entered')
        if add_guardian == 'add_guardian':
            newMember = People.objects.get(pk=obj.id)
            if guardian_entered == 'no':
                redirect_url = f'/services/addPerson_Parent/{newMember.id}'
                return redirect(redirect_url)
            elif guardian_entered == 'yes':
                redirect_url = f'/groups/addPerson_existingParent/{newMember.id}'
                return redirect(redirect_url)
        return redirect('addPerson_childrens_church')
    
    name = request.GET.get('Name')
    name = name.strip()
    exists = False
    surname = request.GET.get('Surname').strip()
    if len(name) > 1 and len(surname) > 1:
       exists = People.objects.filter(Name=name, Surname=surname).exists()
       if exists == True:
        person = People.objects.get(Name=name, Surname=surname)
    context = {
          'exists': exists,
          'person': person,
       }
    return render(request, 'services/check_person_exists_modal.html', context)

@login_required()
def check_parent_exists(request):
    if request.method=='POST':
        child = request.POST.get('child')
        parent = request.POST.get('person')
        obj = guardianRelation.objects.create(parent_id=parent, child_id=child)
        obj.save()

        return redirect('addPerson_childrens_church')
    
    name = request.GET.get('Name')
    name = name.strip()
    exists = False
    surname = request.GET.get('Surname').strip()
    if len(name) > 1 and len(surname) > 1:
       exists = People.objects.filter(Name=name, Surname=surname).exists()
       if exists == True:
        person = People.objects.get(Name=name, Surname=surname)
    child =  request.GET.get('child')
    child = People.objects.get(id=child)
    context = {
          'exists': exists,
          'person': person,
          'child': child,
       }
    return render(request, 'services/check_parent_child_modal.html', context)

@login_required
def isguardian_entered(request):
    return render(request, 'services/isguardian_entered.html')

@login_required
def add_toClassForm(request):
    class_options = childrensChurch_classes.objects.all()
    if request.method=='POST':
        pass

    context = {
        'class_options': class_options
    }
    return render(request, 'services/add_toClassForm.html', context)

@login_required
def class_serviceComdinedOptions(request, pk):
    classes = childrensChurch_classes.objects.filter(head_teacher_id=pk).values_list('class_name')
    classes = list(classes.values_list('class_name', flat=True))
    services = service_attended
    combinations = ['----']
    for class_option in classes:
        for service in services:
            combinations.append(str(class_option) + ': ' + str(service[1]))
    context = {

                'combinations': combinations,
            }
    return render(request, 'services/class_serviceCombinedOptions.html', context)

@login_required
def load_class_members(request):
    class_values = request.GET.get('class_attending')
    class_values = class_values.split(':')
    class_id = childrensChurch_classes.objects.get(class_name=class_values[0])
    service_choices = service_attended
    for service in service_choices:
        for descrip in service:
            if descrip == class_values[1].strip():
                class_num_check = class_num
                break
            else:
                class_num = descrip
    date_of_class = request.GET.get('date')
    attendee_list = class_attendance.objects.filter(dateofclass=date_of_class, class_name=class_id.id, service=class_num_check).values_list('child')
    attendee_list_count = attendee_list.count()
    print(attendee_list)
    class_list = childrensChurch_class_member.objects.filter(class_attending_id=class_id.id, active=True)
    print(class_list)

    attendee_list = list(attendee_list.values_list('child_id', flat=True))
    class_list = class_list.exclude(id__in=attendee_list)
    class_list = class_list.order_by('child_id__Name')
    
    context = {
        'members': class_list,
        'attendee_list_count': attendee_list_count,
    }
    return render(request, 'services/load_class_members.html', context)

@login_required
def mark_child_present(request, pk):
    class_values = request.GET.get('class_attending')
    class_values = class_values.split(':')
    class_id = childrensChurch_classes.objects.get(class_name=class_values[0])
    date_of_visit = request.GET.get('date')
    session_id = childrensChurch_classes.objects.get(pk=class_id.id)
    attendee = People.objects.get(id=pk)
    attendee = childrensChurch_class_member.objects.get(child=attendee, class_attending=class_id)
    service_choices = service_attended
    for service in service_choices:
        for descrip in service:
            if descrip == class_values[1].strip():
                class_num_check = class_num
                break
            else:
                class_num = descrip

    class_attendance.objects.create(
                    child= attendee,
                    dateofclass=date_of_visit,
                    class_name=session_id,
                    service=class_num_check,
                    created_by=request.user
                )

    response = HttpResponse('')
    trigger_client_event(response, 'mark_child_present')
    return response

@login_required
def update_class_count(request):
    print('test')
    class_values = request.GET.get('class_attending')
    class_values = class_values.split(':')
    class_id = childrensChurch_classes.objects.get(class_name=class_values[0])
    date_of_visit = request.GET.get('date')
    service_choices = service_attended
    for service in service_choices:
        for descrip in service:
            if descrip == class_values[1].strip():
                class_num_check = class_num
                break
            else:
                class_num = descrip
    attendee_list = class_attendance.objects.filter(dateofclass=date_of_visit, class_name=class_id.id, service=class_num_check).values_list('child')
    print(attendee_list)
    attendee_list_count = attendee_list.count()
    
    context = { 'attendee_list_count': attendee_list_count}
    return render(request, "services/update_class_count.html", context)