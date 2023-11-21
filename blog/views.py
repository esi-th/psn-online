from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, Category, Comment
from .forms import NewCommentForm


def post_list_view(request):
    posts = Post.objects.all().order_by('-datetime_created')
    categories = Category.objects.all()

    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page')

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/posts_list.html', context={
        'posts': posts,
        'categories': categories,
    })


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = NewCommentForm()
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post=post, reply_to__isnull=True)
        context['likes'] = post.likes.count()
        return context


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = NewCommentForm

    def form_valid(self, form):
        comment_obj = form.save(commit=False)
        comment_obj.author = self.request.user

        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        comment_obj.post = post

        return super().form_valid(form)


@login_required
@require_POST
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post
    form = NewCommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.author = request.user
        new_comment.reply_to = parent_comment
        new_comment.save()
        HttpResponseRedirect(reverse('blog:post_detail', args=[post.id]))
    return HttpResponseRedirect(reverse('blog:post_detail', args=[post.id]))


@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:post_detail', args=[post_id]))
