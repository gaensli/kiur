from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

import magic

class ContentTypeRestrictedFileField(forms.FileField):
	"""
	Same as FileField, but you can specify:
		* content_types - list containing allowed content_types.
		Example: ['application/pdf', 'image/jpeg']
		* max_upload_size - a number indicating the maximum file
		size allowed for upload.
			2.5MB - 2621440
			5MB - 5242880
			10MB - 10485760
			20MB - 20971520
			50MB - 5242880
			100MB 104857600
			250MB - 214958080
			500MB - 429916160
	"""
	def __init__(self, *args, **kwargs):
		self.content_types = kwargs.pop("content_types")
		self.max_upload_size = kwargs.pop("max_upload_size")

		super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

		#we just want the first chunk for the header
		#should be a better way...
		for chunk in data.chunks():
			break

		content_type = magic.Magic(mime=True).from_buffer(chunk)

		try:
			if content_type in self.content_types:
				if data._size > self.max_upload_size:
					raise forms.ValidationError(_('Please keep filesize under'
												'%s. Current filesize %s')
												% (filesizeformat(self.max_upload_size), filesizeformat(data._size)))
			else:
				raise forms.ValidationError(_('Filetype not supported.'))
		except AttributeError:
			print "attr error"
			pass

		return data
