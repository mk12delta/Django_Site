from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Movie, Director, Genre, Theme, Review


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['first_name', 'last_name']


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year_created', 'description', 'genres', 'themes', 'directors', 'movie_image']
        widgets = {
            'themes': forms.SelectMultiple,
            'directors': forms.SelectMultiple,
        }

RATING_CHOICES = [(i, '★' * i) for i in range(1, 6)]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
        label='Rating',
    )

    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'id': 'id_review_text',
                'class': 'd-none',
            }),
        }
        labels = {
            'review_text': 'Your Review',
        }


DECADE_CHOICES = [
    ('1960', '60s'),
    ('1970', '70s'),
    ('1980', '80s'),
    ('1990', '90s'),
    ('2000', '2000s'),
    ('2010', '2010s'),
    ('2020', '2020s'),
    ('any', 'any')
]

class RecommendForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(
        label="What genre do you feel like watching? (Select at least 1)",
        queryset=Genre.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )
    themes = forms.ModelMultipleChoiceField(
        label="Which of these themes sound good? (Select at least 1)",
        queryset=Theme.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )
    decades = forms.MultipleChoiceField(
        label="Feeling a particular film era? (Select at least 1)",
        choices=DECADE_CHOICES,
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )