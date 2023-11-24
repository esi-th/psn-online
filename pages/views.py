from django.shortcuts import render, reverse
from django.views import generic
from django.contrib import messages
from accounts.models import CustomUser
from django.http import HttpResponseRedirect


from .forms import ContactUsFrom


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class AboutUsPageView(generic.TemplateView):
    template_name = 'pages/about_us.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        last_users = CustomUser.objects.all()[:4]
        contex['last_users'] = last_users
        return contex


def contact_us_page_view(request):
    if request.method == 'POST':
        form = ContactUsFrom(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your Message Successfully Saved.')
            return HttpResponseRedirect(reverse('contact_us'))

    form = ContactUsFrom()
    return render(request, 'pages/contact_us.html', context={
        'contact_us_form': form,
    })
