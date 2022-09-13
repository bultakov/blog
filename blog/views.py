from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import (
    Category,
    Post,
    Comment,
    ReplyComment
)

from .forms import (
    PostForm,
    EditPostForm,
    CategoryForm
)


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/add_post.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddPostView, self).get_context_data(**kwargs)
        context['top'] = self.model.objects.order_by('-views')[:10]
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context


class PostView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostView, self).get_context_data(**kwargs)
        context['top'] = self.model.objects.order_by('-views')[:10]
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    form_class = EditPostForm

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['top'] = self.model.objects.order_by('-views')[:10]
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(DeletePostView, self).get_context_data(**kwargs)
        context['top'] = self.model.objects.order_by('-views')[:10]
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog-details.html'

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        post = self.model.objects.filter(slug=self.kwargs.get('slug')).first()
        post.views = post.views + 1
        post.save()
        stuff = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        total_likes = stuff.total_likes()
        liked: bool = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['top'] = self.model.objects.order_by('-views')[:10]
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/add_category.html'

    def get_context_data(self, **kwargs):
        cat_menu = self.model.objects.all()
        context = super(AddCategoryView, self).get_context_data(**kwargs)
        context['top'] = Post.objects.order_by('-views')[:10]
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(category=self.kwargs.get('pk'))
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category_post'] = posts
        context['name'] = self.model.objects.filter(pk=self.kwargs.get('pk')).first().name
        context['categorys'] = self.model.objects.all()
        context['category_count'] = self.model.objects.all().count()
        return context


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/blog-details.html'
    fields = ['body']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        form.instance.user = self.request.user
        return super(AddCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-view', kwargs={'slug': self.object.post.slug})


class AddReplyCommentView(LoginRequiredMixin, CreateView):
    model = ReplyComment
    template_name = 'blog/blog-details.html'
    fields = ['reply_body']

    def form_valid(self, form):
        form.instance.comment_id = self.kwargs.get('pk')
        form.instance.user = self.request.user
        return super(AddReplyCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-view', kwargs={'slug': self.object.comment.post.slug})


@login_required
def LikeView(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-view', args=[post.slug]))
