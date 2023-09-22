from django.db import models
from user.models import *


class PubgAccount(models.Model):
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, default='PUBG MOBILE Global')
    status_type = models.CharField(max_length=50)   # "tekshiruvda", "sotuvda", "sotildi", "bekor_qilindi"
    price = models.CharField(max_length=55)
    level = models.CharField(max_length=10)
    rp = models.CharField(max_length=255)
    clothes = models.CharField(max_length=255)
    skins = models.CharField(max_length=255)
    titles = models.CharField(max_length=255)
    detail = models.TextField()
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user_fk} - {self.type} - {self.price}"


class PubgAccountMedia(models.Model):
    account_fk = models.ForeignKey(PubgAccount, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pubg/', blank=True, null=True)

    def __str__(self):
        return f"{self.account_fk} - {self.file}"


class PubgAccountOrder(models.Model):
    account_fk = models.ForeignKey(PubgAccount, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    additional_phone = models.CharField(max_length=9)
    order_status = models.CharField(max_length=20)  # "jarayonda", "tugallandi" "bekor_qilindi"
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.account_fk} - {self.user_fk} - {self.date}"


class PubgAccountHistory(models.Model):
    account_fk = models.ForeignKey(PubgAccount, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sold_price = models.PositiveIntegerField()
    price_paid_to_us = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.account_fk} - {self.user_fk} - {self.sold_price}"
