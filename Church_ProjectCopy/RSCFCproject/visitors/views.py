from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ConvertsForm, visit_dateInlineFormset, visitorFollowupForm, visit_date_existingPersonForm, Person_Form, visit_detailForm, visitor_First_FollowupForm, visitor_Followup_call_Form, visitor_referral_finalize_form
from .models import visit_date, visit_details, visitor_first_followup, visitor_followup_call, visitor_referral_finalize
from people.models import People
from groups.models import session_attended_options
from campuses.models import campuses_details
from SalvationFollowUps.models import Converts
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.

@login_required
def add_new_visitor(request):
    if request.method=='POST':
        form = Person_Form(request.POST)
        form1 = visit_detailForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = User.objects.get(pk=request.user.pk)
            instance.save()
            if form1.is_valid():
                visitorDetails = form1.save(commit=False)
                visitorDetails.visitor_id = instance.id
                visitorDetails.save()
            return redirect('add_new_visitor')
    else:
        form = Person_Form() 
        form1 = visit_detailForm()
    context= {
        'form': form,
        'form1': form1,
    }
    return render(request, 'visitors/Add_New_Visitor.html', context)

@login_required()
def check_visitor_exists(request):
    if request.method=='POST':
        person_id = request.POST.get('person')
        form1 = visit_detailForm(request.POST)
        if form1.is_valid():
            visitorDetails = form1.save(commit=False)
            visitorDetails.visitor_id = person_id
            visitorDetails.save()
            return redirect('add_new_visitor')
        

    name = request.GET.get('Name')
    name = name.strip()
    exists = False
    form1 = visit_detailForm()
    surname = request.GET.get('Surname').strip()
    if len(name) > 1 and len(surname) > 1:
       exists = People.objects.filter(Name=name, Surname=surname).exists()
       if exists == True:
        person = People.objects.get(Name=name, Surname=surname)
    context = {
          'exists': exists,
          'person': person,
          'form1': form1,
       }
    return render(request, 'visitors/check_visitor_exists_modal.html', context)

@login_required
def visitor_followup(request):
    Followups_due = visit_details.objects.all()
    print(Followups_due)
    finalized = visitor_referral_finalize.objects.filter(finalize=True)
    finalized_list = list(finalized.values_list('visitor_id', flat=True))
    Followups_due = Followups_due.exclude(id__in=finalized_list)
    due_count = Followups_due.count()
    context = {
        'Followups_due': Followups_due,
        'due_count': due_count,
    }
    return render(request, 'visitors/visitor_Followup.html', context)

@login_required
def visitor_feedback(request, pk):
    followup_visitor = visit_details.objects.get(id=pk)
    try:
        submitted_feedback = visitor_first_followup.objects.get(visitor=pk)
    except:
        submitted_feedback = False
    if request.method=='POST':
        followup_visitor_new = visit_details.objects.get(id=followup_visitor.id)
        if submitted_feedback == False:
            form = visitor_First_FollowupForm(request.POST)
        else:
            form = visitor_First_FollowupForm(request.POST, instance=submitted_feedback)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.followedup_up_by = request.user
            instance.visitor = visit_details.objects.get(id=pk)
            instance.save()
            return redirect('visitor_followup')
    else:
        if submitted_feedback == False:
            form = visitor_First_FollowupForm()
        else:
            form = visitor_First_FollowupForm(instance=submitted_feedback)
    

    context = { 
        'followup_visitor': followup_visitor,
        'form': form,
    }
    return render(request, 'visitors/visitor_feedback.html', context)

@login_required
def visitor_feedback_call(request):
    visitor = request.GET.get('myVal')
    try:
        submitted_feedback = visitor_followup_call.objects.get(visitor=visitor)
    except:
        submitted_feedback = False
    if request.method=='POST':
        submitted_feedback = request.POST.get('submitted_feedback')
        visitor = request.POST.get('visitor')
        if submitted_feedback == '':
            form = visitor_Followup_call_Form(request.POST)
        else:
            submitted_feedback = visitor_followup_call.objects.get(id=submitted_feedback)
            form = visitor_Followup_call_Form(request.POST, instance=submitted_feedback)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.followedup_up_by = request.user
            instance.visitor = visit_details.objects.get(id=visitor)
            instance.save()
            return redirect('visitor_followup')
    else:
        if submitted_feedback == False:
            form = visitor_Followup_call_Form()
        else:
            form = visitor_Followup_call_Form(instance=submitted_feedback)

    context = {
        'form': form,
        'visitor': visitor,
        'submitted_feedback': submitted_feedback,
    }
    return render(request, 'visitors/visitor_feedback_call.html', context)

@login_required()
def visitor_referral_finalize_view(request):
    visitor = request.GET.get('myVal')
    try:
        submitted_feedback = visitor_referral_finalize.objects.get(visitor=visitor)
    except:
        submitted_feedback = False
    if request.method=='POST':
        visitor = request.POST.get('visitor')
        submitted_feedback = request.POST.get('submitted_feedback')
        try:
           submitted_feedback = visitor_referral_finalize.objects.get(visitor=visitor)
           form = visitor_referral_finalize_form(request.POST, instance=submitted_feedback)
        except:
            form = visitor_referral_finalize_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.followedup_up_by = request.user
            instance.visitor = visit_details.objects.get(id=visitor)
            instance.save()
            group_referral = instance.refer_to_prayer_cell_id
            if group_referral  != None:
                group = session_attended_options.objects.get(id=instance.refer_to_prayer_cell_id)
                contact = User.objects.get(id=group.group_leader_id)
                visitor = People.objects.get(id=instance.visitor.visitor_id)
                contact
                contact.email
                send_mail("PLEASE FOLLOW UP RECENT VISITOR",
                f"""Dear {contact},
                    
Please could you contact {visitor.Name} a recent first time visitor who wants to join a prayer cell and invite them to join your prayer cell.
            
        {visitor.Name}\'s contact details are:
        Name: {visitor.Name}
        Surname: {visitor.Surname}
        Cell: {visitor.CellNumber}
        Email: {visitor.EmailAddress}

Kind Regards,

{request.user}
                    
                        """,
                "shodandevstesting@gmail.com",
                [contact.email],
                fail_silently=True,)  

            campus_referral = instance.refer_to_campus_id
            if campus_referral  != None:
                campus = campuses_details.objects.get(id=instance.refer_to_campus_id)
                contact = User.objects.get(id=campus.campus_leader_id)
                visitor = People.objects.get(id=instance.visitor.visitor_id)
                contact
                contact.email
                send_mail("PLEASE FOLLOW UP RECENT VISITOR",
                f"""Dear {contact},
                    
Please could you contact {visitor.Name} a recent first time visitor who lives in your area.
            
        {visitor.Name}\'s contact details are:
        Name: {visitor.Name}
        Surname: {visitor.Surname}
        Cell: {visitor.CellNumber}
        Email: {visitor.EmailAddress}

Kind Regards,

{request.user}
                    
                        """,
                "shodandevstesting@gmail.com",
                [contact.email],
                fail_silently=True,)        

        return redirect('visitor_followup')
    else:
        if submitted_feedback == False:
            form = visitor_referral_finalize_form()
        else:
            form = visitor_referral_finalize_form(instance=submitted_feedback)
    context = {
        'visitor': visitor,
        'form': form,
        'submitted_feedback': submitted_feedback,
    }
    return render(request, 'visitors/visitor_feedback_refer_finalize.html', context)



##### OLD VIEWS TO BE REMOVED ######
@login_required
def visitors(request):
    visitors = visit_date.objects.all()
    visitor_count = visit_date.objects.count()
    if request.method == 'POST':
        form_inline = visit_dateInlineFormset(request.POST)
        form = ConvertsForm(request.POST)
        if form.is_valid() and form_inline.is_valid():
          instance = form.save(commit=False)
          instance.createdBy = User.objects.get(pk=request.user.pk)
          instance.save()
          form_inline.instance = instance
          form_inline.save()
          visitor_name = form.cleaned_data.get('Name')
          messages.success(request, f'{visitor_name} has been added')
          return redirect('visitors')          
        else:
          if form.non_field_errors()[0] == 'Converts with this Name and Surname already exists.':
            visitor_name = form.cleaned_data.get('Name')
            visitor_surname = form.cleaned_data.get('Surname')
            visitor_id = Converts.objects.filter(Name=visitor_name, Surname=visitor_surname).values()
            visitor_id = visitor_id[0]
            id = visitor_id['id']
            visitor_status = visit_date.objects.filter(visitor=id).exists()
            if visitor_status == False:
                return redirect('visitors-update-existing', id)
            else:
                messages.warning(request, f'Could not save! {visitor_name} {visitor_surname} already has a visit date saved.')
                return redirect('visitors')
    
    else:
       form_inline = visit_dateInlineFormset()
       form = ConvertsForm()
            
    context = {
        'form': form,
        'form_inline': form_inline,
        'visitors': visitors,
        'visitor_count': visitor_count

    }
    return render(request, 'visitors/visitors.html', context)

@login_required
def visitors_update(request, pk):
    visitor = Converts.objects.get(id=pk)
    if request.method=='POST':
        form = ConvertsForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('visitors')
    else:
        form = ConvertsForm(instance=visitor)
    context= {
        'form': form
    }
    return render(request, 'visitors/visitor_update.html', context)

@login_required
def visitors_delete(request, pk):
    visitor = Converts.objects.get(id=pk)
    if request.method=='POST':
        visitor.delete()
        return redirect('visitors')
    context= {
        'visitor': visitor
    }
    return render(request, 'visitors/visitors_delete.html', context)

@login_required
def visitors_update_existing(request, pk):
    visitor = Converts.objects.get(id=pk)
    if request.method=='POST':
        form_inline = visit_dateInlineFormset(request.POST)
        form = visit_date_existingPersonForm(request.POST, instance=visitor)
        if form.is_valid() and form_inline.is_valid():
          instance = form.save(commit=False)
          instance.createdBy = User.objects.get(pk=request.user.pk)
          instance.save()
          form_inline.instance = instance
          form_inline.save()
          return redirect('visitors')
    else:
       form_inline = visit_dateInlineFormset()
       form = visit_date_existingPersonForm(instance=visitor)
    context= {
        'form': form,
        'form_inline': form_inline,
        'visitor': visitor

    }
    return render(request, 'visitors/visitor_update_existing.html', context)