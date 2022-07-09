from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    LoginAPIView, RegistrationAPIView, ReviewViewSet,
                    TitlesViewSet, UsersViewSet)

router_v1 = SimpleRouter()
router_v1.register(
    r'users', UsersViewSet,
    basename='user'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='reviews'
)
router_v1.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenresViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)

urlpatterns = [
    path('v1/auth/token/', LoginAPIView.as_view()),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
