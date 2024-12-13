from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', get_user_accounts, name='get_user_accounts'),
    path('add_account/', add_account, name='add_account'),
    path('delete_account/', delete_account, name='delete_account'),
    path('update_account/', update_account, name='update_account'),
    path('freeze_account/', freeze_account, name='freeze_account'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('delete_transaction/', delete_transaction, name='delete_transaction'),
    path('get_account_transactions/', get_account_transactions, name='get_account_transactions'),

]
