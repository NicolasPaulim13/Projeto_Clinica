from django.db import models
from django.utils.timezone import now

class PasswordRecovery(models.Model):
    email = models.EmailField()
    recovery_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f'{self.email} - {self.recovery_code}'
