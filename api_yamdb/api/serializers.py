from authentication.models import User
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class UsernameValidate:
    """Абстрактный класс для валидации ограничений имени пользователя."""

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя пользователя недопустимо')
        return value


class UserAdminSerializer(serializers.ModelSerializer, UsernameValidate):
    """Сериализация управления пользователя Админом."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        lookup_field = "username"


class UserMeSerializer(serializers.ModelSerializer, UsernameValidate):
    """Сериализация регистрации пользователя для /me эндпойнта."""

    username = serializers.CharField(
        max_length=150,
        required=False
    )

    email = serializers.CharField(
        max_length=254,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = (
            'role',
        )


class RegistrationSerializer(serializers.ModelSerializer, UsernameValidate):
    """Сериализация регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """Сериализация Входа пользователя."""
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(
        read_only=True
    )
    genre = GenresSerializer(
        many=True,
        read_only=True
    )
    rating = serializers.SerializerMethodField(
        allow_null=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
            'rating'
        )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = (
            'id',
            'author',
            'pub_date'
        )

    def create(self, validated_data):
        title = validated_data.get('title')
        author = validated_data.get('author')
        review = Review.objects.filter(title=title, author=author).first()
        if review:
            raise serializers.ValidationError('Недопустимое значение')
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = (
            'id',
            'author',
            'pub_date'
        )

    def create(self, validated_data):
        text = validated_data.get('text')
        review = validated_data.get('review')
        author = validated_data.get('author')
        comment = Comment.objects.filter(
            review=review,
            author=author,
            text=text).first()
        if comment:
            raise serializers.ValidationError('Недопустимое значение')
        return Comment.objects.create(**validated_data)
