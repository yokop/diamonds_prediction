from django.forms import ModelForm
from .models import Diamond,Diamond_predicted

class Diamond_prediction_form(ModelForm):
    class Meta:
        model = Diamond
        fields = ['carat','cut','color','clarity','depth','table','x','y','z']


class Diamond_prediction_feedback_form(ModelForm):
    class Meta:
        model = Diamond_predicted
        fields = ['real_price_feedback','price_feedback','imported_to_dataset']
        labels = {
                'real_price_feedback': 'What is the real price',
                'price_feedback': 'Give feadback in ypur words',
                'imported_to_dataset': 'Add this case to dataset'
                }