from django import forms

class frmComentario(forms.Form):
    autor = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Ingresa tu nombre '
            })
    )

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'Deja tu comentario '
            })
    )