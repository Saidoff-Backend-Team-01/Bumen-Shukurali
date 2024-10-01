# from .validators import file_validator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", _("image")
        VIDEO = "video", _("video")
        AUDIO = "audio", _("audio")
        FILE = "file", _("file")
        MUSIX = "music", _("music")

    type = models.CharField(_("type"), max_length=50, choices=MediaType.choices)
    file = models.FileField(
        _("file"),
        upload_to="media_files/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["png", "jpg", "jpeg", "gif", "mp4", "mp3"]
            )
        ],
    )

    def clean(self):
        if self.type not in self.MediaType.values:
            raise ValidationError(_("Invalid File Type"))
        elif self.type == self.MediaType.IMAGE:
            if self.file.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
                raise ValidationError(_("Invalid Image File"))
            
    
    def __str__(self) -> str:
        return str(self.file)

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Media")

    
