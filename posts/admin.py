from django.contrib import admin

from .models import Post,PostReact

admin.site.register(Post)

admin.site.register(PostReact)