from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Idea(models.Model):
    PUBLIC = 1
    PROTECTED = 2
    PRIVATED = 3
    STATUS = (
        (PUBLIC, _('The idea is public and available by someone')),
        (PROTECTED, _('The idea is protected and available by followers')),
        (PRIVATED, _('The idea is privated and not available')),
    )
    idea = models.CharField(max_length=254, null=False, blank=False)
    user = models.ForeignKey(
        CustomUser,
        related_name="author",
        on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=PUBLIC
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.idea} ({self.status})"
