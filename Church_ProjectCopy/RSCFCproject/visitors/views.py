from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ConvertsForm, visit_dateInlineFormset, visitorFollowupForm, visit_date_existingPersonForm
from .models import visit_date
from SalvationFollowUps.models import Converts
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

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