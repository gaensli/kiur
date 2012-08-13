#import magic
import re
import warnings

from django.utils import timezone
from django.contrib.auth.models import User

from libmods.models import Footprint, Component
from libmods.forms import UploadFormOne, UploadFormLib, UploadFormDcm, UploadFormWrl, UploadFormMod

MAX_UPLOAD_SIZE = 2621440 # 2.5MB

def parse_uploaded_file(request):
	''' Determines the type of file an upload is and calls the right 
	    function to save the models and returns a context dictionary 
			                                                             '''
	f = request.FILES["lib_mod_dcm_or_wrl"]

	if f.size > MAX_UPLOAD_SIZE:
		raise ParseFailed("File too Large. The maximum file size allowed is %.1f MB." % (MAX_UPLOAD_SIZE/1048576.0))

	first_line = f.readline()
	parsed = {}

	#for chunk in f.chunks():
	#	break
	#if (magic.Magic(mime=True).from_buffer(chunk) != "text/plain"):
	#	raise ParseFailed("File is not text/plain type.")

	if "EESchema-LIBRARY" in first_line:
		parsed["upload_form"] = UploadFormLib()

		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter("always")
			parsed["saved"], parsed["db_duplicates"] = ParseLib(f, first_line, request)
			parsed["up_duplicates"] = filter(lambda i: issubclass(i.category, ProblemInUp), w)


	elif "EESchema-DOCLIB" in first_line:
		form = UploadFormDcm(initial={"dcm":f})
	elif "PCBNEW-LibModule-V1" in first_line:
		form = UploadFormMod(initial={"mod":f})
	elif "VRML" in first_line:
		form = UploadFormWrl(initial={"wrl":f})
	else:
		raise ParseFailed("Not a valid KiCAD file.")

	return parsed


def ParseLib(f, first_line, request):
	''' 
	Parser for .lib file. Will save and return a list of saved components
	and a list of components whos name clashes with one in the 
	database. Will raise a warning if there are duplicate names or other
	problems within an uploaded .lib itself.
	                                                               '''
	try:
		ki_version = re.match(r".*(\d\.\d)", first_line).group(1).split(".")
	except:
		raise ParseFailed("File identified as EESchema Library but cannot determine version.")
	lib_open = False
	components_text = {}
	duplicates = []
	saved = []
	for line in f:
		if line[0] == '#':
			pass
		elif line[:3] == "DEF":
			if lib_open:
				components_text[name] += "ENDDEF\n"
				warnings.warn("The component definition for %s is not closed properly. There may be a problem parsing this component." % name, ProblemInUp)
				lib_open = False
			try:
				name = re.match(r"DEF ([\/\-_\w]+) ", line).group(1)
			except:
				warnings.warn("Problem determining name of definition beginning with:\n\t" + line, ProblemInUp)
			else:
				if name in components_text:
					warnings.warn ("Duplicate component %s in uploaded .lib" % name, ProblemInUp)
				components_text[name] =  line
				lib_open = True
		elif (line[:6] == "ENDDEF") and lib_open:
			components_text[name] += line
			lib_open = False
		elif lib_open:
			components_text[name] += line

	if lib_open:
			components_text[name] += "ENDDEF\n"
			warnings.warn("A component definition for %s is not closed properly. There may be a problem parsing this component." % name, ProblemInUp)
	
	for name, text in components_text.iteritems():
		print name
		try:
			lib = Component.objects.get(name=name)
		except Component.DoesNotExist:
			lib = Component()
			lib.name = name
			lib.description = ""
			lib.submitter = request.user
			lib.maintainer = request.user
			lib.revision = 1
			lib.votes = 0
			lib.date_added = timezone.now()
			lib.ki_version = ki_version
			lib.ki_text = text 
			lib.save()
			saved.append(lib)
		except Component.MultipleObjectsReturned:
			warnings.warn("There are already multiple components with the name %s. This really shouldn't have happend. Please contact the administrator." % name, ProblemInUp)
			duplicates.append({
				 "component" : lib
				,"new_text": text 
			})
		else:
				duplicates.append({
					 "component" : lib
					,"new_text": text 
				})
	return saved, duplicates

class ProblemInUp(UserWarning):
	pass

class ParseFailed(Exception):
	def __init__(self, msg=None):
		if msg is None:
			msg = "Parsing of uploaded file failed."
		super(ParseFailed, self).__init__(msg)
