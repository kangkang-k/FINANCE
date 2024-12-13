from django.db import models
from django.contrib.auth.models import User
from accounts_manager.models import Transaction


class Budget(models.Model):
    CATEGORY_CHOICES = Transaction.CATEGORIES

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} - {self.get_category_display()} - {self.amount}元"
