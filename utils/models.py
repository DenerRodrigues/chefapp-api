from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Indicates that the record is active. Instead of deleting the record, uncheck this.'),
    )
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)
    last_update = models.DateTimeField(verbose_name=_('last update'), blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            super(BaseModel, self).delete(using, keep_parents)
        else:
            self.is_active = False
            self.save()
