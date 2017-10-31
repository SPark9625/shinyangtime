from django import forms

class ProposalForm(forms.Form):
	title = forms.CharField()
	text = forms.CharField(max_length=300, widget=forms.Textarea)