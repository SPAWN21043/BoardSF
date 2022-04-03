from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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


class PostDetail(LoginRequiredMixin, FormMixin, DetailView):
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


class CreatePost(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'creat.html'
    form_class = PostsForm
    permission_required = ('Posts.creat_post',)

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user
        return initial


class UpdatePostList(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'updatelist.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(UpdatePostList, self).get_context_data(**kwargs)
        user = self.request.user
        context['item'] = Posts.objects.filter(author=user)
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'creat.html'
    form_class = PostsForm
    '''permission_required'''

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Posts.objects.get(id_Post=id)


class PrivateList(LoginRequiredMixin, ListView):
    model = Responses
    template_name = 'privateposts.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super(PrivateList, self).get_context_data(**kwargs)
        user = self.request.user
        context['post_user'] = Posts.objects.filter(author=user)
        context['item'] = Responses.objects.filter(post__author=user)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def delete_responses(request, pk):
    try:
        responses = Responses.objects.get(id_response=pk)
        responses.delete()
        return HttpResponseRedirect('/private/')
    except Responses.DoesNotExist:
        return HttpResponseRedirect('<h2>Отклик не удален</h2>')


@login_required
def public_responses(request, pk):
    try:
        responses = Responses.objects.get(id_response=pk)
        responses.status = True
        responses.save()
        return HttpResponseRedirect('/private/')
    except Responses.DoesNotExist:
        return HttpResponseRedirect('<h2>Отклик не удален</h2>')


@login_required
def sub_category(request):
    user = request.user
    print(user)
    catt_id = request.POST['catt_id']
    category = Category.objects.get(pk=int(catt_id))

    if user not in category.subscribed.all():
        category.subscribed.add(user)

    else:
        category.subscribed.remove(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))
