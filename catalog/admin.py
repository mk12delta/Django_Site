from django.contrib import admin
from .models import Genre, Theme, Director, Movie, Favorite, Review, Comment

# Register your models here.
admin.site.register(Genre)
admin.site.register(Theme)
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name']
    search_fields = ['first_name', 'last_name']



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year_created']
    list_filter = ['genres']
    search_fields = ['title', 'description']
    filter_horizontal = ['genres', 'themes', 'directors']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'rating', 'is_hidden', 'created_at']
    list_filter = ['rating', 'is_hidden']
    search_fields = ['review_text']

    @admin.action(description='Hide selected reviews')
    def hide_reviews(modeladmin, request, queryset):
        queryset.update(is_hidden=True)

    @admin.action(description='Unhide selected reviews')
    def unhide_reviews(modeladmin, request, queryset):
        queryset.update(is_hidden=False)

    actions = [hide_reviews, unhide_reviews]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'is_hidden', 'created_at']
    list_filter = ['is_hidden']
    search_fields = ['comment_text']

    @admin.action(description='Hide selected comments')
    def hide_comments(modeladmin, request, queryset):
        queryset.update(is_hidden=True)

    @admin.action(description='Unhide selected comments')
    def unhide_comments(modeladmin, request, queryset):
        queryset.update(is_hidden=False)

    actions = [hide_comments, unhide_comments]







