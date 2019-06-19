from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import User
# Create your models here.

import os
import logging
from django.conf import settings

lgr = logging.getLogger(__name__)


def file_cleanup(sender, instance, using, **kwargs):
    settings_path = instance.session_file_path()

    if os.path.exists(settings_path):
        os.remove(settings_path)


from django.db.models.signals import post_delete


class SampleModel(models.Model):

    class Meta:
        managed = False

# post_delete.connect(file_cleanup, sender=SalesNavigatorAccount)

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    product_page = models.URLField(help_text='Solar light Product Page')

    freelancer = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)
