from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from functools import wraps

from accounts.models import UserProfile


# 自定义登录装饰器，确保用户已登录
def login_required_json(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 401,
                'message': '用户未登录。',
                'data': {}
            }, status=200)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@csrf_exempt
@login_required_json
def update_user_info(request):
    user = request.user

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    old_password = request.POST.get('old_password')
    gender = request.POST.get('gender')
    birth_date = request.POST.get('birth_date')
    avatar = request.FILES.get('avatar')

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        if old_password and check_password(old_password, user.password):
            user.set_password(password)
            update_session_auth_hash(request, user)
        else:
            return JsonResponse({
                'status': 400,
                'message': '原始密码不正确。',
                'data': {}
            }, status=200)

    if gender is not None:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.gender = gender

    if birth_date:
        try:
            profile.birth_date = birth_date
        except ValueError:
            return JsonResponse({
                'status': 400,
                'message': '出生日期格式不正确。',
                'data': {}
            }, status=200)

    if avatar:
        profile.avatar = avatar

    user.save()
    profile.save()

    return JsonResponse({
        'status': 200,
        'message': '用户信息修改成功。',
        'data': {}
    }, status=200)


@csrf_exempt
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'status': 200,
            'message': '登录成功。',
            'data': {
                'username': user.username,
                'email': user.email
            }
        }, status=200)
    else:
        return JsonResponse({
            'status': 400,
            'message': '用户名或密码错误。',
            'data': {}
        }, status=200)


@csrf_exempt
def user_register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'status': 400,
            'message': '用户名已存在。',
            'data': {}
        }, status=200)

    if User.objects.filter(email=email).exists():
        return JsonResponse({
            'status': 400,
            'message': '邮箱已被其他用户使用。',
            'data': {}
        }, status=200)

    user = User(
        username=username,
        email=email,
        password=make_password(password)
    )
    user.save()

    return JsonResponse({
        'status': 200,
        'message': '注册成功。',
        'data': {}
    }, status=200)


@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated:
        request.session.flush()
        return JsonResponse({
            'status': 200,
            'message': '退出登录成功。',
            'data': {}
        }, status=200)
    else:
        return JsonResponse({
            'status': 401,
            'message': '用户未登录。',
            'data': {}
        }, status=200)


@csrf_exempt
def get_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 200,
            'message': '用户已登录。',
            'data': {
                'username': request.user.username,
                'email': request.user.email
            }
        })
    else:
        return JsonResponse({
            'status': 401,
            'message': '用户未登录。',
            'data': {}
        })


@csrf_exempt
@login_required_json
def get_user_info(request):
    user = request.user
    user_info = {
        'username': user.username,
        'email': user.email,
    }
    try:
        profile = UserProfile.objects.get(user=user)
        user_info['gender'] = profile.gender
        user_info['birth_date'] = profile.birth_date
        if profile.avatar:
            user_info['avatar'] = request.build_absolute_uri(profile.avatar.url)
        else:
            user_info['avatar'] = None
    except UserProfile.DoesNotExist:
        user_info['gender'] = None
        user_info['birth_date'] = None
        user_info['avatar'] = None
    return JsonResponse({
        'status': 200,
        'message': '用户信息获取成功。',
        'data': {
            'user_info': user_info
        }
    }, status=200)
