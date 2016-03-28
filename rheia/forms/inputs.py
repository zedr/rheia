from bootstrap3_datepicker.widgets import DatePickerInput as _DatePickerInput


class DatePickerInput(_DatePickerInput):
    @property
    def media(self):
        # TODO: find a better way to do the override...
        media = super(DatePickerInput, self).media
        media._css = {'all': ("css/datepicker3.css",)}
        media._js = ("js/lib/bootstrap-datepicker.js",)
        return media


__all__ = (DatePickerInput.__name__, )
