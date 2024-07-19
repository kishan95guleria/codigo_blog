from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import *
from django.views import View
from django.contrib.auth import logout
from django.views.generic import ListView  ,DetailView
from django.db.models import Q
from .searching import BlogDocument
from .decorder import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail

@method_decorator(login_required, name='dispatch')
class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5 

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return BlogDocument.search().query('match', content=query).to_queryset()
        return Blog.objects.all().order_by('-published_date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all() 
        return context    
@method_decorator(login_required, name='dispatch')
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    @check_authorized
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        if request.user.is_authenticated:
            comment_content = request.POST.get('comment')
            # Check if the user has already commented
            if not blog.comments.filter(author=request.user).exists():
                Comment.objects.create(
                    blog=blog,
                    author=request.user,
                    content=comment_content
                )
        return redirect(reverse('blog_detail', args=[blog.pk]))    

class BlogLoginView(LoginView):
    template_name = 'login.html'  
    redirect_authenticated_user = True  
    success_url = reverse_lazy('blog_list') 
    authentication_form = CustomAuthenticationForm

class SignUpView(CreateView):
    form_class = BlogUserCreationForm
    template_name = 'signup.html' 
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return response    

class BlogLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class Not_Authorized(View):
    def get(self, request):
        return render(request, 'not_authorized.html')      
@method_decorator(login_required, name='dispatch')           
class ShareBlogView(View):
    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        name = request.POST.get('name')
        to_email = request.POST.get('to_email')
        comments = request.POST.get('comments')

        subject = f"Check out this blog post: {blog.title}"
        message = f"Hi,\n\n{name} has shared a blog post with you:\n\nTitle: {blog.title}\nPublished Date: {blog.published_date}\n\n{comments}\n\nYou can read the post here: {request.build_absolute_uri(blog.get_absolute_url())}"
        from_email = 'demowisdom694@gmail.com'

        send_mail(subject, message, from_email, [to_email])

        return redirect(reverse('blog_detail', args=[pk]))        
@method_decorator(login_required, name='dispatch')
class AddCommentView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if not blog.comments.filter(author=request.user).exists():
            comment_content = request.POST.get('comment')
            Comment.objects.create(
                blog=blog,
                author=request.user,
                content=comment_content
            )
        return redirect(reverse('blog_detail', args=[pk]))