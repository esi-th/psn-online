from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect


from .models import Category, Comment, Product, Review, Company
from .forms import NewCommentForm, NewReviewForm


def products_list_view(request):
    category = request.GET.get('category')
    product_filter = request.GET.get('filter_by')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all().order_by('-datetime_created')

    if min_price and max_price:
        products = products.filter(price__range=(min_price, max_price))

    if product_filter:
        products = products.filter(company__name__icontains=product_filter)

    if category:
        products = products.filter(category__name=category)

    paginator = Paginator(products, 6)
    page_num = request.GET.get('page')

    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    companies = Company.objects.all()

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
        'companies': companies,
    })


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['comment_form'] = NewCommentForm()
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        contex['comments'] = Comment.objects.filter(product=product, reply_to__isnull=True)
        contex['reviews'] = Review.objects.filter(product=product)
        contex['review_form'] = NewReviewForm()
        return contex


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = NewCommentForm

    def form_valid(self, form):
        comment_obj = form.save(commit=False)
        comment_obj.author = self.request.user

        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        comment_obj.product = product

        return super().form_valid(form)


@login_required
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    product = parent_comment.product

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.reply_to = parent_comment
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('products:product_detail', args=[product.id]))

        return HttpResponseRedirect(reverse('products:product_detail', args=[product.id]))


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    form_class = NewReviewForm

    def form_valid(self, form):
        review_obj = form.save(commit=False)
        review_obj.author = self.request.user

        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        review_obj.product = product

        return super().form_valid(form)


@require_POST
def product_search_view(request):
    if request.method == 'POST':
        product_keyword = request.POST['searched']
        products = Product.objects.filter(title__icontains=product_keyword).order_by('-datetime_modified')

        if not products:
            messages.warning(request, 'No Products Found!')
            return redirect('products:products_list')

        return render(request, 'products/products_list.html', context={
            'products': products,
        })
