from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """禁用 CSRF 检查的 Session 认证"""

    def enforce_csrf(self, request):
        return  # 不执行 CSRF 检查
