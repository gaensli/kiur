from django import forms

class UploadFormOne(forms.Form):
	lib_mod_dcm_or_wrl = forms.FileField()

class UploadFormLib(forms.Form):
	lib = forms.CharField()
	dcm = forms.FileField()

class UploadFormDcm(forms.Form):
	lib = forms.FileField()
	dcm = forms.CharField()

class UploadFormMod(forms.Form):
	mod = forms.CharField()
	wrl = forms.FileField()

class UploadFormWrl(forms.Form):
	mod = forms.FileField()
	dcm = forms.CharField()
