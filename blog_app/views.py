from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from blog_app.forms import PostForm
from blog_app.models import Post

## CRUD
# C => CREATE
# R => READ/RETRIEVE
# U => UPDATE
# D => DELETE
## FUNCTION-BASED VIEWS

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("draft-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)




class PostListView(ListView):
    model=Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")

class PostDetailView(DetailView):
    model=Post
    template_name = "post_detail.html"
    context_object_name = "post"
    
    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset    


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "draft_list.html"
    context_object_name = "drafts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")

class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "draft_detail.html"
    context_object_name = "draft"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset





   
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    
    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("draft-detail", kwargs={"pk": post.pk})
        
class PostUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(request,
                      "post_create.html",
                      {"form":form},
                      )
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(request,
                      )


    
class PostDeleteView(LoginRequiredMixin, View):
    def get(self,request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk, published_at__isnull=False)
        post.delete()
        return redirect("post-list")
    



class DraftDeleteView(LoginRequiredMixin, View):
    def get(self,request, pk, *args, **kwargs):
        draft = Post.objects.get(pk=pk, published_at__isnull=True)
        draft.delete()
        return redirect("draft-list")
    

class DraftPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        draft = Post.objects.get(pk=pk, published_at__isnull=True)
        draft.published_at = timezone.now()
        draft.save()
        return redirect("post-detail", draft.pk)







