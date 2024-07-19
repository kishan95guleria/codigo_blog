
from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('login/', BlogLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', BlogLogoutView.as_view(), name='logout'),
    path('blog/<int:pk>/share/', ShareBlogView.as_view(), name='share_blog'),
    path('not-authorized/', Not_Authorized.as_view(), name='not_authorized'),
    path('blog/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
]