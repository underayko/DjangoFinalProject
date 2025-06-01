import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile_with_qr(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        
        # Generate QR code using username or ID
        qr = qrcode.make(f"{instance.username}")
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f"{instance.username}_qr.png"
        profile.qr_code.save(file_name, File(buffer), save=True)
