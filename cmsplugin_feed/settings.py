"""
This module enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

# Define the cache timeout in second for the feed
# default is 3600s (1 hour)
CMSPLUGIN_FEED_CACHE_TIMEOUT = getattr(settings,
                                       'CMSPLUGIN_FEED_CACHE_TIMEOUT', 3600)