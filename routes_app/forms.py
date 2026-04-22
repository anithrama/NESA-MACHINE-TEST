from django import forms

from .models import AirportRoute

TREE_NODES = {
    "A", "B", "C", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T"
}


class AirportRouteForm(forms.ModelForm):
    class Meta:
        model = AirportRoute
        fields = ["airport_code", "position", "direction", "duration"]
        widgets = {
            "airport_code": forms.TextInput(attrs={"placeholder": "A, B, C...", "maxlength": 1}),
            "position": forms.NumberInput(attrs={"placeholder": "Position index (e.g. 1)"}),
            "direction": forms.Select(choices=AirportRoute.DIRECTION_CHOICES),
            "duration": forms.NumberInput(attrs={"placeholder": "Duration in minutes"}),
        }

    def clean_airport_code(self):
        code = self.cleaned_data["airport_code"].strip().upper()
        if code in TREE_NODES:
            raise forms.ValidationError("This node already exists.")
        if AirportRoute.objects.filter(airport_code=code).exists():
            raise forms.ValidationError("This node already exists.")
        return code


class NodeSearchForm(forms.Form):
    start = forms.CharField(max_length=1)
    target = forms.CharField(max_length=1)
    direction = forms.ChoiceField(choices=(("left", "Left"), ("right", "Right")))

    def clean_start(self):
        start = self.cleaned_data["start"].strip().upper()
        if not start.isalpha() or len(start) != 1:
            raise forms.ValidationError("Enter a valid single-letter node.")
        if start in {"I", "O"}:
            raise forms.ValidationError("This airport code is not allowed.")
        return start

    def clean_target(self):
        target = self.cleaned_data["target"].strip().upper()
        if not target.isalpha() or len(target) != 1:
            raise forms.ValidationError("Enter a valid single-letter node.")
        if target in {"I", "O"}:
            raise forms.ValidationError("This airport code is not allowed.")
        return target


class ShortestRouteForm(forms.Form):
    source = forms.CharField(max_length=1)
    destination = forms.CharField(max_length=1)

    def _clean_code(self, value, label):
        code = value.strip().upper()
        if code in {"I", "O"}:
            raise forms.ValidationError(f"{label} airport code is not allowed.")
        if code not in TREE_NODES:
            raise forms.ValidationError(f"{label} airport does not exist.")
        return code

    def clean_source(self):
        return self._clean_code(self.cleaned_data["source"], "Source")

    def clean_destination(self):
        return self._clean_code(self.cleaned_data["destination"], "Destination")

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")
        destination = cleaned_data.get("destination")
        if source and destination and source == destination:
            raise forms.ValidationError("Source and destination must be different airports.")
        return cleaned_data
