from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

class BaseRegisterView(CreateView): # Метод для регистрации пользователя на портале.
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/login'

@login_required
def upgrade_me(request): # Метод для обновления принадлежности пользователя к группе authors.
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts')