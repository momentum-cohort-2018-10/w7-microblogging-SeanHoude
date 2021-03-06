from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import (TemplateView, RedirectView,)
from blog import views
from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
from blog.routers import router

urlpatterns = [
    path('', views.index, name='home'),
    path('posts/<slug>/', views.post_detail, name='post_detail'),
    path('create_hail', views.create_hail, name='create_hail'),
    path('posts/<slug>/edit_post/', views.edit_post, name='edit_post'),
    path('post/<slug>/add_comment_to_post', views.add_comment_to_post,
         name="add_comment_to_post"),
    path('post/<slug>/<pk>/edit_comment', views.edit_comment, name='edit_comment'),
    path('post/<slug>/<pk>/delete_comment', views.delete_comment, name='delete_comment'),
    path('search', views.search, name='search'),
    path('post/<slug>/favorited', views.toggle_favorite, name='toggle_favorite'),
    path('post/<slug>/liked', views.toggle_like, name='toggle_like'),
    path('<request.user>/<pk>/followed', views.toggle_follow, name='toggle_follow'),    
    path('<request.user>/liked', views.liked, name='liked'),
    path('<request.user>/favorited', views.favorited, name='favorited'),
    path('<request.user>/posted', views.posted, name='posted'),
    path('<request.user>/commented', views.commented, name='commented'),
    path('profiles/<username>/', views.user_profile, name='user_profile'),
    # Password Reset URL's
    path('accounts/password/reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name="password_reset"),
    path('accounts/password/reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path('accounts/password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name="password_reset_confirm"),
    path('accounts/password/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name="password_reset_complete"),
    # REST API urls
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/posts/', views.PostListCreate.as_view(), name='post_list_create'),
    path('api/v1/follows/', views.FollowListCreate.as_view(), name="follow_list_create"),
    path('api/v1/followdestroy/<str:username>/', views.FollowRetrieveUpdateDestroy.as_view(), name="follow_destroy"),
    path('api/v1/comments/create', views.CommentListCreate.as_view(), name='comment_create'),
    # REST API V2
    path('api/v2/', include((router.urls, 'posts'), namespace='apiv2')),
    # Registration/admin urls
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/register', views.NewRegistrationView.as_view(), name='registration_register'),
    path('accounts/allauth/', include('allauth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
