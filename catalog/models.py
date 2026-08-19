from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    """Model representing a movie genre."""
    name = models.CharField(max_length=100, unique=True, help_text="Enter a genre (e.g., Action)")

    def __str__(self):
        return self.name


class Theme(models.Model):
    """Model representing a movie theme/tag."""
    name = models.CharField(max_length=100, unique=True, help_text="Enter a theme (e.g., Revenge)")

    def __str__(self):
        return self.name


class Director(models.Model):
    """Model representing a director."""
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    date_of_birth = models.CharField(max_length=60, blank=True, default='')
    date_of_death = models.CharField(max_length=60, blank=True, default='')

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        return reverse("director_detail", args=[str(self.id)])


class Movie(models.Model):
    """Model representing a movie title."""
    title = models.CharField(max_length=200)
    year_created = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    genres = models.ManyToManyField(Genre, related_name="movies", help_text="Select one genre")
    themes = models.ManyToManyField(Theme, related_name="movies", blank=True)
    directors = models.ManyToManyField(Director, related_name="movies", blank=True)

    # Optional: image like your old project had
    movie_image = models.ImageField(upload_to="images/", null=True, blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", args=[str(self.id)])


class Favorite(models.Model):
    """Join table: a user favorites a movie."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="uq_favorite_user_movie")
        ]

    def __str__(self):
        return f"{self.user.username} favorited {self.movie.title}"


class Review(models.Model):
    """A user review for a movie (rating + optional text)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False, help_text="If True, review is hidden from public view (soft-delete moderation)")

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="uq_review_user_movie")
        ]

    def __str__(self):
        return f"Review({self.movie.title}) by {self.user.username}"


class Comment(models.Model):
    """A comment on a review."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")

    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False, help_text="If True, comment is hidden from public view (soft-delete moderation)")
    
    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on Review {self.review.id}"
