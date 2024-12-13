用户管理 API 技术文档
概述
该 API 提供了与用户管理相关的基本功能，包括用户注册、登录、登出、修改信息等操作。返回的 JSON 格式已经标准化，便于前端进行处理。

基本 API 结构
所有接口返回的 JSON 格式如下：
{
"status": int, // 状态码，200表示成功，其他表示错误
"message": "中文消息", // 错误或成功的提示消息
"data": {} // 返回的数据，成功时返回数据，失败时返回空对象
}

接口列表

1. 用户登录
   URL: /accounts/login/
   方法: POST
   请求参数:
   username (string): 用户名
   password (string): 密码
   成功响应:
   {
   "status": 200,
   "message": "登录成功。",
   "data": {
   "username": "example_user",
   "email": "user@example.com"
   }
   }
   失败响应:
   {
   "status": 400,
   "message": "用户名或密码错误。",
   "data": {}
   }
2. 用户注册
   URL: /accounts/register/
   方法: POST
   请求参数:
   username (string): 用户名
   password (string): 密码
   email (string): 邮箱地址
   成功响应:
   {
   "status": 200,
   "message": "注册成功。",
   "data": {}
   }
   失败响应:
   用户名已存在：
   {
   "status": 400,
   "message": "用户名已存在。",
   "data": {}
   }
   邮箱已被使用：
   {
   "status": 400,
   "message": "邮箱已被其他用户使用。",
   "data": {}
   }
3. 用户登出
   URL: /accounts/logout/
   方法: POST
   请求参数: 无
   成功响应:
   {
   "status": 200,
   "message": "退出登录成功。",
   "data": {}
   }
   失败响应:
   用户未登录：
   {
   "status": 401,
   "message": "用户未登录。",
   "data": {}
   }
4. 获取登录状态
   URL: /accounts/status/
   方法: GET
   请求参数: 无
   成功响应:
   {
   "status": 200,
   "message": "用户已登录。",
   "data": {
   "username": "example_user",
   "email": "user@example.com"
   }
   }
   失败响应:
   用户未登录：
   {
   "status": 401,
   "message": "用户未登录。",
   "data": {}
   }
5. 获取用户信息
   URL: /accounts/user-info/
   方法: GET
   请求参数: 无
   认证要求: 用户必须已登录
   成功响应:
   {
   "status": 200,
   "message": "用户信息获取成功。",
   "data": {
   "user_info": {
   "username": "example_user",
   "email": "user@example.com",
   "gender": "male",
   "birth_date": "1990-01-01",
   "avatar": "http://example.com/media/avatars/avatar.jpg"
   }
   }
   }
   失败响应:
   用户未登录：
   {
   "status": 401,
   "message": "用户未登录。",
   "data": {}
   }
6. 修改用户信息
   URL: /accounts/update-info/
   方法: POST
   请求参数:
   username (string, 可选): 用户名
   email (string, 可选): 邮箱
   password (string, 可选): 新密码
   old_password (string, 必须传递): 旧密码
   gender (string, 可选): 性别
   birth_date (string, 可选): 出生日期，格式为 "YYYY-MM-DD"
   avatar (file, 可选): 头像文件
   成功响应:
   {
   "status": 200,
   "message": "用户信息修改成功。",
   "data": {}
   }
   失败响应:
   原始密码不正确：
   {
   "status": 400,
   "message": "原始密码不正确。",
   "data": {}
   }
   出生日期格式不正确：
   {
   "status": 400,
   "message": "出生日期格式不正确。",
   "data": {}
   }
   安全性要求
   登录状态验证: 所有需要用户登录的操作（如获取用户信息、修改用户信息等）都要求用户已登录。

CSRF 保护: 在需要保护的视图函数中使用了 @csrf_exempt 装饰器来跳过 CSRF 校验;可以根据需要为特定接口启用 CSRF 校验。

密码保护: 在用户修改密码时，系统会要求输入原始密码以验证身份，确保安全。

错误处理
为方便前端开发，所有视图返回的status均为200，如需获取真实status code，请从返回的json数据中获取（data['status']）

status: 状态码 均为200
message: 提示信息
data: {}

备注
头像: 头像上传的文件会存储在服务器的 MEDIA_ROOT 目录下，前端可以通过返回的 URL 获取用户头像。
日期格式: 出生日期格式要求为 YYYY-MM-DD，不符合格式的日期会返回错误。
