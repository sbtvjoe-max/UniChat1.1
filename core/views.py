import os
import platform
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Channel, Conversation, Message

def home(request):
    """UniChat Dashboard - The Central Hub"""
    # Ensure default channels exist
    for code, name in Channel.PLATFORM_CHOICES:
        Channel.objects.get_or_create(name=code)
    
    active_channels = Channel.objects.filter(is_active=True)
    recent_conversations = Conversation.objects.filter(channel__in=active_channels).order_by('-last_message_at')[:5]
    
    context = {
        "active_channels": active_channels,
        "recent_conversations": recent_conversations,
        "total_active": active_channels.count(),
        "all_channels": Channel.objects.all(),
    }
    return render(request, "core/index.html", context)

def integrations(request):
    """Manage connected messaging services"""
    if request.method == "POST":
        channel_id = request.POST.get("channel_id")
        action = request.POST.get("action")
        
        try:
            channel = Channel.objects.get(id=channel_id)
            if action == "enable":
                channel.is_active = True
                messages.success(request, f"{channel.get_name_display()} enabled successfully.")
            else:
                channel.is_active = False
                messages.info(request, f"{channel.get_name_display()} disabled.")
            channel.save()
        except Channel.DoesNotExist:
            messages.error(request, "Channel not found.")
        
        return redirect("integrations")

    channels = Channel.objects.all()
    return render(request, "core/integrations.html", {"channels": channels})

def wipe_data(request):
    """Deadman Switch implementation - wipes sensitive data"""
    if request.method == "POST":
        # In a real app, verify the Deadman PIN here
        Message.objects.all().delete()
        Conversation.objects.all().delete()
        # Mark as wiped in profile
        if request.user.is_authenticated:
            request.user.profile.last_wipe_at = timezone.now()
            request.user.profile.save()
        
        messages.warning(request, "SECURITY PROTOCOL ACTIVATED: All local data has been wiped.")
        return redirect("home")
    return redirect("home")