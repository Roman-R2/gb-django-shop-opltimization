from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class AdminAccessMixin:
    # Проверим, что пользователь администратор
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
