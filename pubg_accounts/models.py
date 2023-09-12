from django.db import models
from user.models import *


class PubgAccount(models.Model):
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, default='PUBG MOBILE Global')
    status_type = models.CharField(max_length=50)
    price = models.CharField(max_length=55)
    level = models.CharField(max_length=10)
    rp = models.CharField(max_length=255)
    clothes = models.CharField(max_length=255)
    skins = models.CharField(max_length=255)
    titles = models.CharField(max_length=255)
    detail = models.TextField()

    def __str__(self):
        return f"{self.user_fk} - {self.type} - {self.price}"


class PubgAccountMedia(models.Model):
    account_fk = models.ForeignKey(PubgAccount, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pubg/', blank=True, null=True)

    def __str__(self):
        return f"{self.account_fk} - {self.file}"

