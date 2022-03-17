from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

#TO handle image convert
import base64
from django.core.files.base import ContentFile


from .models import Post, PostReact,Comment
from .serializers import PostSerializer,CommentSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def posts(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''


    

    user = request.user
    following = user.following.select_related('user')

    following = user.following.all()

    ids = []
    ids = [i.user.id for i in following]
    ids.append(user.id)
    print('IDS:', ids)

    # Query 5 posts form users you follow
    posts = list(Post.objects.filter(
        parent=None, user__id__in=ids).order_by("-created"))[0:5]

    # Query top ranked posts
    topPosts = Post.objects.filter(
        Q(parent=None)).order_by("-vote_rank", "-created")

    # Query recent posts
    recentPosts = Post.objects.filter(Q(parent=None) & Q(
        vote_rank__gte=0)).order_by("-created")[0:5]

    # Add Top Ranked posts To List of posts

    index = 0
    for post in recentPosts:
        if post not in posts:
            posts.insert(index, post)
            index += 1

    # Add Top ranked posts to feed in list of posts
    for post in topPosts:
        if post not in posts:
            posts.append(post)
            

    _query = Q(content__icontains=query)
    
    if query != '':
        posts = Post.objects.filter(_query)

    

    paginator = PageNumberPagination()
    paginator.page_size = 8     #10
    result_page = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# This View for post creation
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_post(request):
    user = request.user
    data = request.data

    # print("Hello this data ",data)


    # is_comment = data.get('isComment')
    # if is_comment:
    #     parent = Mumble.objects.get(id=data['postId'])
    #     mumble = Mumble.objects.create(
    #         parent=parent,
    #         user=user,
    #         content=data['content'],
    #     )
    # else:

    img = data['image']
    if img["base64Data"] != '' :

        file = ContentFile(base64.b64decode(img["base64Data"]), name='temp.' + img["imageType"])
        print("Image",img)

    # format, imgstr = img.split(';base64,') 
    # ext = format.split('/')[-1]


        post = Post.objects.create(
                user=user,
                content=data['content'],
                image=file

        )
    else:
            post = Post.objects.create(
                user=user,
                content=data['content'],
            )


    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def edit_post(request, pk):
    user = request.user
    data = request.data

    try:
        post = Post.objects.get(id=pk)

        if user != post.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = PostSerializer(post, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def delete_post(request, pk):
    user = request.user
    try:
        post = Post.objects.get(id=pk)
        if user != post.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def post_details(request, pk):
    try:
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    except:
        message = {
            'detail': 'Post doesn\'t exist'
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def post_comments(request, pk):
#     post = Post.objects.get(id=pk)
#     comments = post.post_set.all()
#     serializer = PostSerializer(comments, many=True)
#     return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_react(request,pk):
    user = request.user
    data = request.data

    print("user",user)

    print("data are",data)

    post = Post.objects.get(id=pk)
    # What if user is trying to remove their vote?
    react, created = PostReact.objects.get_or_create(post=post, user=user)

    if react.value == data.get('value'):
        # If same value is sent, user is clicking on vote to remove it
        react.delete()
    else:

        react.value = data['value']
        react.save()

    # We re-query the vote to get the latest vote rank value
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def repost(request):
    pass



#Crud Operation For comment 
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getComments(request,pk):
    post = Post.objects.get(id=pk)
    print(post)
    comments = post.comment_set.all()
    serializer = CommentSerializer(comments,many=True)

    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def delete_comment(request, pk):
    user = request.user
    try:
        comment = Comment.objects.get(id=pk)
        if user != comment.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)



@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def edit_comment(request,pk):
    user = request.user
    data = request.data

    try:
        comment =  Comment.objects.get(id=pk)
        if user !=comment.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = CommentSerializer(comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)



    except Exception as e:
        return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_comment(request,pk):
    user = request.user
    data = request.data
    post = Post.objects.get(id=pk)

    post_serializer = PostSerializer(post,many=False)
    print(post_serializer.data)

    # post.comment_count =  post.comment_count + 1 
    # post.save()
    # print(post)

    comment = Comment.objects.create(user=user,post=post,content=data['content'])

    serializer = CommentSerializer(comment,many=False)

    return Response(serializer.data,status=status.HTTP_201_CREATED)







