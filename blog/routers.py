from rest_framework import routers
from rest_framework.response import Response
from blog import views

router = routers.SimpleRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
