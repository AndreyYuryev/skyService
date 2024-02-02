from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from mailstream.models import Stream
from bootstrap_datepicker_plus.widgets import DatePickerInput
from mailstream.models import Client
# from django.forms.models import ModelMultipleChoiceField


# class CustomSelectMultiple(ModelMultipleChoiceField):
#     def label_from_instance(self, obj):
#         return "%s - %s" %(obj.email, obj.fullname)

class DateForm(ModelForm):
    # clients = ModelMultipleChoiceField(queryset=Client.objects.all(), widget=CheckboxSelectMultiple(),
    #                                         required=False, label='Подписчики')
    # clients = CustomSelectMultiple(queryset=Client.objects.all(), required=False)
    class Meta:
        model = Stream
        fields = ('name',
                  'started_at',
                  'ended_at',
                  'message',
                  'client',
                  'regularity',
                  'status',)
        widgets = {
            # 'started_at': DateTimeInput(format=('%d %B %Y %H:%M:%S'),
            #                             attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # 'ended_at': DateInput(attrs={'type': 'datetime-local',})
            # "clients": CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            "started_at": DatePickerInput(options={"format": "DD MMMM YYYY", 'locale': 'RU', }),
            "ended_at": DatePickerInput(range_from="started_at", options={"format": "DD MMMM YYYY", 'locale': 'RU', }),
        }

    class Media:
        js = ('js/jquery.js',)
