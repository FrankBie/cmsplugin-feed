import feedparser

from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, InvalidPage


from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_feed.models import Feed
from cmsplugin_feed.forms import FeedForm
from cmsplugin_feed.settings import CMSPLUGIN_FEED_CACHE_TIMEOUT

def get_cached_feed(instance):
    """
    get the feed from cache if it exists else fetch it.
    """
    if not cache.has_key("feed_%s" %instance.id):
        feed = feedparser.parse(instance.feed_url)
        cache.set("feed_%s" %instance.id, feed, CMSPLUGIN_FEED_CACHE_TIMEOUT)
    return cache.get("feed_%s" %instance.id)
    


class FeedPlugin(CMSPluginBase):
    model = Feed
    name = _('Feed')
    form = FeedForm
    render_template = 'cmsplugin_feed/feed.html'

    def render(self, context, instance, placeholder):
        feed = get_cached_feed(instance)
        #import pdb; pdb.set_trace()
        if instance.paginate_by:
            is_paginated =True
            request = context['request']
            feed_page_param = "feed_%s_page" %str(instance.id)

            feed_paginator = Paginator(feed["entries"], instance.paginate_by) 
            # Make sure page request is an int. If not, deliver first page.
            try:
                page = int(request.GET.get(feed_page_param, '1'))
            except ValueError:
                page = 1
            # If page request (9999) is out of range, deliver last page of results.
            try:
                entries = feed_paginator.page(page)
            except (EmptyPage, InvalidPage):
                entries = feed_paginator.page(paginator.num_pages)
        else:
            is_paginated =False
            entries = feed["entries"]
                    
        context.update({
            'instance': instance,
            'feed_entries': entries,
            'is_paginated' : is_paginated,
            'placeholder': placeholder,
            })
        return context

plugin_pool.register_plugin(FeedPlugin)
