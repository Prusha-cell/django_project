# tasks/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def notify_owner_on_status_change(sender, instance, **kwargs):
    if not instance.pk:
        # Новая задача — ничего не отправляем
        return

    old_instance = Task.objects.get(pk=instance.pk)

    # Проверяем, изменился ли статус
    if old_instance.status != instance.status:
        # не отправлять уведомление, если статус повторяется (напр., несколько раз подряд 'done')
        if old_instance.status == 'done' and instance.status == 'done':
            return

        # Если у задачи есть владелец и у него есть email
        if instance.owner and instance.owner.email:
            send_mail(
                subject='Статус вашей задачи обновлён',
                message=f"Ваша задача «{instance.title}» изменила статус с «{old_instance.status}» на «{instance.status}».",
                from_email=None,
                recipient_list=[instance.owner.email],
                fail_silently=False,
            )
