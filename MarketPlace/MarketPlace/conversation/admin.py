from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ConversationMessage)
admin.site.register(Conversation)