from django.contrib import admin
from .models import Post, PostRating


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "text", "date_added"]
    list_filter = ["date_added", "author"]


@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "rating"]
    list_filter = ["user", "post"]
