from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import Media

from .managers import NewsManager


# Create your models here.
class News(models.Model):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    created_at = models.DateTimeField(_("create at"), auto_now_add=True)
    is_publish = models.BooleanField(_("is publish"), default=True)
    published = NewsManager()

    class Meta:
        verbose_name = _("news")
        verbose_name_plural = _("news")

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_images')
    image = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='news_images')

    class Meta:
        verbose_name = _("news image")
        verbose_name_plural = _("news images")