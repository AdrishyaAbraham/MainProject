
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Student,Teacher,Resource,Class,Section,GuideTeacher,Session,ClassRegistration
from .forms import StudentForm,TeacherForm,ResourceForm,ClassForm,SectionForm,GuideTeacherForm,SessionForm,ClassRegistrationForm



def index(request):
    return render(request,'adminpanel/indexdashboard.html')

# def index1(request):
#     return render(request,'adminpanel/index.html',{
#        'students': Student.objects.all()
#     })

# def index2(request):
#     return render(request,'adminpanel/index_teacher.html',{
#        'teachers': Teacher.objects.all()
#     })

# def base(request):
#     return render(request,'adminpanel/base.html')

# def view_student(request, id):
#   return HttpResponseRedirect(reverse('index1'))


# def add(request):
#   if request.method == 'POST':
#     form = StudentForm(request.POST)
#     if form.is_valid():
#       new_student_number = form.cleaned_data['student_number']
#       new_name = form.cleaned_data['name']
#       new_email = form.cleaned_data['email']
      
#       new_student = Student(
#         student_number=new_student_number,
#         name=new_name,
#         email=new_email,
       
#       )
#       new_student.save()
#       return render(request, 'adminpanel/add.html', {
#         'form': StudentForm(),
#         'success': True
#       })
#   else:
#     form = StudentForm()
#   return render(request, 'adminpanel/add.html', {
#     'form': StudentForm()
#   })


# def edit(request, id):
#   if request.method == 'POST':
#     student = Student.objects.get(pk=id)
#     form = StudentForm(request.POST, instance=student)
#     if form.is_valid():
#       form.save()
#       return render(request, 'adminpanel/edit.html', {
#         'form': form,
#         'success': True
#       })
#   else:
#     student = Student.objects.get(pk=id)
#     form = StudentForm(instance=student)
#   return render(request, 'adminpanel/edit.html', {
#     'form': form
#   })


# def delete(request, id):
#   if request.method == 'POST':
#     student = Student.objects.get(pk=id)
#     student.delete()
#   return HttpResponseRedirect(reverse('index1'))

# #teacher----adminpage---


# def base_teacher(request):
#     return render(request,'adminpanel/base_teacher.html')

# def view_teacher(request,id):
#     return HttpResponseRedirect(reverse('index2'))

# def add_teacher(request):
#   if request.method == 'POST':
#     form = TeacherForm(request.POST)
#     if form.is_valid():
#       new_teacher_number = form.cleaned_data['teacher_number']
#       new_name = form.cleaned_data['name']
#       new_email = form.cleaned_data['email']
      
#       new_teacher = Teacher(
#         teacher_number=new_teacher_number,
#         name=new_name,
#         email=new_email,
       
#       )
#       new_teacher.save()
#       return render(request, 'adminpanel/add_teacher.html', {
#         'form': TeacherForm(),
#         'success': True
#       })
#   else:
#     form = TeacherForm()
#   return render(request, 'adminpanel/add_teacher.html', {
#     'form': TeacherForm()
#   })


# def edit_teacher(request, id):
#   if request.method == 'POST':
#     teacher = Teacher.objects.get(pk=id)
#     form = TeacherForm(request.POST, instance=teacher)
#     if form.is_valid():
#       form.save()
#       return render(request, 'adminpanel/edit_teacher.html', {
#         'form': form,
#         'success': True
#       })
#   else:
#     teacher = Teacher.objects.get(pk=id)
#     form = TeacherForm(instance=teacher)
#   return render(request, 'adminpanel/edit_teacher.html', {
#     'form': form
#   })


# def delete_teacher(request, id):
  # if request.method == 'POST':
  #   teacher = Teacher.objects.get(pk=id)
  #   teacher.delete()
  # return HttpResponseRedirect(reverse('index2'))

#----------------HOD-dashboard-----------#

def hoddashboard(request):
   return render(request,'hod/hoddashboard.html')

def index1(request):
    return render(request,'hod/index.html',{
       'students': Student.objects.all()
    })

def index2(request):
    return render(request,'hod/index_teacher.html',{
       'teachers': Teacher.objects.all()
    })

def base(request):
    return render(request,'hod/base.html')

def view_student(request, id):
  return HttpResponseRedirect(reverse('index1'))


def add(request):
  if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
      new_student_number = form.cleaned_data['student_number']
      new_name = form.cleaned_data['name']
      new_email = form.cleaned_data['email']
      new_address=form.cleaned_data['address']
      new_phone_number=form.cleaned_data['phone_number']
      new_gender=form.cleaned_data['gender']
      new_dob=form.cleaned_data['dob']
      new_doj=form.cleaned_data['doj']
      new_fathername=form.cleaned_data['fathername']
      new_father_contact=form.cleaned_data['father_contact']
      new_mothername=form.cleaned_data['mothername']
      new_mother_contact=form.cleaned_data['mother_contact']


      
      new_student = Student(
        student_number=new_student_number,
        name=new_name,
        email=new_email,
        address=new_address,
        phone_number=new_phone_number,
        gener=new_gender,
        dob=new_dob,
        doj=new_doj,
        fathername=new_fathername,
        father_contact=new_father_contact,
        mothername=new_mothername,
        mother_contact=new_mother_contact,

       
      )
      new_student.save()
      return render(request, 'hod/add.html', {
        'form': StudentForm(),
        'success': True
      })
    else:
       print(form.errors)
  else:
     
     form = StudentForm()
  return render(request, 'hod/add.html', {
    'form': StudentForm()
  })


def edit(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return render(request, 'hod/edit.html', {
        'form': form,
        'success': True
      })
  else:
    student = Student.objects.get(pk=id)
    form = StudentForm(instance=student)
  return render(request, 'hod/edit.html', {
    'form': form
  })


def delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    student.delete()
  return HttpResponseRedirect(reverse('index1'))

def base_teacher(request):
    return render(request,'hod/base_teacher.html')

def view_teacher():
    return HttpResponseRedirect(reverse('index2'))

def add_teacher(request):
  if request.method == 'POST':
    form = TeacherForm(request.POST)
    if form.is_valid():
      new_teacher_number = form.cleaned_data['teacher_number']
      new_name = form.cleaned_data['name']
      new_email = form.cleaned_data['email']
      new_address = form.cleaned_data['address']
      new_phone_number = form.cleaned_data['phone_number']
      new_gender = form.cleaned_data['gender']
      new_dob = form.cleaned_data['dob']
      new_doj = form.cleaned_data['doj']

      
      new_teacher = Teacher(
        teacher_number=new_teacher_number,
        name=new_name,
        email=new_email,
        address=new_address,
        phone_number=new_phone_number,
        gender=new_gender,
        dob=new_dob,
        doj=new_doj,

       
      )
      new_teacher.save()
      return render(request, 'hod/add_teacher.html', {
        'form': TeacherForm(),
        'success': True
      })
  else:
    form = TeacherForm()
  return render(request, 'hod/add_teacher.html', {
    'form': TeacherForm()
  })


def edit_teacher(request, id):
  if request.method == 'POST':
    teacher = Teacher.objects.get(pk=id)
    form = TeacherForm(request.POST, instance=teacher)
    if form.is_valid():
      form.save()
      return render(request, 'hod/edit_teacher.html', {
        'form': form,
        'success': True
      })
  else:
    teacher = Teacher.objects.get(pk=id)
    form = TeacherForm(instance=teacher)
  return render(request, 'hod/edit_teacher.html', {
    'form': form
  })


def delete_teacher(request, id):
  if request.method == 'POST':
    teacher = Teacher.objects.get(pk=id)
    teacher.delete()
  return HttpResponseRedirect(reverse('index2'))

def add_class(request):
    forms = ClassForm()  # Initialize the form here
    class_obj = Class.objects.all()  # You can fetch all classes outside the POST block as well

    if request.method == 'POST':
        forms = ClassForm(request.POST)  # Re-bind the form with POST data
        if forms.is_valid():
            new_name = forms.cleaned_data['name']
            new_display_name = forms.cleaned_data['display_name']

            new_class = Class(
                name=new_name,
                display_name=new_display_name
            )
            new_class.save()
            return redirect('add_class')

    context = {
        'forms': forms,  # No need for parentheses here
        'class_obj': class_obj,
        'success': True if request.method == 'POST' and forms.is_valid() else False
    }

    return render(request, 'hod/create_class.html', context)


def create_section(request):
    forms = SectionForm()
    if request.method == 'POST':
        forms = SectionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-section')
    section = Section.objects.all()
    context = {
        'forms': forms,
        'section': section
    }
    return render(request, 'hod/create_classsection.html', context)  

def create_guide_teacher(request):
    forms = GuideTeacherForm()
    if request.method == 'POST':
        forms = GuideTeacherForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('guide-teacher')
    guide_teacher = GuideTeacher.objects.all()
    context = {
        'forms': forms,
        'guide_teacher': guide_teacher
    }
    return render(request, 'hod/create_guideteacher.html', context)    

def create_session(request):
    forms = SessionForm()
    if request.method == 'POST':
        forms = SessionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-session')
    session = Session.objects.all()
    context = {
        'forms': forms,
        'session': session
    }
    return render(request, 'hod/create_session.html', context)

def class_registration(request):
    forms = ClassRegistrationForm()
    if request.method == 'POST':
        forms = ClassRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('class-list')
    context = {'forms': forms}
    return render(request, 'hod/class_registration.html', context)

def class_list(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'hod/class_list.html', context)


#------------teacher dashborad---#
def teacherdashboard(request):
   return render(request,'teacher/teacher_dashboard.html')

def attendance(request):
   return render(request,'teacher/attendance.html')

def index_resource(request):
   return render(request,'teacher/index_resource.html',{
      'resources':Resource.objects.all()
   })

def add_resource(request):
  if request.method == 'POST':
    form = ResourceForm(request.POST)
    if form.is_valid():
      new_resource_id = form.cleaned_data['resource_id']
      new_resource_title = form.cleaned_data['resource_title']
      new_resource_file = form.cleaned_data['resource_file']
      new_file_type = form.cleaned_data['file_type']
      new_description = form.cleaned_data['description']
      new_uploaded_date = form.cleaned_data['uploaded_date']

      new_resource = Resource(
        resource_id=new_resource_id,
        resource_title=new_resource_title,
        resource_file=new_resource_file,
        file_type=new_file_type,
        description=new_description,
        uploaded_date=new_uploaded_date,
      )
      new_resource.save()
      return render(request, 'teacher/add_resource.html', {
        'form': ResourceForm(),
        'success': True
      })
  else:
    form = ResourceForm()
  return render(request, 'teacher/add_resource.html', {
    'form': ResourceForm()
  })


def view_resource():
 return HttpResponseRedirect(reverse('index_resource'))

def edit_resource(request):
    if request.method == 'POST':
      resource = Resource.objects.get(pk=id)
      form = ResourceForm(request.POST, instance=resource)
      if form.is_valid():
        form.save()
      return render(request, 'teacher/edit_resource.html', {
        'form': form,
        'success': True
      })
    else:
      resource = Resource.objects.get(pk=id)
      form = ResourceForm(instance=resource)
    return render(request, 'teacher/edit_resource.html', {
    'form': form
  })



def delete_resource(request):
    if request.method == 'POST':
     resource = Resource.objects.get(pk=id)
     resource.delete()
    return HttpResponseRedirect(reverse('index_resource'))


def uploadresource(request):
   return render(request,'teacher/resource.html')




#--------------student dashboard-------#
def studentdashboard(request):
   return render(request,'student/student_dashboard.html')

def downloadresource(request):
   return render(request,'student/resources.html')

def editprofile(request):
   return render(request,'student/edit-profile.html')

#--------login page and registration-----#
def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Invalid Login")
            return render(request, 'login/index.html')    

    else:
        return render(request, 'login/index.html')    

def register_page(request):
    if request.method == "POST":
        name = request.POST ['name']
        username = request.POST ['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        phone=request.POST['phone']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                # messages.info(request, 'Username already exists')
                # return redirect('register')
                return render(request, 'login/register.html', {'username_exists': True})
                # if User.objects.filter(userban).exists():
            #     messages.info(request, 'Email already exists') 
            #     return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('register')
    else:
        return render(request, 'login/register.html')
    
def logout_user(request):
    print('Logged Out')
    logout(request)
    return redirect('/')