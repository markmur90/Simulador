from django import forms
from .models import (
    Debtor, DebtorAccount, Creditor, CreditorAccount,
    CreditorAgent, ClientID, Kid, PaymentIdentification,
    Transfer, PostalAddress
)


class DebtorForm(forms.ModelForm):
    mobile_phone_number = forms.CharField(max_length=20, required=False)
    postal_address_country = forms.CharField(max_length=2)
    postal_address_street = forms.CharField(max_length=70)
    postal_address_city = forms.CharField(max_length=70)

    class Meta:
        model = Debtor
        fields = [
            'name', 'mobile_phone_number', 'customer_id',
            'postal_address_country', 'postal_address_street',
            'postal_address_city'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.address:
            addr = self.instance.address
            self.fields['postal_address_country'].initial = addr.country
            self.fields['postal_address_street'].initial = addr.street
            self.fields['postal_address_city'].initial = addr.city

    def save(self, commit=True):
        debtor = super().save(commit=False)
        addr_data = {
            'country': self.cleaned_data['postal_address_country'],
            'street': self.cleaned_data['postal_address_street'],
            'city': self.cleaned_data['postal_address_city'],
        }
        if commit:
            if debtor.address_id:
                for k, v in addr_data.items():
                    setattr(debtor.address, k, v)
                debtor.address.save()
            else:
                debtor.address = PostalAddress.objects.create(**addr_data)
            debtor.save()
        return debtor


class DebtorAccountForm(forms.ModelForm):
    class Meta:
        model = DebtorAccount
        fields = ['debtor', 'iban', 'currency']


class CreditorForm(forms.ModelForm):
    postal_address_country = forms.CharField(max_length=2)
    postal_address_street = forms.CharField(max_length=70)
    postal_address_city = forms.CharField(max_length=70)

    class Meta:
        model = Creditor
        fields = ['name', 'postal_address_country', 'postal_address_street', 'postal_address_city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.address:
            addr = self.instance.address
            self.fields['postal_address_country'].initial = addr.country
            self.fields['postal_address_street'].initial = addr.street
            self.fields['postal_address_city'].initial = addr.city

    def save(self, commit=True):
        creditor = super().save(commit=False)
        addr_data = {
            'country': self.cleaned_data['postal_address_country'],
            'street': self.cleaned_data['postal_address_street'],
            'city': self.cleaned_data['postal_address_city'],
        }
        if commit:
            if creditor.address_id:
                for k, v in addr_data.items():
                    setattr(creditor.address, k, v)
                creditor.address.save()
            else:
                creditor.address = PostalAddress.objects.create(**addr_data)
            creditor.save()
        return creditor


class CreditorAccountForm(forms.ModelForm):
    class Meta:
        model = CreditorAccount
        fields = ['creditor', 'iban', 'currency']


class CreditorAgentForm(forms.ModelForm):
    class Meta:
        model = CreditorAgent
        fields = ['bic', 'financial_institution_id', 'other_information']


class ClientIDForm(forms.ModelForm):
    class Meta:
        model = ClientID
        fields = ['codigo', 'client_id']


class KidForm(forms.ModelForm):
    class Meta:
        model = Kid
        fields = ['codigo', 'kid']


class PaymentIdentificationForm(forms.ModelForm):
    class Meta:
        model = PaymentIdentification
        fields = ['end_to_end_id', 'instruction_id']


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        exclude = ['created_at', 'updated_at', 'auth_id']