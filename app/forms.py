from django import forms


class MailingForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label="Сообщение для рассылки")
    buttons = forms.CharField(widget=forms.TextInput, label="Кнопки (опционально)", required=False)
