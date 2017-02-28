from django.contrib import admin
from django.db import models
from django.forms import TextInput

from .models import AccessToken, MAX_TOKEN_NAME_LENGTH, MAX_TOKEN_VALUE_LENGTH


TEXT_INPUT_SIZE = max(MAX_TOKEN_NAME_LENGTH, MAX_TOKEN_VALUE_LENGTH)


class AccessTokenAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': TEXT_INPUT_SIZE})
        }
    }

    list_display = ('name', 'value')


admin.site.register(AccessToken, AccessTokenAdmin)
