from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
from .models import Blog, Blogger, Comment
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def index(request):
    return render(request, 'blog/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            form.cleaned_data.get('password1')

            # login user after signing up
            login(request, user)

            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class BlogListView(generic.ListView):
    """Generic class-based view listing all blogs."""
    model = Blog
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.order_by('-post_date')


class BloggerListView(generic.ListView):
    """Generic class-based view listing all bloggers."""
    model = Blogger


class BlogDetailView(generic.DetailView):
    """Generic class-based view displaying Blog post details."""
    model = Blog


class BloggerDetailView(generic.DetailView):
    """Generic class-based view displaying Blogger details."""
    model = Blogger


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['description']

    def form_valid(self, form):
        form.instance.comment_by = self.request.user
        form.instance.comment_on = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(CreateCommentView, self).form_valid(form)

    def get_success_url(self):
        blog_id = self.object.comment_on.pk
        return reverse_lazy('blog_detail', kwargs={'pk': blog_id})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateCommentView, self).get_context_data(**kwargs)
        # Get the blog object from the "pk" URL parameter and add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context


class CreateBlogView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'post']

    def form_valid(self, form):
        # Queryset filters Blogger model.
        queryset = Blogger.objects.filter(name=self.request.user)
        # Checks if the queryset exists.
        if queryset.exists():
            # If blogger exists, get the user
            blogger_name = Blogger.objects.get(name=self.request.user)
            form.instance.blogger = blogger_name
            return super(CreateBlogView, self).form_valid(form)
        else:
            # if blogger doesn't exist create a blogger
            blogger_name = Blogger.objects.create(name=self.request.user)
            form.instance.blogger = blogger_name
            return super(CreateBlogView, self).form_valid(form)


