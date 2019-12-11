from dal import autocomplete
from django import forms
from django.urls import reverse_lazy

from HCI.choices import get_all_states
from HCI.models import Course, University


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'university', 'description', 'url', 'prerequisites', 'core_for_major',
                  'last_taught', 'instructor', 'learning_goals', 'equivalent']

    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        widget=autocomplete.ModelSelect2(url='university:auto_complete'),
        help_text="Don't find your university? <a href=\"{}\">Add one.</a>",
    )

    equivalent = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='course:auto_complete'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['university'].help_text = self.fields['university'].help_text.format(reverse_lazy('university:add'))


class UniversityCreateForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'short_name', 'country', 'state', 'city']

    state = forms.ChoiceField(
        choices=get_all_states(),
        widget=autocomplete.Select2(url='university:state_auto_complete', forward=['country'])
    )

