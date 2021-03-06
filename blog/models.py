# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


from autoslug.fields import AutoSlugField
from django_markdown.models import MarkdownField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from slugify import Slugify

slugify_lower = Slugify(to_lower=True)


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(_('Post title'), max_length=255)
    content = MarkdownField(_('Content'))
    published = models.BooleanField(_('Published status'), default=False)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(_('Banner image'), 
                               upload_to='post_banner_images',
                               null=True,
                               blank=True)
    large_thumbnail = ImageSpecField(source='banner',
                                     processors=[ResizeToFill(600, 600)],
                                     format='JPEG',
                                     options={'quality': 80})
    thumbnail = ImageSpecField(source='banner',
                               processors=[ResizeToFill(300, 300)],
                               format='JPEG',
                               options={'quality': 80})
    slug = AutoSlugField(unique=True, 
                         populate_from='title')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
