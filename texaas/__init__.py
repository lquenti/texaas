import re
import os
import shlex
import subprocess
import sys
import toml

from typing import Dict, List

"""
TODOs:
- Extraroute for all templates
- Type everything (once the pipeline is configured)
"""

BASE_PATH = os.path.abspath('..')



def template(template_name: str):
	filename = template_name + '.tex'
	if template_name not in cfg.FILES:
		# TODO: Error Handling
		raise Exception()

	# TODO: Probably better to do config sanity checks when init
	# TODO: If a POST-Parameter does not exist, return a helpful message
	#vars = {v: request.form[v] for v in cfg.FILES[template_name]['variables']}
	tex = create_tex(filename, vars)

	path_to_pdf = compile_latex(filename, tex)


def input_regex(var_name):
	return re.compile(r"\\input\s*{\s*(?:" + var_name + r")}", re.MULTILINE)

def compile_latex(filename: str, tex: str):
	"""TODO: Throws subprocess.CalledProcessError"""
	full_path = f"{cfg.TEMPLATE_PATH}{os.sep}{filename}"
	cmd: List[str] = cfg.TEX_CMD + [full_path]
	# TODO: Create me first since my tex is replaced lol
	subprocess.run(cmd, check=True, cwd=cfg.general['tmp_dir'])

def create_tex(template_name: str, vars: Dict[str, str]):
	p = f"{cfg.TEMPLATE_PATH}{os.sep}{template_name}"
	with open(p, 'r') as fp:
		s = fp.read()
	for v, replacement in vars.items():
		pattern = input_regex(v)
		s, n = re.subn(pattern, replacement, s)
		if n == 0:
			# TODO: Error Handling, Pattern did not match
			raise Exception()
	return s


class Config:
	DEFAULT_FILENAME: str = "config.toml"
	DEFAULT_PATH: str = f"{BASE_PATH}{os.sep}{DEFAULT_FILENAME}"

	GENERAL_TABLE: str = "general"

	# TODO: Actually parse other stuff
	# TODO: Make everything read only

	def __init__(self, toml_str: str):
		"""TODO: Throws KeyError"""
		d = toml.loads(toml_str)
		self.general = d[self.GENERAL_TABLE]
		del d[self.GENERAL_TABLE]

		# We ignore simple values
		self.FILES = {k: v for k, v in d.items() if type(v) is dict}

		self.TEMPLATE_PATH = BASE_PATH + self.general['template_path']

		tex_cmd = f"{self.general['tex_compiler']} {self.general['tex_args']}"
		self.TEX_CMD: List[str] = shlex.split(tex_cmd)

		os.mkdir(self.general['tmp_dir'], 0o755)

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
		global cfg
	except FileNotFoundError:
		print("config.toml NOT FOUND! Quitting...", file=sys.stderr)


if __name__ == '__main__':
	main()
