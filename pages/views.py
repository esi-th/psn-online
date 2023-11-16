from django.shortcuts import render
from django.views import generic
from django.contrib import messages


from .forms import ContactUsFrom


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class AboutUsPageView(generic.TemplateView):
    template_name = 'pages/about_us.html'


def contact_us_page_view(request):
    if request.method == 'POST':
        form = ContactUsFrom(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your Message Successfully Saved.')

    form = ContactUsFrom()
    return render(request, 'pages/contact_us.html', context={
        'contact_us_form': form,
    })
