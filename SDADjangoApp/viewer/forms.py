import re

from django.core.exceptions import ValidationError
from django.forms import (
  CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea
)

from viewer.models import Genre

from datetime import date


class PastMonthField(DateField):

    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=result.day)


class MovieForm(Form):
    title = CharField(max_length=128)
    genre = ModelChoiceField(queryset=Genre.objects)
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()
    description = CharField(widget=Textarea, required=False)

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')

        if len(sentences) <= 2:
            raise ValidationError("We need at least 3 sentences for the movie description")

        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'Comedy' and result['rating'] > 5:
          self.add_error('genre', 'Genre error configuration')
          self.add_error('rating', '')
          raise ValidationError(
            "Commedies aren't so good to be rated over 5."
            )
        return result