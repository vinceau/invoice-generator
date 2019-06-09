#!/usr/bin/env python3

"""Generates LaTeX, markdown, and plaintext copies of my cv."""

import argparse
import jinja2
import os
import re
import shutil
import yaml

parser = argparse.ArgumentParser(description='Render a LaTex Template with variables.')

parser.add_argument('-b','--build-dir', help='Specify the build directory', required=False, default='./.build/' )
parser.add_argument('-i','--in', help='Invoice File', required=False, default='./invoice.yaml' )
parser.add_argument('-v','--var', help='Variables File', required=False, default='./variables.yaml' )
parser.add_argument('-o','--out', help='Output File', required=False, default='./output.pdf' )
parser.add_argument('-t','--template', help='Template File', required=False, default='./template.tex')
args = vars(parser.parse_args())


project = "./"
in_file = args['in']
var_file = args['var']
output_file = args['out']
build_d = args['build_dir']
template_file = args['template']
out_file = os.path.join(build_d, "renderer_template")


current_object = None
current_content = ""
latex_formated_variables = ""


def load_yaml(file_name):
    with open(file_name, 'r') as stream:
        return yaml.safe_load(stream)

"""
with open(in_file) as f:
    content = f.read()
    keys = re.findall(r"%(.+):", content)
    values = re. findall(r":\s*([\w\W]+?)\s*(?:%|$)", content)
"""

options = {
    "variables": load_yaml(var_file),
    "invoice": load_yaml(in_file),
}

latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('/')),
	keep_trailing_newline=True
)
template = latex_jinja_env.get_template(os.path.realpath(template_file))
######

renderer_template = template.render(**options)

if not os.path.exists(build_d):  # create the build directory if not exisiting
    os.makedirs(build_d)

with open(out_file+".tex", "w") as f:  # saves tex_code to outpout file
    f.write(renderer_template)


os.system('pdflatex -output-directory {} {}'.format(os.path.realpath(build_d), os.path.realpath(out_file + '.tex')))

final = os.path.realpath(output_file)
shutil.copy2(out_file+".pdf", final)

print("Generated: " + final)
