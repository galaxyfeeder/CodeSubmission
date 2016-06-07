from django import forms

from review.models import Review


class ReviewForm(forms.ModelForm):
    status = forms.ChoiceField(choices=((2, 'Accepted'), (3, 'Declined')))

    class Meta:
        model = Review
        fields = ['comment', 'status']
