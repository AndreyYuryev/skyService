from django.forms import ModelForm, DateTimeInput, DateInput
from mailstream.models import Stream
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class DateTimeForm(ModelForm):
    class Meta:
        model = Stream
        fields = ('name',
                  'started_at',
                  'ended_at',
                  'message',
                  'regularity',
                  'status',
                  'all_recipient',)
        widgets = {
            # 'started_at': DateTimeInput(format=('%d %B %Y %H:%M:%S'),
            #                             attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # 'ended_at': DateInput(attrs={'type': 'datetime-local',})
            "started_at": DateTimePickerInput(options={"format": "DD MMMM YYYY, HH:mm:ss", 'locale': 'RU',}),
            "ended_at": DateTimePickerInput(range_from="started_at"),
        }
    class Media:
        js = ('js/jquery.js',)