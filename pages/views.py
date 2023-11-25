from django.shortcuts import render, reverse
from django.views import generic
from django.contrib import messages
from accounts.models import CustomUser
from django.http import HttpResponseRedirect
from .models import DiscountSlider, TopSlider, TopProduct
from products.models import Product
from blog.models import Post


from .forms import ContactUsFrom


class HomePageView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        top_slider_products = TopSlider.objects.all()
        top_product_one = TopProduct.objects.first()
        top_product_two = TopProduct.objects.last()
        featured_products = Product.objects.all().order_by('-datetime_created')
        featured_products = featured_products[:6]
        discount_products = DiscountSlider.objects.all()
        products_list = Product.objects.all()[:8]
        blog_posts = Post.objects.all()[:2]
        contex['top_slider'] = top_slider_products
        contex['top_product_one'] = top_product_one
        contex['top_product_two'] = top_product_two
        contex['featured_products'] = featured_products
        contex['discount_products'] = discount_products
        contex['products_list'] = products_list
        contex['posts'] = blog_posts
        return contex


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
