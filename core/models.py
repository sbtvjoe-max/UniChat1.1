from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_pin = models.CharField(max_length=4, blank=True, null=True)
    deadman_pin = models.CharField(max_length=4, blank=True, null=True)
    is_biometric_enabled = models.BooleanField(default=False)
    last_wipe_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Channel(models.Model):
    PLATFORM_CHOICES = [
        ('whatsapp', 'WhatsApp Business'),
        ('messenger', 'Facebook Messenger'),
        ('instagram', 'Instagram Messages'),
        ('sms', 'SMS (Twilio)'),
        ('tiktok', 'TikTok Messages'),
    ]
    
    name = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    is_active = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

class Conversation(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='conversations')
    external_id = models.CharField(max_length=255) # ID from the platform
    participant_name = models.CharField(max_length=255)
    last_message_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.participant_name} ({self.channel.get_name_display()})"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    is_from_me = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'Me' if self.is_from_me else self.conversation.participant_name}: {self.body[:50]}"