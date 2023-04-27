from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Task
from django.urls import reverse
from dotenv import load_dotenv
import os
import telebot
from telebot import types


load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")


bot = telebot.TeleBot(TG_TOKEN)



def task_list(request):
    call_back=[]
    if request.method == 'GET':
        tasklist = Task.objects.filter(status=False).order_by('-id')
    else:
        for q in request.POST:
            call_back.append(q)

        if call_back[1] == 'in_progres':
            tasklist = Task.objects.filter(status=False).order_by('-id')
        elif call_back[1] == 'done':
            tasklist = Task.objects.filter(status=True).order_by('-id')
            
    return render(request, 'app_desk/task_list.html', {'tasklist':tasklist})

def task_detail(request, task_id):
    try:
        task = Task.objects.get(id = task_id)
    except:
        raise Http404("Заявка не найдена!")
    return render(request, 'app_desk/task_detail.html', {'task':task})

def task_add(request):

    user_exist = False
    text = request.POST['text']
    words = text.split()
    title = (' '.join(words[:5]))
    pc_ip = request.META.get('REMOTE_ADDR')

    try:
        user = User.objects.get(pc_ip = pc_ip)
        user_exist = True
    except:
        user_exist = False

    if user_exist:
        pc_name = user.pc_name
        fio = user.fio
        phone = user.phone
        dep = user.dep
        Task.objects.create(title=title, text=text, pc_ip=pc_ip, pc_name=pc_name, fio=fio, phone=phone,dep=dep)
        tg_message = f"{fio} \n\n{text}\n\n{pc_name}\n{phone}"
    else:
        Task.objects.create(title=title, text=text, pc_ip=pc_ip)
        tg_message = f"Пользователя нет в базе \n\n{text}\n\n{pc_ip}"

    try:
        bot.send_message(chat_id=GROUP_ID, text=tg_message)
    except:
        print('lost connection with TELEGRAMM')
    
    return HttpResponseRedirect(reverse('app_desk:task_list'))

def status_update(request):
    task_id = int(request.POST['task_id'])
    task = Task.objects.get(id = task_id)        
    
    if task.status:
        task.status = False
    else:
        task.status = True
    task.save()
    
    return HttpResponseRedirect(reverse('app_desk:task_list'))
        