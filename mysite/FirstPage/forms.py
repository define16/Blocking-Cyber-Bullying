from django import forms


class CommentForm(forms.Form):
    id = forms.CharField(label='demo-id')
    comment = forms.CharField(label='demo-comment')
    # print("form : ", id, comment)

class reportForm(forms.Form):
    reportid = forms.CharField(label='reportid')

class reportFormO(forms.Form):
    reportid1 = forms.CharField(label='reportid1')

class nobullyingForm(forms.Form):
    bullying_id = forms.CharField(label='bullying_id')