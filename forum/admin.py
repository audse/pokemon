from django.contrib import admin
from .models import Bookmark, Category, Post, Reply

admin.site.register(Bookmark)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reply)