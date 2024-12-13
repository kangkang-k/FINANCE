from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('bank', '银行账户'),
        ('wallet', '电子钱包'),
        ('other', '其他'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='other')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_frozen = models.BooleanField(default=False)  # 新增字段：是否冻结
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} ({self.get_account_type_display()}) - {'冻结' if self.is_frozen else '正常'}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', '收入'),
        ('expense', '支出'),
    )
    CATEGORIES = (
        ('salary', '工资'),
        ('shopping', '购物'),
        ('dining', '餐饮'),
        ('rent', '房租'),
        ('commute', '通勤'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, null=True, blank=True)  # 固定分类

    def __str__(self):
        return f"{self.account.account_name} - {self.get_transaction_type_display()} - {self.amount} - {self.get_category_display()}"
