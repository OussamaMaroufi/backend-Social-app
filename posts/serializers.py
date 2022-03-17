from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post,Comment
from users.serializers import UserProfileSerializer, UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    # original_post = serializers.SerializerMethodField(read_only=True)
    up_voters = serializers.SerializerMethodField(read_only=True)
    down_voters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data
    # Also it stil to define original post and up_voters and down_voters

    # def get_original_post(self, obj):
    #     original = obj.repost
    #     if original != None:
    #         serializer = PostSerializer(original, many=False)
    #         return serializer.data
    #     else:
    #         return None

    def get_up_voters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(
            post=obj, value='like').values_list('user', flat=True)

        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data

    def get_down_voters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(
            post=obj, value='dislike').values_list('user', flat=True)

        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField(read_only=True)
       

        class Meta:
            model = Comment
            fields = '__all__'

        def get_user(self, obj):
            user = obj.user.userprofile
            serializer = UserProfileSerializer(user, many=False)
            return serializer.data
