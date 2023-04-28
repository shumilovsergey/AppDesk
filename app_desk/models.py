from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .const import TG_TOKEN, GROUP_ID
import requests



class Task(models.Model):
    title = models.CharField('название заявки', max_length=56)
    text = models.TextField('текст заявки')
    time_date = models.DateTimeField('время дата',default=timezone.now)
    status = models.BooleanField('выполнено', default=False)
    comment = models.TextField('комментарий', default='Комментариев нет')
    ###
    pc_ip = models.CharField('IP адрес', max_length=15)
    pc_name = models.CharField('имя компьютера', max_length=24, default='???')
    fio = models.CharField('ФИО пользователя', max_length=56, default='???')
    phone = models.CharField('Номер телефона', max_length=24, default='Отсутствует')
    dep = models.CharField('Отдел', max_length=24, default='Отсутствует')    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

class User(models.Model):
    pc_ip = models.CharField('IP адрес', max_length=15)
    pc_name = models.CharField('имя компьютера', max_length=24)
    fio = models.CharField('ФИО пользователя', max_length=56)
    phone = models.CharField('Номер телефона', max_length=24)
    dep = models.CharField('Отдел', max_length=24)
    admin = models.BooleanField('Право доступа')

    def __str__(self):
        return self.fio
    
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'



@receiver(post_save, sender=Task)
def new_task_pushup(sender, instance, created, **kwargs):
    if created:
        text = instance.text
        pc_ip = instance.pc_ip
        pc_name = instance.pc_name
        phone = instance.phone
        fio = instance.fio

        if fio == '???':
            tg_message = f"Пользователя нет в базе \n\n{text}\n\n{pc_ip}"
        else:
            tg_message = f"{fio} \n\n{text}\n\n{pc_name}\n{phone}"

        try:
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={
                "chat_id": GROUP_ID,
                "text": tg_message
            })
        except:
            print('lost connection with TELEGRAMM')   

        return
        