from import_export import fields, resources, widgets

from import_export.widgets import ForeignKeyWidget

class CustomBooleanWidget(widgets.Widget):
    
    def __init__(self, active=None):
        self.active = active



class ValidatingForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        try:
            val = super().clean(value)
        except self.model.DoesNotExist:
            raise ValueError(f"{self.model.__name__} with value={value} does not exist")
        return val
