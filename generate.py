#!/usr/bin/env python3

"""Generates LaTeX from templates"""

import argparse
import jinja2
import os
import re
import shutil
import yaml
import uuid

class Loader(yaml.SafeLoader):
    """Loader is a custom loader that supports !import and !include statements
    """

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)
        Loader.add_constructor('!import', Loader.include)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


def pdflatex(output_dir, input_tex, output_pdf):
    os.system('pdflatex -output-directory {} {}'.format(output_dir, input_tex))
    input_name = os.path.splitext(input_tex)[0]
    shutil.copy2(input_name+".pdf", output_pdf)


def generate_latex(template_file, options, output_file):
    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('/')),
        keep_trailing_newline=True
    )
    template = latex_jinja_env.get_template(template_file)
    renderer_template = template.render(**options)

    # create the build directory if it does not exist
    build_d = os.path.dirname(output_file)
    if not os.path.exists(build_d):
        os.makedirs(build_d)

    # write the tex output to file
    with open(output_file, "w") as f:
        f.write(renderer_template)


def process_file(in_file, build_dir, template_file):
    unique_str = uuid.uuid4().hex[:6]
    build_d = os.path.join(build_dir, unique_str)
    out_file = os.path.join(build_d, "renderer_template")
    tex_file = os.path.realpath(out_file) + ".tex"

    options = yaml.load(in_file, Loader)
    full_basename = os.path.splitext(in_file.name)[0]
    output_file = full_basename + ".pdf"

    # Check if the file already exists
    if os.path.isfile(output_file):
        new_output_file = "{}_{}.pdf".format(full_basename, unique_str)
        print("{} already exists. Saving to: {}".format(output_file, new_output_file))
        output_file = new_output_file

    # Generate the final latex file
    generate_latex(os.path.realpath(template_file), options, tex_file)
    # Convert the latex file to PDF
    pdflatex(os.path.realpath(build_d), tex_file, output_file)

    return output_file


def main(args):
    for in_file in args['file']:
        output_file = process_file(in_file, args['build_dir'], args['template'])
        print("Generated: " + output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Render a LaTex Template with variables.')

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    parser.add_argument('-b', '--build-dir', help='Specify the build directory',
                        required=False, default='./.build/')
    parser.add_argument('-t', '--template', help='Template File',
                        required=False, default='./template.tex')
    args = vars(parser.parse_args())

    main(args)
