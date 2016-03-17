from django.forms import IntegerField, widgets
from django.core.exceptions import ValidationError

from rheia.parsers.time import parse_time


class DurationField(IntegerField):
    """A field that parses time-strings representing the duration of a task.
    """
    widget = widgets.TextInput

    def clean(self, value):
        """Clean the field by parsing it.
        """
        # Check for null.
        if value is None:
            return None
        else:
            try:
                return parse_time(value)
            except ValueError as exc:
                raise ValidationError(str(exc))
