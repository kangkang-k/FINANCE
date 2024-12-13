import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal


@csrf_exempt
@login_required
def get_user_accounts(request):
    user = request.user
    accounts = Account.objects.filter(user=user)

    account_data = [
        {
            'id': account.id,
            'name': account.account_name,
            'type': account.get_account_type_display(),
            'balance': str(account.balance),
            'created_at': account.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': account.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for account in accounts
    ]

    return JsonResponse({
        'status': 200,
        'message': '账户信息获取成功。',
        'data': {
            'accounts': account_data
        }
    }, status=200)


@csrf_exempt
@login_required
def add_account(request):
    """
    添加一个新的账户。
    请求参数：
    - name: 账户名称
    - account_type: 账户类型 (bank, wallet, other)
    - balance: 初始余额
    """
    user = request.user
    account_name = request.POST.get('account_name')
    account_type = request.POST.get('account_type')
    balance = request.POST.get('balance')

    # 参数验证
    if not account_name:
        return JsonResponse({
            'status': 400,
            'message': '账户名称不能为空。',
            'data': {}
        }, status=200)

    if account_type not in ['bank', 'wallet', 'other']:
        return JsonResponse({
            'status': 400,
            'message': '账户类型无效((bank, wallet, other))。',
            'data': {}
        }, status=200)

    try:
        balance = Decimal(balance)
    except ValueError:
        return JsonResponse({
            'status': 400,
            'message': '余额必须是有效的数字。',
            'data': {}
        }, status=200)

    account = Account.objects.create(
        user=user,
        account_name=account_name,
        account_type=account_type,
        balance=balance
    )

    return JsonResponse({
        'status': 200,
        'message': '账户创建成功。',
        'data': {
            'id': account.id,
            'name': account.account_name,
            'type': account.get_account_type_display(),
            'balance': str(account.balance),
            'created_at': account.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': account.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
    }, status=200)


@csrf_exempt
@login_required
def delete_account(request):
    account_id = request.POST.get('account_id')
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        account.delete()

        return JsonResponse({
            'status': 200,
            'message': '账户删除成功。',
            'data': {}
        }, status=200)

    except Account.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': '账户不存在或不属于当前用户。',
            'data': {}
        }, status=200)


@csrf_exempt
@login_required
def update_account(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({
            "status": 400,
            "message": "请求格式错误，请提交 JSON 格式数据。",
            "data": {}
        }, status=200)

    account_id = body.get("account_id")
    account_name = body.get("account_name")
    account_type = body.get("account_type")
    balance = body.get("balance")

    if not account_id:
        return JsonResponse({
            "status": 400,
            "message": "账户 ID 不能为空。",
            "data": {}
        }, status=200)

    try:
        account = Account.objects.get(id=account_id, user=request.user)
    except Account.DoesNotExist:
        return JsonResponse({
            "status": 404,
            "message": "账户不存在。",
            "data": {}
        }, status=200)

    valid_account_types = dict(Account.ACCOUNT_TYPES).keys()
    if account_type and account_type not in valid_account_types:
        return JsonResponse({
            "status": 400,
            "message": "账户类型不合法。",
            "data": {}
        }, status=200)
    if account_name:
        account.account_name = account_name
    if account_type:
        account.account_type = dict(Account.ACCOUNT_TYPES)[account_type]
    if balance is not None:
        try:
            account.balance = float(balance)
        except ValueError:
            return JsonResponse({
                "status": 400,
                "message": "余额格式错误，应为数字。",
                "data": {}
            }, status=200)

    account.save()

    return JsonResponse({
        "status": 200,
        "message": "账户信息更新成功。",
        "data": {
            "id": account.id,
            "name": account.account_name,
            "account_type": account.account_type,
            "balance": account.balance
        }
    }, status=200)


@csrf_exempt
@login_required
def freeze_account(request):
    account_id = request.POST.get('account_id')
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        account.is_frozen = not account.is_frozen
        account.save()
        status = "冻结" if account.is_frozen else "解冻"
        return JsonResponse({"message": f"账户已{status}", "is_frozen": account.is_frozen, "status": 200, "data": {}},
                            status=200)
    except Account.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': '账户不存在或不属于当前用户。',
            'data': {}
        }, status=200)


from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction


@csrf_exempt
@login_required
def add_transaction(request):
    account_id = request.POST.get('account_id')
    account = Account.objects.get(id=account_id, user=request.user)

    amount = request.POST.get('amount')
    transaction_type = request.POST.get('transaction_type')
    description = request.POST.get('description', '')
    category = request.POST.get('category')
    amount = Decimal(amount)

    if transaction_type == 'income':
        account.balance += amount
    elif transaction_type == 'expense':
        if account.balance < amount:
            return JsonResponse({
                'status': 400,
                'message': '账户余额不足。',
                'data': {}
            }, status=200)
        account.balance -= amount

    transaction = Transaction.objects.create(
        account=account,
        amount=amount,
        transaction_type=transaction_type,
        description=description,
        category=category
    )

    account.save()

    return JsonResponse({
        'status': 200,
        'message': '交易记录添加成功。',
        'data': {
            'transaction_id': transaction.id,
            'amount': transaction.amount,
            'transaction_type': transaction.get_transaction_type_display(),
            'category': transaction.get_category_display(),
            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    }, status=200)


@csrf_exempt
@login_required
def delete_transaction(request):
    transaction_id = request.POST.get('transaction_id')
    try:
        # 获取交易记录
        transaction = Transaction.objects.get(id=transaction_id, account__user=request.user)
    except Transaction.DoesNotExist:
        return JsonResponse({
            'status': 400,
            'message': '交易记录不存在。',
            'data': {}
        }, status=200)

    account = transaction.account

    transaction.delete()

    account.save()

    return JsonResponse({
        'status': 200,
        'message': '交易记录删除成功。',
        'data': {}
    }, status=200)


@csrf_exempt
@login_required
def get_account_transactions(request):
    account_id = request.POST.get('account_id')
    try:
        account = Account.objects.get(id=account_id, user=request.user)
    except Account.DoesNotExist:
        return JsonResponse({
            'status': 400,
            'message': '账户不存在。',
            'data': {}
        }, status=200)

    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')

    transaction_data = [{
        'id': transaction.id,
        'amount': transaction.amount,
        'transaction_type': transaction.get_transaction_type_display(),
        'description': transaction.description,
        'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
    } for transaction in transactions]

    return JsonResponse({
        'status': 200,
        'message': '查询成功。',
        'data': transaction_data
    }, status=200)
