from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from . forms import * 
from .models import *

# Create your views here.


def teacher_registration(request):
    form = PersonalInfoForm()
    education_form = EducationInfoForm()
    training_form = TrainingInfoForm()
    experience_form = ExperienceInfoForm()
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES)
        education_form = EducationInfoForm(request.POST)
        training_form = TrainingInfoForm(request.POST)
        experience_form = ExperienceInfoForm(request.POST)
        
        if form.is_valid()  and education_form.is_valid() and training_form.is_valid()  and experience_form.is_valid():
            education_info = education_form.save()
            training_info = training_form.save()
            experience_info = experience_form.save()
            personal_info = form.save(commit=False)
            personal_info.education = education_info
            personal_info.training = training_info
            personal_info.experience = experience_info
            personal_info.save()
            return redirect('teacher-list')

    context = {
        'form': form,
        'education_form': education_form,
        'training_form': training_form,
        'experience_form': experience_form
    }
    return render(request, 'hod/teacher-registration.html', context)


def teacher_list(request):
    teacher = PersonalInfo.objects.filter(is_delete=False)
    context = {'teacher': teacher}
    return render(request, 'hod/teacher-list.html', context)

def teacher_profile(request, teacher_id):
    teacher = PersonalInfo.objects.get(id=teacher_id)
    context = {
        'teacher': teacher
    }
    return render(request, 'hod/teacher-profile.html', context)

def teacher_delete(request, teacher_id):
    teacher = PersonalInfo.objects.get(id=teacher_id)
    teacher.is_delete = True
    teacher.save()
    return redirect('teacher-list')

def teacher_edit(request, teacher_id):
    teacher = PersonalInfo.objects.get(id=teacher_id)
    form = PersonalInfoForm(instance=teacher)
    education_form = EducationInfoForm(instance=teacher.education)
    training_form = TrainingInfoForm(instance=teacher.training)
    experience_form = ExperienceInfoForm(instance=teacher.experience)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=teacher)
        education_form = EducationInfoForm(request.POST, instance=teacher.education)
        training_form = TrainingInfoForm(request.POST, instance=teacher.training)
        experience_form = ExperienceInfoForm(request.POST, instance=teacher.experience)
        if form.is_valid() and education_form.is_valid() and training_form.is_valid()  and experience_form.is_valid():
            education_info = education_form.save()
            training_info = training_form.save()
            experience_info = experience_form.save()
            personal_info = form.save(commit=False)
            personal_info.education = education_info
            personal_info.training = training_info
            personal_info.experience = experience_info
            personal_info.save()
            return redirect('teacher-list')
    context = {
        'form': form,
        'education_form': education_form,
        'training_form': training_form,
        'experience_form': experience_form
    }
    return render(request, 'hod/teacher-edit.html', context)


def add_designation(request):
    forms = AddDesignationForm()
    if request.method == 'POST':
        forms = AddDesignationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('designation')
    designation = Designation.objects.all()
    context = {'forms': forms, 'designation': designation}
    return render(request, 'hod/designation.html', context)