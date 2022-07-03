from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from core.utils import EmailSender
from reviews.models import Category, Genre, Title
from .mixins import ListCreateDestroyViewSet
from .filters import TitleSearchFilter
from .serializers import (
    UserAdminSerializer,
    UserMeSerializer,
    RegistrationSerializer,
    LoginSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitlesReadSerializer,
    TitlesCreateSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from .permissions import (
    AdminOnlyPermission,
    IsAdminOrReadOnly,
    ReadOnlyOrModOrAdmin,
)


User = get_user_model()


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        sender = EmailSender(request)
        code = sender.get_code_for_user(user)
        try:
            sender.send_token_for_mail(user.email, code)
        except Exception:
            user.delete()
            return Response(serializer.data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user.confirmation_code = code
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response({'confirmation_code': 'uncorrect  confirmation_code'},
                        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return UserAdminSerializer

    def get_permissions(self):
        if self.action == 'me':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated, AdminOnlyPermission,)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get', 'patch', 'delete'])
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReadOnlyOrModOrAdmin,)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_title_id(self):
        return self.kwargs.get('title_id')

    def get_title(self):
        return get_object_or_404(Title, pk=self.get_title_id())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReadOnlyOrModOrAdmin,)

    def get_queryset(self):
        title = self.get_title()
        review = get_object_or_404(title.reviews, pk=self.get_review_id())
        return review.comments.all()

    def perform_create(self, serializer):
        title = self.get_title()
        review = get_object_or_404(title.reviews, pk=self.get_review_id())
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        title = self.get_title()
        review = get_object_or_404(title.reviews, pk=self.get_review_id())
        serializer.save(author=self.request.user, review=review)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_review_id(self):
        return self.kwargs.get('review_id')


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleSearchFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesCreateSerializer
