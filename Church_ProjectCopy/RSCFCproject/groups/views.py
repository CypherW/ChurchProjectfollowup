from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Count, Q
from SalvationFollowUps.models import Converts
from visitors.models import visit_date
from people.models import People, guardianRelation
from .models import session_attendance, group_membership, session_attended_options, prayer_cell_feedback, session_absent
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from .forms import Person_Form, Date_Attended_Form, group_type_select, present_select_fieldsForm, prayer_cell_feedbackForm, absentee_followup_form, multiple_Group_absentee_feedback_form, remove_from_group_form
from django.template import RequestContext
from .filters import group_meetingsFilter
from datetime import datetime
from django.utils import timezone
from django_htmx.http import trigger_client_event
from django.core.mail import send_mail
from django.db import IntegrityError
import json, random

# Create your views here.
@login_required
def group_attendance(request):
    if request.method=='POST':
        group_leader_id = request.user.id
        form = Date_Attended_Form(group_leader_id, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            meeting = instance.session_attended
            date = instance.dateofvisit
            instance.createdBy = User.objects.get(pk=request.user.pk)
            return redirect('prayer_cell_feedback_form/?meeting={}&date={}'.format(meeting, date))

    else:
        group_leader_id = request.user.id
        form = Date_Attended_Form(group_leader_id)
    visitors = People.objects.order_by('Name')

    context = {
        'visitors': visitors,
        'form': form,

    }
    
    return render(request, 'groups/attendance.html', context)


@login_required
def load_session_members(request):
    session_id = request.GET.get('session_attended')
    date_of_visit = request.GET.get('dateofvisit')
    attendee_list = session_attendance.objects.filter(dateofvisit=date_of_visit, session_attended=session_id).values_list('attendee')
    attendee_list_count = attendee_list.count()
    member_list = group_membership.objects.filter(group_id=session_id, active=True)
    attendee_list = list(attendee_list.values_list('attendee_id', flat=True))
    member_list = member_list.exclude(member_id__in=attendee_list)
    member_list = member_list.order_by('member_id__Name')
    
    context = {
        'members': member_list,
        'attendee_list_count': attendee_list_count,
    }
    return render(request, 'groups/load_session_members.html', context)

@login_required
def load_searchByTyping_add_present(request):
    session_id = request.GET.get('session_attended')
    date_of_visit = request.GET.get('dateofvisit')
    attendee_list = session_attendance.objects.filter(dateofvisit=date_of_visit, session_attended=session_id).values_list('attendee')
    attendee_list_count = attendee_list.count()
    search_term = request.GET.get('search')
    member_list = group_membership.objects.filter(group_id=session_id, active=True)
    attendee_list = list(attendee_list.values_list('attendee_id', flat=True))
    member_list = member_list.exclude(member_id__in=attendee_list)
    member_list = member_list.order_by('member_id__Name')
    member_list = member_list.filter(
            member__Name__istartswith=search_term) | member_list.filter(
            member__Surname__istartswith=search_term)
    context = {
        'members': member_list,
        'attendee_list_count': attendee_list_count,
    }
    return render(request, 'groups/load_session_members.html', context)

@login_required
def mark_attendee_present(request, pk):
    session_id = request.GET.get('session_attended')
    date_of_visit = request.GET.get('dateofvisit')
    session_id = session_attended_options.objects.get(pk=session_id)
    attendee = People.objects.get(id=pk)

    session_attendance.objects.create(
                    attendee= attendee,
                    dateofvisit=date_of_visit,
                    session_attended=session_id,
                    createdby_id=request.user.id
                )
    response = HttpResponse('')
    trigger_client_event(response, 'mark_attendee_present')
    return response

@login_required
def update_attending_count(request):
    date_of_visit = request.GET.get('dateofvisit')
    session_id = request.GET.get('session_attended')
    attendee_list = session_attendance.objects.filter(dateofvisit=date_of_visit, session_attended=session_id).values_list('attendee')
    attendee_list_count = attendee_list.count()
    context = { 'attendee_list_count': attendee_list_count}
    return render(request, "groups/update_attending_count.html", context)

@login_required
def prayer_cell_check_present(request):
    session_id = request.GET.get('session_attended')
    date_of_visit = request.GET.get('dateofvisit')
    attendee_list = session_attendance.objects.filter(dateofvisit=date_of_visit, session_attended=session_id)
    attendee_list = attendee_list.order_by('attendee_id__Name')
    count = attendee_list.count()
    my_date = datetime.strptime(date_of_visit, "%Y-%m-%d")
    formatted_date = my_date.strftime("%d %B %Y")

    context = {
        'count': count,
        'attendee_list': attendee_list,
        'session_date': formatted_date,
    }

    return render(request, 'groups/prayer_cell_check_present.html', context)

@login_required
def prayer_cell_feedback_form(request):
    if request.method=='POST':
        form = prayer_cell_feedbackForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.date_of_meeting = request.GET.get('date')
                instance.disciple_leader_id = request.user.id
                meeting = request.GET.get('meeting')
                session_attended = session_attended_options.objects.get(session_attended=meeting)
                instance.meeting_hosted_id = session_attended.id
                instance.save()
                attendee_list = session_attendance.objects.filter(dateofvisit=instance.date_of_meeting, session_attended=instance.meeting_hosted_id).values_list('attendee')
                member_list = group_membership.objects.filter(group_id=instance.meeting_hosted_id, active=True)
                attendee_list = list(attendee_list.values_list('attendee_id', flat=True))
                member_list = member_list.exclude(member_id__in=attendee_list)
                member_list = member_list.order_by('member_id__Name')
                for member in member_list:
                    absentee = People.objects.get(id= member.member_id)
                    group_absent_instance = session_absent(absentee=absentee)
                    group_absent_instance.dateofmeeting = instance.date_of_meeting
                    group_absent_instance.session_missed = session_attended
                    group_absent_instance.save()
                return redirect('group_attendance')
            except IntegrityError:
                # Handle unique constraint violation
                meeting_date = request.GET.get('date')
                meeting = request.GET.get('meeting')
                meeting_hosted_id = session_attended.id
                duplicate_form = prayer_cell_feedback.objects.get(date_of_meeting=meeting_date, meeting_hosted=meeting_hosted_id)
                return render(request, 'groups/feedback_form_already_submitted.html', {
                    'form': form,
                    'duplicate_form': duplicate_form,
                })
    else:
        form = prayer_cell_feedbackForm()
    meeting = request.GET.get('meeting')
    session_attended = session_attended_options.objects.get(session_attended=meeting)
    date = request.GET.get('date')
    date = datetime.strptime(date, "%Y-%m-%d")
    date = date.strftime("%d %B %Y")
    context= {
        'form': form,
        'meeting': meeting,
        'date': date,
    }
    return render(request, 'groups/prayer_cell_feedbackForm.html', context)

@login_required
def group_person_detail(request, pk):
    person =  People.objects.get(id=pk)
    parents = guardianRelation.objects.filter(child=pk).values()
    parentlist = []
    for obj in parents:
        parentlist.append(People.objects.get(id=obj['parent_id']))
    parents = parentlist
    children = guardianRelation.objects.filter(parent=pk).values()
    childrenlist = []
    for obj in children:
        childrenlist.append(People.objects.get(id=obj['child_id']))
    children = childrenlist
    groups = group_membership.objects.filter(member=pk)
    grouplist = []
    for obj in groups:
        grouplist.append(session_attended_options.objects.get(id=obj.group_id))
    groups = grouplist
    groupstring = ''
    for group in groups:
        groupstring += group.session_attended + ', '
    groups = groupstring.rstrip(', ')
    context = {
        'person': person,
        'parents': parents,
        'children': children,
        'groups': groups,
        
    }
    return render(request, 'groups/person_detail.html', context)

@login_required()
def edit_person_details(request, pk):
    person = People.objects.get(id=pk)
    if request.method=='POST':
        edit_form = Person_Form(request.POST, instance=person)
        if edit_form.is_valid():
            edit_form.save()
            redirect_url = f'/groups/person/{person.id}'
            return redirect(redirect_url)
    else:
        edit_form = Person_Form(instance=person)
    context = {
        'edit_form': edit_form,
        'person': person,
    }
    return render(request, 'groups/editPerson_details.html', context)

@login_required    
def group_addPersonForm(request):
    if request.method=='POST':
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
                groupAddedto = session_attended_options.objects.get(pk=check)
                group_membership_instance = group_membership(member=newMember)
                group_membership_instance.group = groupAddedto
                group_membership_instance.active = True
                group_membership_instance.save()
            add_guardian = request.POST.get('add_guardian')
            guardian_entered = request.POST.get('guardian_entered')
            if add_guardian == 'add_guardian':
                newMember = People.objects.get(pk=obj.id)
                if guardian_entered == 'no':
                    redirect_url = f'/groups/addPerson_Parent/{newMember.id}'
                    return redirect(redirect_url)
                elif guardian_entered == 'yes':
                    redirect_url = f'/groups/addPerson_existingParent/{newMember.id}'
                    return redirect(redirect_url)
            return redirect('group_attendance')
    else:
        form = Person_Form()
    group_options = session_attended_options.objects.all()
    context= {
        'form': form,
        'group_options': group_options,
    }
    return render(request, 'groups/addPerson.html', context)

@login_required()
def check_person_exists(request):
    if request.method=='POST':
        checks = request.POST.getlist('checks[]')
        person_id = request.POST.get('person')
        for check in checks:
                newMember = People.objects.get(pk=person_id)
                groupAddedto = session_attended_options.objects.get(pk=check)
                exists = group_membership.objects.filter(member=newMember, group=groupAddedto).exists()
                if exists == False:
                    group_membership_instance = group_membership(member=newMember)
                    group_membership_instance.group = groupAddedto
                    group_membership_instance.active = True
                    group_membership_instance.save()
        return redirect('/groups')

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
    return render(request, 'groups/check_person_exists_modal.html', context)

    


@login_required    
def addPerson_Parent(request, pk):
    if request.method=='POST':
        form = Person_Form(request.POST)
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
            checks = request.POST.getlist('checks[]')
            for check in checks:
                newMember = People.objects.get(pk=obj.id)
                groupAddedto = session_attended_options.objects.get(pk=check)
                group_membership_instance = group_membership(member=newMember)
                group_membership_instance.group = groupAddedto
                group_membership_instance.active = True
                group_membership_instance.save()
            
                
            return redirect('group_attendance')
    else:
        form = Person_Form()
    context= {
        'form': form,
    }
    return render(request, 'groups/addPerson_Parent.html', context)

@login_required
def addPerson_existingParent(request, pk):
    child = People.objects.get(pk=pk)
    context = {
        'child': child,

    }
    return render(request, 'groups/addParent_existing.html', context)

@login_required
def load_searchByTyping_add_parent(request):
    search_term = request.GET.get('search')
    parent_list = People.objects.all()
    child = request.GET.get('myVariable')
    parent_list = parent_list.exclude(id=child)
    parent_list = parent_list.order_by('Name')
    parent_list = parent_list.filter(
            Name__istartswith=search_term) | parent_list.filter(
            Surname__istartswith=search_term)
    context = {
        'parent_list': parent_list,
        'child': child,
    }
    return render(request, 'groups/load_searchByTyping_add_parent.html', context)

@login_required
def load_searchByTyping_add_parent_selectedParent(request):
    parent = request.GET.get('parentName')
    child = request.GET.get('child_id')
    context = {
        'parent': parent,
        'child': child,
    }
    return render(request, 'groups/load_searchByTyping_add_parent_selectedParent.html', context)

@login_required
def confirmed_exisiting_parent(request):
    try:
        if request.method == 'POST':
            parent = request.POST.get('parentName')
            child_id = request.POST.get('child_id')
            child = People.objects.get(pk=child_id)
            parent = parent.split(' ')
            parentName = parent[0]
            parentSurname = parent[1]
            parent = People.objects.get(Name=parentName, Surname=parentSurname)
            guardianRelation_instance = guardianRelation(parent=parent)
            guardianRelation_instance.child = child
            guardianRelation_instance.save()
            response = JsonResponse({'location': '/groups/'})
            response['HX-Redirect'] = '/groups/'
            return response
    except Exception as e:
        return JsonResponse({'error': 'An error occurred'}, status=500)
    else:
        print('Request method is not POST')
        return redirect('group_attendance')



@login_required
def isguardian_entered(request):
    return render(request, 'groups/isguardian_entered.html')

@login_required    
def present_bysession(request):
    group_leader_id = request.user.id
    form = present_select_fieldsForm(group_leader_id)
    context= {
        'form': form,
    }
    return render(request, 'groups/present_bysession.html', context)

@login_required
@permission_required('groups.view_prayer_cell_feedback', raise_exception=True)
def meeting_occurrences(request):
    session = session_attendance.objects.all()
    eventFilter = group_meetingsFilter(request.GET, queryset=session)
    meetings_last_thirty_days = session_attendance.objects.filter(dateofvisit__gte=timezone.now() - timezone.timedelta(days=30)).distinct('dateofvisit', 'session_attended')
    meetings_last_thirty_days = meetings_last_thirty_days.order_by('-dateofvisit')
    meetings_last_thirty_days = [meetings_last_thirty_days[i:i + 3] for i in range(0, len(meetings_last_thirty_days), 3)]
    form = group_type_select()

    context= {
        'eventFilter': eventFilter,
        'session': session,
        'form': form,
        'meetings_last_thirty_days': meetings_last_thirty_days,
        
    }

    return render(request, 'groups/group_meetings.html', context)

@login_required
def load_dates_present_by_session(request):
    session_id = request.GET.get('meeting_attended')
    dates = session_attendance.objects.filter(session_attended=session_id).order_by('dateofvisit').distinct('dateofvisit')
    dates = [session.dateofvisit.strftime('%d %B %Y') for session in dates]
    dates.append('----')
    dates.reverse()

    context = {
        'dates': dates,
    }
    return render(request, "groups/present_date_options.html", context)

@login_required
def load_category_select_present_table(request):
    date= request.GET.get('date')
    session_id = request.GET.get('meeting_attended')
    formatted_date = datetime.strptime(date, "%d %B %Y")
    attendee_list = session_attendance.objects.filter(dateofvisit=formatted_date, session_attended=session_id)
    attendee_list = attendee_list.order_by('attendee_id__Name')
    count = attendee_list.count()

    context = {
        'count': count,
        'attendee_list': attendee_list,
    }
    return render(request, "groups/category_select_present_table.html", context)

@login_required
def load_searchByTyping_attending(request):
    date = request.GET.get('date')
    session_id = request.GET.get('meeting_attended')
    search_term = request.GET.get('search')
    formatted_date = datetime.strptime(date, "%d %B %Y")
    attendee_list = session_attendance.objects.filter(dateofvisit=formatted_date, session_attended=session_id)
    attendee_list = attendee_list.order_by('attendee_id__Name')
    count = attendee_list.count()
    attendee_list = attendee_list.filter(
            attendee__Name__istartswith=search_term) | attendee_list.filter(
            attendee__Surname__istartswith=search_term)
    context = {
        'count': count,
        'attendee_list': attendee_list
    }

    return render(request, "groups/category_select_present_table.html", context)

@login_required
@require_http_methods('DELETE')
def remove_attendee(request, pk):
    attendee = get_object_or_404(session_attendance, pk=pk)
    attendee.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = json.dumps({"remove_attendee": "remove_attendee"})
    response = trigger_client_event(response, 'remove_attendee')
    return response

@login_required
def update_present_count(request):
    date = request.GET.get('date')
    formatted_date = datetime.strptime(date, "%d %B %Y")
    session_id = request.GET.get('meeting_attended')
    attendee_list = session_attendance.objects.filter(dateofvisit=formatted_date, session_attended=session_id)
    count = attendee_list.count()
    context = {'count': count}
    return render(request, "groups/update_present_count.html", context)


@login_required
def load_event_dates(request):
    event_type = request.GET.get('session_attended_options')
    dates = session_attendance.objects.filter(session_attended=event_type).order_by('dateofvisit').distinct('dateofvisit')
    dates = [session.dateofvisit.strftime('%d %B %Y') for session in dates]
    dates.reverse()
    dates = [dates[i:i + 3] for i in range(0, len(dates), 3)]    
    print('load_event_dates')
    context = {
        'dates': dates,
    }
    return render(request, "groups/event_dates.html", context)

@login_required
def load_event_date_attendance(request):
    date = request.GET.get('myVariable')
    session_id = request.GET.get('session_attended_options')
    if session_id == '':
        session_id = request.GET.get('session_id')
    formatted_date = datetime.strptime(date, "%d %B %Y")
    attendee_list = session_attendance.objects.filter(dateofvisit=formatted_date, session_attended=session_id)
    count = attendee_list.count()
    member_list = group_membership.objects.filter(group_id=session_id, active=True)
    members = member_list.count()
    absentee_list = session_absent.objects.filter(dateofmeeting=formatted_date, session_missed=session_id)
    absent = absentee_list.count()
    id_add = random.randint(1,100)*random.randint(1,100)
    id_add = str(id_add)
    try:
        groupFeedback = prayer_cell_feedback.objects.get(meeting_hosted_id=session_id, date_of_meeting=formatted_date)
        groupFeedback = groupFeedback.word_discussed
    except:
        groupFeedback = 'No feedback provided'
    
    context = {
        'count': count,
        'absent': absent,
        'groupFeedback': groupFeedback,
        'date': date,
        'id_add': id_add,
        'session_id': session_id,
                        }
    
    return render(request, "groups/load_event_date_attendance.html", context)

@login_required
def noFeedback_button(request):
    date = request.GET.get('eventDate')
    session_id = request.GET.get('session_attended_options')
    if session_id == '':
        session_id = request.GET.get('session_id')
    meetingName = session_attended_options.objects.get(id=session_id)
    leader = User.objects.get(pk=meetingName.group_leader_id)
    requester = request.user.username
    leaderEmail = leader.email
    send_mail("FEEDBACK FOR MEETING",
f"""Dear {leader}, 
    
You had a meeting on {date} but did not submit feedback. Please could you submit feedback for this meeting at your earliest convenience?
     
Kind Regards,

Pastor {requester}
       
         """,
    "shodandevstesting@gmail.com",
    [leaderEmail],
    fail_silently=False,
)
    return render(request, "groups/noFeedback_button.html")

@login_required
def display_event_feedback_modal(request):
    date = request.GET.get('eventDate')
    session_id = request.GET.get('session_attended_options')
    if session_id == '':
        session_id = request.GET.get('session_id')
        print('blank')
    formatted_date = datetime.strptime(date, "%d %B %Y")
    session = session_attended_options.objects.get(id=session_id)
    feedback = prayer_cell_feedback.objects.get(date_of_meeting=formatted_date, meeting_hosted=session_id)
    context = { 
        'session': session,
        'date': date,
        'feedback': feedback,
          }
    return render(request, "groups/display_event_feedback_modal.html", context)

@login_required
def display_event_absent_modal(request):
    date = request.GET.get('eventDate')
    session = request.GET.get('session')
    session_id = session_attended_options.objects.get(session_attended=session)
    formatted_date = datetime.strptime(date, "%d %B %Y")
    absentee_list = session_absent.objects.filter(dateofmeeting=formatted_date, session_missed=session_id)
    absentee_count = absentee_list.count()
    absentee_list = absentee_list.order_by('absentee_id__Name')
    context = { 
        'date': date,
        'session': session,
        'absentee_list': absentee_list,
        'absentee_count': absentee_count,

          }
    return render(request, "groups/display_event_absent_modal.html", context)

@login_required
def display_absentee_feedback_modal(request):
    absentee = request.GET.get('absent_instance')
    absentee = session_absent.objects.get(id=absentee)
    followup_date = absentee.follow_up_date
    date = request.GET.get('eventDate')
    session = request.GET.get('session')
    session_id = session_attended_options.objects.get(session_attended=session)
    formatted_date = datetime.strptime(date, "%d %B %Y")
    absentee_list = session_absent.objects.filter(dateofmeeting=formatted_date, session_missed=session_id)
    absentee_count = absentee_list.count()
    absentee_list = absentee_list.order_by('absentee_id__Name')
    context = { 
        'date': date,
        'session': session,
        'absentee_list': absentee_list,
        'absentee_count': absentee_count,
        'absentee': absentee,
        'followup_date': followup_date,

          }
    return render(request, "groups/display_absentee_feedback_modal.html", context)

@login_required
def display_event_present_modal(request):
    date = request.GET.get('eventDate')
    session = request.GET.get('session')
    session_id = session_attended_options.objects.get(session_attended=session)
    formatted_date = datetime.strptime(date, "%d %B %Y")
    attendee_list = session_attendance.objects.filter(dateofvisit=formatted_date, session_attended=session_id)
    attendee_list = attendee_list.order_by('attendee_id__Name')
    present_count = attendee_list.count()
    context = { 
        'date': date,
        'session': session,
        'attendee_list': attendee_list,
        'present_count': present_count,

          }
    return render(request, "groups/display_event_present_modal.html", context)

@login_required
def redirect_display_event_feedback_modal(request):
    date = request.GET.get('eventDate')
    session_id = request.GET.get('session_attended_options')
    formatted_date = datetime.strptime(date, "%d %B %Y")
    session = session_attended_options.objects.get(session_attended=session_id)
    feedback = prayer_cell_feedback.objects.get(date_of_meeting=formatted_date, meeting_hosted=session.id)
    context = { 
        'session': session,
        'date': date,
        'feedback': feedback, 
          }
    return render(request, "groups/display_event_feedback_modal.html", context)

@login_required
def add_toGroupForm(request):
    group_options = session_attended_options.objects.all()
    context = {
        'group_options': group_options
    }
    return render(request, 'groups/add_toGroupForm.html', context)

@login_required
def group_absent_followup(request):
    group_leader = request.user.id
    group = session_attended_options.objects.filter(group_leader_id=group_leader)
    if len(group) == 1:
        group = group[0]
        absentees = session_absent.objects.filter(session_missed_id=group.id, follow_up_Feedback=None)
        absentee_count = absentees.count()
        form = '0'
    else:
        absentees = '0'
        absentee_count = '0'
        group_leader_id = request.user.id
        form = multiple_Group_absentee_feedback_form(group_leader_id) 

    context = {
        'group': group,
        'absentees': absentees,
        'absentee_count': absentee_count,
        'form': form,
    }

    return render(request, 'groups/group_absent_followup.html', context)

@login_required
def multi_group_absent_followup_selected(request):
    group_leader = request.user.id
    session = request.GET.get('session_attended')
    group = session_attended_options.objects.get(id=session)
    absentees = session_absent.objects.filter(session_missed_id=group.id, follow_up_Feedback=None)
    absentee_count = absentees.count()
    context = {
        'absentees': absentees,
        'absentee_count': absentee_count,
        'session': session,
    }
   

    return render(request, 'groups/multi_group_absent_followup_selected.html', context)

@login_required
def multi_group_view_Previous_feedback_button(request):
    session = request.GET.get('session')
    group = session_attended_options.objects.get(id=session)

    context = {
        'group': group
    }
    return render(request, 'groups/multi_group_view_Previous_feedback_button.html', context)

@login_required
def group_absentee_followup(request, pk):
    absentee = session_absent.objects.get(pk=pk)
    if request.method=='POST':
        form = absentee_followup_form(request.POST, instance=absentee)
        form.save()
        return redirect('group_absent_followup')
    else:
        form = absentee_followup_form(instance=absentee)

    context = {
        'absentee': absentee,
        'form': form,
    }

    return render(request, 'groups/group_absentee_followup.html', context)

@login_required
def group_remove_member(request, pk):
    absentee = session_absent.objects.get(pk=pk)
    if request.method=='POST':
        form = remove_from_group_form(request.POST, instance=absentee)
        instance = form.save(commit=False)
        session_id = instance.session_missed_id
        if form.is_valid():
            reason = form.cleaned_data['reason_leaving']
        absentee_id = instance.absentee_id
        membership_obj = group_membership.objects.get(group_id=session_id, member_id=absentee_id)
        membership_obj.active = False
        membership_obj.save()
        meeting_missed_obj = session_absent.objects.get(id=pk)
        meeting_missed_obj.follow_up_Feedback = "Has left group: " + reason
        meeting_missed_obj.save()


        return redirect('group_absent_followup')
    else:
        form = remove_from_group_form(instance=absentee)

    context = {
        'absentee': absentee,
        'form': form,
    }

    return render(request, 'groups/group_remove_member.html', context)

@login_required
def group_absent_view_feedback(request, meeting):
    group = session_attended_options.objects.get(session_attended=meeting)
    absentees = session_absent.objects.filter(session_missed_id=group.id, follow_up_Feedback__isnull=False).order_by('-dateofmeeting')
    context = {
        'group': group,
        'absentees': absentees,
    }

    return render(request, 'groups/group_absent_view_feedback.html', context)

@login_required
def group_absentee_view_feedback(request, pk):
    absentee = session_absent.objects.get(pk=pk)
    meeting = 'Ylife'
    
    context = {
        'absentee': absentee,
        'meeting': meeting,
    }

    return render(request, 'groups/group_absentee_view_feedback.html', context)