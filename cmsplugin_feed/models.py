from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext as _
from cms.models import CMSPlugin

class Feed(CMSPlugin):
    name = models.CharField(verbose_name=_('name'),max_length=255,
                            null=True, blank=True)
    feed_url = models.URLField(verbose_name=_('feed URL'),verify_exists=True)
    paginate_by = models.IntegerField(verbose_name="paginate by",
                                      null=True, blank=True,
                                      default=5)

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.id:
            cache.delete("feed_%s" %self.id)
        return super(Feed, self).save(*args, **kwargs)
