from django.forms import DateInput


class MyDateInput(DateInput):
    template_name = 'models/widgets/date_picker.html'
