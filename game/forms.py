from django import forms
from django.forms.widgets import NumberInput
from game.fields import ListTextWidget


class RangeInput(NumberInput):
    input_type = "range"


ETHNICITY_CHOICES = (
    'Black or African American', 'Asian', 'White or European', 'Hispanic or Latino', 'Mixed', 'Prefer not to disclose',
    'Other (please specify)')
GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('NA', 'Prefer not to disclose'),
                  ('Other', 'Other (please specify)')]
GENDER_CHOICES_LIST = ('Male', 'Female', 'Prefer not to disclose', 'Other (please specify)')
EDU_CHOICES = ('High School or Equivalent', 'Vocational/Technical School (2 year)', 'Some College',
               'College Graduate (4 year)', 'Masters Degree (MS)', 'Doctoral Degree (PhD)',
               'Professional Degree (MD, JD, etc.)', 'Other (please specify)')


class DemographicsForm(forms.Form):
    worker_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    ethnicity = forms.CharField(widget=ListTextWidget(data_list=ETHNICITY_CHOICES, name='ethnicity'), required=True)
    gender = forms.CharField(label='Gender', widget=ListTextWidget(data_list=GENDER_CHOICES_LIST, name='gender'),
                             required=True)

    age = forms.IntegerField(
        label="What is your age (in years)?",
        min_value=1,
        max_value=150, required=True)

    edu = forms.CharField(label='Please indicate the highest level of education completed',
                          widget=ListTextWidget(data_list=EDU_CHOICES, name='edu'),
                          required=True)

    game_exp = forms.IntegerField(widget=RangeInput,
                                  label="How much experience do you have with playing computer games? [1=None at all, 100=A lot]",
                                  min_value=1,
                                  max_value=100, required=True)

    def get_fields(self):
        return {'worker_id': self.worker_id,
                'ethnicity': self.ethnicity,
                'gender': self.gender,
                'age': self.age,
                'edu': self.edu,
                'game_exp': self.game_exp
                }

class EnterWorkerIdForm(forms.Form):
    worker_id = forms.CharField(label='Your Worker ID', required=True)

    def get_fields(self):
        return {'worker_id': self.worker_id}

class EnterCompletionCodeForm(forms.Form):
    completion_code = forms.CharField(label='Your Completion Code', required=True)

    def get_fields(self):
        return {'completion_code': self.completion_code}