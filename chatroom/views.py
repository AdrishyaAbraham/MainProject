from django.shortcuts import render

# Create your views here.

def video_chat(request):
    context= {}
    return render(request, 'chatroom/counselling.html', context=context)