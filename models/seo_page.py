from wagtail.core.models import Page
from django.db import models
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel, ObjectList)
from django.core.validators import MaxValueValidator, MinValueValidator


class SeoPage(Page):
    """ SeoPage contain the SEO pannel to add to your pages when you want SEO checks"""
    keyword = models.CharField(max_length=30, blank=True)
    delay_keyword = models.IntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])

    seo_panels = [
        MultiFieldPanel([
            FieldPanel('keyword'),
            FieldPanel('delay_keyword'),
        ]),
    ]

    seo_object_list = ObjectList(seo_panels, heading='SEO')

    class Meta:
        abstract=True