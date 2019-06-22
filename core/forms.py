from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import Company

import logging
from django.conf import settings

lgr = logging.getLogger(__name__)



class CompanyForm(forms.ModelForm):
    # link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Invite or .me Link'}))
    # accounts = forms.ModelMultipleChoiceField(
    #     queryset=Account.objects.filter(status=Account.READY),
    #     required=True
    # )

    class Meta:
        model = Company
        exclude = ['freelancer','paid' ]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        # self.fields["accounts"].initial = (
        #     Account.objects.free().values_list(
        #         'id', flat=True
        #     )
        # )

    def clean2(self):
        super(CompanyForm, self).clean()
        lgr.info('clean SampleModelForm')

        # access cleaned data
        account_email = self.cleaned_data.get("email")

        valid = False

        if not valid:

            raise forms.ValidationError("Invalid Account Credentials")
        else:
            lgr.info('credentials valid')
