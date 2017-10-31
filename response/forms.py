from django import forms

class ProposalForm(forms.Form):
	title = forms.CharField(label="제목")
	text = forms.CharField(label="내용", widget=forms.Textarea)