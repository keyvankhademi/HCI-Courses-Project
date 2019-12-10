from django import forms
from dal import autocomplete
from HCI.models import Course, University


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'university', 'description', 'url', 'prerequisites', 'core_for_major',
                  'last_taught', 'instructor', 'learning_goals', 'equivalent']

    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        widget=autocomplete.ModelSelect2(url='university:auto_complete')
    )
