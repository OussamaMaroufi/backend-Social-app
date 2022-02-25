from django.contrib import admin

from .models import Post,PostReact,Comment

admin.site.register(Post)

admin.site.register(PostReact)

admin.site.register(Comment)