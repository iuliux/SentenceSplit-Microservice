from __future__ import unicode_literals

import random
import re
import string

from django.core.validators import RegexValidator
from django.db import models


MIN_TOKEN_NAME_LENGTH = 1
MAX_TOKEN_NAME_LENGTH = 50


MIN_TOKEN_VALUE_LENGTH = 50
MAX_TOKEN_VALUE_LENGTH = 100


TOKEN_NAME_VALIDATOR = RegexValidator(
    regex=re.compile(r'^[\w-]{%d,%d}$' %
                     (MIN_TOKEN_NAME_LENGTH, MAX_TOKEN_NAME_LENGTH)),
    message='A token name must be a string of a size between %d and %d '
            'characters long and must consist of only alphanumeric '
            'characters, underscores and hyphens' %
            (MIN_TOKEN_NAME_LENGTH, MAX_TOKEN_NAME_LENGTH)
)


TOKEN_VALUE_VALIDATOR = RegexValidator(
    regex=re.compile(r'^[a-zA-Z0-9]{%d,%d}$' %
                     (MIN_TOKEN_VALUE_LENGTH, MAX_TOKEN_VALUE_LENGTH)),
    message='A token value must be an alphanumeric string of a size between '
            '%d and %d characters long' %
            (MIN_TOKEN_VALUE_LENGTH, MAX_TOKEN_VALUE_LENGTH)
)


ALPHANUMERIC_CHARSET = (
    string.ascii_lowercase + string.ascii_uppercase + string.digits
)


def generate_token():
    """ Generates random valid values for access tokens. """
    length = random.randint(MIN_TOKEN_VALUE_LENGTH, MAX_TOKEN_VALUE_LENGTH)
    return ''.join(random.choice(ALPHANUMERIC_CHARSET) for _ in range(length))


class AccessToken(models.Model):

    # Unique human-readable name for token (required for distinguishing tokens)
    name = models.CharField('Name', max_length=MAX_TOKEN_NAME_LENGTH,
                            default='', unique=True,
                            validators=[TOKEN_NAME_VALIDATOR])

    # Actual token value (will be generated automatically, if is omitted)
    value = models.CharField('Value', max_length=MAX_TOKEN_VALUE_LENGTH,
                             default=generate_token, db_index=True,
                             validators=[TOKEN_VALUE_VALIDATOR])

    def save(self, *args, **kwargs):
        # Validate name and value before making actual query to db
        TOKEN_NAME_VALIDATOR(self.name)
        TOKEN_VALUE_VALIDATOR(self.value)
        # If no ValidationError was raised, then try to save token to db
        super(AccessToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.value
