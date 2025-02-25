import os
import json
import zipfile
import tempfile

def save_zip(data, filename):

	# Create a ZIP file
	zip_file = tempfile.mkstemp(prefix=filename, suffix='.zip')
	zip_file_name = os.path.abspath(zip_file[1])
	zipf = zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED)

	# Create the data
	json_data = json.dumps(data, indent=4)
	json_file_name = filename + '.json'

	# Add the JSON file to the ZIP
	zipf.writestr(json_file_name, json_data)
	zipf.close()

	return zip_file_name
