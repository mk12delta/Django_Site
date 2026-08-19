from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count, Q
from .models import Movie, Director, Genre, Theme, Favorite, Review, Comment
from .forms import MovieForm, DirectorForm, ReviewForm, RecommendForm, DECADE_CHOICES
from django.contrib import messages
from django.contrib.auth import login


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class MovieCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_movie'
    model = Movie
    form_class = MovieForm
    template_name = 'catalog/movie_form.html'
    success_url = reverse_lazy('movie_list')


class DirectorCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_director'
    model = Director
    form_class = DirectorForm
    template_name = 'catalog/director_form.html'
    success_url = reverse_lazy('director_list')


@login_required
def my_movies(request):
    """Favorites list for the logged-in user."""
    favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    movie_ids = [fav.movie_id for fav in favorites]
    user_review_map = dict(
        Review.objects.filter(user=request.user, movie_id__in=movie_ids).values_list('movie_id', 'id')
    )
    return render(request, 'catalog/my_movies.html', {
        'favorites': favorites,
        'user_review_map': user_review_map,
    })


def index(request):
    """Home page."""
    context = {
        'num_movies': Movie.objects.count(),
        'num_directors': Director.objects.count(),
        'num_reviews': Review.objects.count(),
        'num_genres': Genre.objects.count(),
        'num_themes': Theme.objects.count(),
        'num_favorites': Favorite.objects.count(),
        'num_comments': Comment.objects.count(),
    }
    return render(request, 'index.html', context)


def movie_list(request):
    """List all movies."""
    movies = Movie.objects.all()

    favorite_movie_ids = []
    user_review_map = {}
    if request.user.is_authenticated:
        favorite_movie_ids = list(
            Favorite.objects.filter(user=request.user).values_list('movie_id', flat=True)
        )
        user_review_map = dict(
            Review.objects.filter(user=request.user).values_list('movie_id', 'id')
        )

    return render(request, 'catalog/movie_list.html', {
        'movie_list': movies,
        'favorite_movie_ids': favorite_movie_ids,
        'user_review_map': user_review_map,
    })


def movie_detail(request, pk):
    """Detail page for a single movie."""
    movie = get_object_or_404(Movie, pk=pk)
    is_favorite = (
        request.user.is_authenticated and
        Favorite.objects.filter(user=request.user, movie=movie).exists()
    )
    reviews = movie.reviews.filter(is_hidden=False).select_related('user')
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    return render(request, 'catalog/movie_detail.html', {
        'movie': movie,
        'is_favorite': is_favorite,
        'reviews': reviews,
        'user_review': user_review,
    })


@login_required
def add_favorite(request, pk):
    """Add a movie to the logged-in user's favorites."""
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        Favorite.objects.get_or_create(user=request.user, movie=movie)
    return redirect(request.POST.get('next', 'my_movies'))


@login_required
def remove_favorite(request, pk):
    """Remove a movie from the logged-in user's favorites."""
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        Favorite.objects.filter(user=request.user, movie=movie).delete()
    return redirect(request.POST.get('next', 'my_movies'))


@login_required
def write_review(request, pk):
    """Create a review for a movie. One per user per movie."""
    movie = get_object_or_404(Movie, pk=pk)
    if Review.objects.filter(user=request.user, movie=movie).exists():
        return redirect('movie_detail', pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'catalog/review_form.html', {'form': form, 'movie': movie})


@login_required
def edit_review(request, pk):
    """Edit the logged-in user's own review."""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=review.movie.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'catalog/review_form.html', {
        'form': form,
        'movie': review.movie,
        'editing': True,
    })


@login_required
def delete_review(request, pk):
    """Delete the logged-in user's own review."""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    movie_pk = review.movie.pk
    if request.method == 'POST':
        review.delete()
    return redirect('movie_detail', pk=movie_pk)


def director_list(request):
    """List all directors."""
    directors = Director.objects.all()
    return render(request, 'catalog/director_list.html', {'director_list': directors})


def director_detail(request, pk):
    """Detail page for a single director."""
    director = get_object_or_404(Director, pk=pk)
    return render(request, 'catalog/director_detail.html', {'director': director})


def genre_list(request):
    """List all genres."""
    return HttpResponse("Genre list — coming soon")


def genre_detail(request, pk):
    """Detail page for a single genre."""
    genre = get_object_or_404(Genre, pk=pk)
    return HttpResponse(f"Genre detail: {genre.name} — coming soon")


def theme_list(request):
    """List all themes."""
    return HttpResponse("Theme list — coming soon")


def theme_detail(request, pk):
    """Detail page for a single theme."""
    theme = get_object_or_404(Theme, pk=pk)
    return HttpResponse(f"Theme detail: {theme.name} — coming soon")


def review_list(request):
    """List all reviews."""
    return HttpResponse("Review list — coming soon")


def review_detail(request, pk):
    """Detail page for a single review."""
    review = get_object_or_404(Review, pk=pk)
    return HttpResponse(f"Review detail: {review} — coming soon")


def comment_list(request):
    """List all comments."""
    return HttpResponse("Comment list — coming soon")


def comment_detail(request, pk):
    """Detail page for a single comment."""
    comment = get_object_or_404(Comment, pk=pk)
    return HttpResponse(f"Comment detail: {comment} — coming soon")


def favorite_list(request):
    """List all favorites."""
    return HttpResponse("Favorites list — coming soon")


def favorite_detail(request, pk):
    """Detail page for a single favorite."""
    favorite = get_object_or_404(Favorite, pk=pk)
    return HttpResponse(f"Favorite detail: {favorite} — coming soon")


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_movie'
    model = Movie
    form_class = MovieForm
    template_name = 'catalog/movie_form.html'
    success_url = reverse_lazy('movie_list')


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_movie'
    model = Movie
    template_name = 'catalog/movie_delete.html'
    success_url = reverse_lazy('movie_list')


class DirectorUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_director'
    model = Director
    form_class = DirectorForm
    template_name = 'catalog/director_form.html'
    success_url = reverse_lazy('director_list')


class DirectorDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_director'
    model = Director
    template_name = 'catalog/director_delete.html'
    success_url = reverse_lazy('director_list')

def recommend_movie(request):
    """Page for user to make selections to have a movie recommended"""
    form = RecommendForm(request.GET or None)
    results = Movie.objects.none()

    if form.is_valid():
        genres = form.cleaned_data['genres']
        themes = form.cleaned_data['themes']
        decades = form.cleaned_data['decades']
        results = Movie.objects.all()

        if decades:
            decade_queries = Q()
            for decade in decades:
                if decade != "any":
                    start = int(decade)
                    end = start + 9
                else:
                    start = DECADE_CHOICES[0][0]
                    end = DECADE_CHOICES[-2][0]
                decade_queries |= Q(year_created__range=(start, end))
            results = results.filter(decade_queries)

        if genres:
            results = results.annotate(
                matched_genres=Count('genres', filter=Q(genres__in=genres), distinct=True)
            )

        if themes:
            results = results.annotate(
                matched_themes=Count('themes', filter=Q(themes__in=themes), distinct=True)
            )

        if genres:
            results = results.filter(genres__in=genres)
        if themes:
            results = results.filter(themes__in=themes)

        results = results.distinct()
        results = results.order_by('-matched_genres', '-matched_themes', 'title')

    context = {'form':form, 'results':results}
    return render(request, 'catalog/recommend_movie.html', context)

