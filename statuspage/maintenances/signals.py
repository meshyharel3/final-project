from django.db.models.signals import post_save
from django.dispatch import receiver

from maintenances.models import Maintenance, MaintenanceUpdate
from subscribers.models import Subscriber
from utilities.utils import on_transaction_commit, get_mail_domain


@receiver(post_save, sender=Maintenance)
@on_transaction_commit
def send_notifications(sender, instance: Maintenance, **kwargs):
    is_new = kwargs.get('created', False)

    if is_new and instance.visibility:
        try:
            subscribers = Subscriber.objects.filter(incident_subscriptions=True)

            for subscriber in subscribers:
                if subscriber.incident_notifications_subscribed_only and len(instance.components.filter(subscribers__in=[subscriber])) == 0:
                    continue
                subscriber.send_mail(subject=f'Maintenance - {instance.title}', template='maintenances/created', context={
                    'maintenance': instance,
                    'components': instance.components.filter(visibility=True),
                }, headers={
                    'Message-ID': f'maintenance-{instance.id}-0@{get_mail_domain()}',
                })
        except:
            pass


@receiver(post_save, sender=MaintenanceUpdate)
@on_transaction_commit
def send_notifications(sender, instance: MaintenanceUpdate, **kwargs):
    is_new = kwargs.get('created', False)

    if is_new and instance.maintenance.visibility:
        try:
            subscribers = Subscriber.objects.filter(incident_subscriptions=True)
            message_id = f'maintenance-{instance.maintenance.id}-{instance.id}@{get_mail_domain()}'
            previous_message_ids = [
                f'maintenance-{instance.maintenance.id}-0@{get_mail_domain()}',
                *list(map(
                    lambda update: f'maintenance-{instance.maintenance.id}-{update.id}@{get_mail_domain()}',
                    instance.maintenance.updates.all()
                ))
            ]

            for subscriber in subscribers:
                if subscriber.incident_notifications_subscribed_only and len(instance.maintenance.components.filter(subscribers__in=[subscriber])) == 0:
                    continue
                subscriber.send_mail(subject=f'Maintenance - {instance.maintenance.title}', template='maintenanceupdates/created', context={
                    'maintenance': instance.maintenance,
                    'update': instance,
                    'components': instance.maintenance.components.filter(visibility=True),
                }, headers={
                    'Message-ID': message_id,
                    'References': ' '.join(previous_message_ids),
                })
        except:
            pass