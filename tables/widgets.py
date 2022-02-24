from django.forms import DateTimeInput, TimeInput


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'

class XDSoftTimePickerInput(TimeInput):
    template_name = 'widgets/xdsoft_timepicker.html'