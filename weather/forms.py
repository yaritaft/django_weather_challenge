from django import forms

#VALUE, text in the front
service_options = (
    ('NOAA', 'noaa'),
    ('WEATHER_DOT_COM', 'weatherdotcom'),
    ('ACCUWEATHER', 'accuweather'),
)

class AxisForm(forms.Form):
    latitude = forms.DecimalField(
        required=False, label="latitude", widget=forms.NumberInput(), min_value=-180, max_value=180,
        max_digits=5, decimal_places=2,
    )
    longitude = forms.DecimalField(
        required=False, label="longitude", widget=forms.NumberInput(), min_value=-180, max_value=180,
        max_digits=5, decimal_places=2,
    )
    services = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=service_options,
    )

