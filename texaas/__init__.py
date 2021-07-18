import os
import sys
import toml

from flask import Flask
from flask import jsonify

app = Flask(__name__)
BASE_PATH = os.path.abspath('..')
cfg = None

@app.route('/health')
def health():
	return jsonify(success=True)

@app.route('/template/<string:template_name>')
def create_template(template_name: str):
	
	...

class Config:
	DEFAULT_FILENAME: str = "config.toml"
	DEFAULT_PATH: str = f"{BASE_PATH}{os.sep}{DEFAULT_FILENAME}"

	GENERAL_TABLE: str = "general"

	def __init__(self, toml_str: str):
		"""TODO: Throws KeyError"""
		d = toml.loads(toml_str)
		self.general = d[self.GENERAL_TABLE]
		del d[self.GENERAL_TABLE]

		# We ignore simple values
		self.files = {k: v for k, v in d.items() if type(v) is dict}

	@classmethod
	def from_filename(cls, path_to_toml: str = DEFAULT_PATH):
		"""TODO Throws FileNotFoundError, toml.decoder.DecodeError"""
		if path_to_toml[-5:].lower() != ".toml":
			path_to_toml += ".toml"
		with open(path_to_toml, 'r') as fp:
			t = fp.read()
		return cls(t)

def main():
	try:
		cfg = Config.from_filename()
	except FileNotFoundError:
		print("config.toml NOT FOUND! Quitting...", file=sys.stderr)
	app.run()

if __name__ == '__main__':
	main()