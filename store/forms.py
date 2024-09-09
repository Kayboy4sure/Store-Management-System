from django import forms
from .models import Stock


# class XZ_DateInput(forms.DateInput):
#      input_type = "date"
#      def __init__(self, **kwargs):
#           kwargs["format"] = "%d/%m/%Y"
#           super().__init__(**kwargs)

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']
     
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category


    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        for instance in Stock.objects.all():
            if instance.item_name == item_name:
                raise forms.ValidationError(item_name + ' is already created')
        return item_name

class StockSearchForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget= forms.DateInput(attrs={"type":"date"}))
    end_date = forms.DateField(required=False, widget= forms.DateInput(attrs={"type":"date"}))
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'export_to_CSV','start_date','end_date']
        labels = {
            'category': 'category', 
            'item_name': 'item_name', 
            'export_to_CSV': 'export_to_CSV', 
            'start_date': 'start_date',
        }

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_by']
          
class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']