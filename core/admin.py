from django.contrib import admin
from django.db import models
from django.forms import TextInput

from core.models import (
    MAX_TOKEN_NAME_LENGTH, MAX_TOKEN_VALUE_LENGTH, AccessToken
)


TEXT_INPUT_SIZE = max(MAX_TOKEN_NAME_LENGTH, MAX_TOKEN_VALUE_LENGTH)


class AccessTokenAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': TEXT_INPUT_SIZE})
        }
    }

    list_display = ('name', 'value')


admin.site.register(AccessToken, AccessTokenAdmin)
