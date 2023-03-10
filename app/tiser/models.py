import uuid

from accounts.models import TiserUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TiserStatus(models.TextChoices):
    CREATED = "created", _("Created")
    PAYED = "payed", _("Payed")
    CANCELLED = "cancelled", _("Cancelled")


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return f"{self.title}"


class Tiser(models.Model):
    title = models.CharField(_("Title"), max_length=64)
    desc = models.TextField(_("Description"), blank=True)
    author = models.ForeignKey(
        TiserUser,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name=_("Category"),
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        editable=False,
        choices=TiserStatus.choices,
        default=TiserStatus.CREATED
    )
    price = models.PositiveIntegerField(
        _("Price"),
        editable=False,
        default=0,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Tiser")
        verbose_name_plural = _("Tisers")

    def __str__(self):
        return f"{self.title} [{self.id}]"
