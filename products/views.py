from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import generic


from .models import Category, Comment, Product, Review
from .forms import NewCommentForm, NewReviewForm


def products_list_view(request):
    category = request.GET.get('category')

    if category is not None:
        products = Product.objects.filter(category__name=category).order_by('datetime_modified')
    else:
        products = Product.objects.all().order_by('datetime_created')

    paginator = Paginator(products, 1)
    page_num = request.GET.get('page')

    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
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
    post = parent_comment.product

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.reply_to = parent_comment
            new_comment.save()

    return reverse('post_detail', args=[comment_id])


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
        products = Product.objects.filter(title__contains=product_keyword).order_by('-datetime_modified')

        if not products:
            messages.warning(request, 'No Products Found!')
            return redirect('products_list')

        return render(request, 'products/products_list.html', context={
            'products': products,
        })
