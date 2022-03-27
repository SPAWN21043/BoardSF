from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from .models import Posts, Category, Responses
from Post.forms import PostsForm, ResponseForm
from .filters import SearchFilter


class PostsList(ListView):
    model = Posts
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Posts.objects.order_by('-id_Post')
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(FormMixin, DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = ResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().id_Post})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CreatePost(CreateView):
    model = Posts
    template_name = 'creat.html'
    form_class = PostsForm
    permission_required = ('Post.creat_post',)


class PrivateList(ListView):
    model = Responses
    template_name = 'privateposts.html'
    context_object_name = 'response'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        return context







