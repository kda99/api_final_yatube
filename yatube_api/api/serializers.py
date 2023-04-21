from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',
                                        read_only=True,
                                        default=serializers.
                                        CurrentUserDefault())
    following = serializers.SlugRelatedField(slug_field='username',
                                             read_only=False,
                                             queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [serializers.UniqueTogetherValidator(
            queryset=Follow.objects.all(), fields=('user', 'following'))]

    def validate_following(self, value):
        user = self.context['request'].user
        following = value
        if user == following:
            raise serializers.ValidationError('You cannot follow yourself!')
        return value

    def validate_user(self, value):
        if isinstance(value, User):
            raise serializers.ValidationError('Тип данных подписчика не'
                                              ' соответствует!')
        return value
