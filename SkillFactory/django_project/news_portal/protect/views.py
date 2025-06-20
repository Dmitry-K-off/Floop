import pytz
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page # Импорт для кэширования.
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render

from news.models import Author


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get(self, request):
        current_time = timezone.now()
#        models = Author.objects.all()

        context = {
#            'models': models,
            'current_time': current_time,
            'timezones': pytz.common_timezones,
            'selected_timezone': request.session.get('django_timezone'),
        }

        return render(request, 'protect/index.html', context)

    def post(self, request):
        timezone_str = request.POST.get('timezone')

        if timezone_str and timezone_str in pytz.common_timezones:
            request.session['django_timezone'] = timezone_str
        else:
            request.session['django_timezone'] = timezone.get_default_timezone_name()

        return redirect('/')