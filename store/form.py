from django import forms
from . models import Contact


class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Name", widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Quý danh của bạn',
        'required' : 'required',
    }))

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Email của bạn',
        'required' : 'required',
    }))

    subject = forms.CharField(max_length=50, label="Subject", widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Tiêu đề',
        'required' : 'required',
    }))

    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Nhập lời nhắn của bạn',
        'rows' : '8',
        'required' : 'required',
    }))

    class Meta:
        model = Contact
        fields = '__all__'