from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Following(models.Model):
    PENDING = 1
    APPROVED = 2
    DENIED = 3
    STATUS = (
        (PENDING, _('The follow request is pending approval or deny')),
        (APPROVED, _('The follow request is approved')),
        (DENIED, _('The follow request is deny')),
    )
    followed = models.ForeignKey(
        CustomUser,
        related_name="followed",
        on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        CustomUser,
        related_name="follower",
        on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=PENDING
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")
        constraints = [
            models.CheckConstraint(
                check=~Q(follower__exact=F('followed')),
                name='you_cannot_follow_yourself'
            )
        ]
        ordering = ["-created"]

    def __str__(self):
        return(
            f"REQUEST FROM {self.follower.username} TO FOLLOW "
            f"{self.followed.username} IN STATUS {self.status}"
        )
