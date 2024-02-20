from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from school.models import *
# Create your views here.

def video_chat(request):
    return render(request, 'chatroom/counselling.html', {'name':request.user.name})


def video_chat_students(request):
    return render(request, 'chatroom/counselling_student.html')

@never_cache
@login_required(login_url='login_page')
def call(request):
    context= {
        'name':request.user.name
    }
    return render(request, 'chatroom/counselling_chatroom.html', context)


@never_cache
@login_required(login_url='login_page')
def join_room(request):

    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/c/call/?roomID=" + roomID)
    context= {
        'name':request.user.name
    }
    return render(request, 'chatroom/join_room.html', context)