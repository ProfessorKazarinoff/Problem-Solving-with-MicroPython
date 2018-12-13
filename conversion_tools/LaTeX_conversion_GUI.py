# -*- coding: utf-8 -*-
"""
LaTex_Converion_GUI.py

This script produces a GUI window that converts a directory of Jupyter notebooks into one big LaTeX document
Created on Thurs Dec 13 10:26:57 2018

@author: peter.kazarinoff
"""

from pathlib import Path

from gooey import Gooey, GooeyParser

from converter_functions import (
    file_to_nbnode,
    export_nbnode,

)


@Gooey(dump_build_config=True, program_name="Jupter Notebook Conversion Tool (convert directory of notebooks)")
def main():
    desc = "A Python GUI App to convert a directory of Jupyter Notebooks into one big LaTeX document"
    template_select_help_msg = "Select a template (.tplx-file) to apply"

    my_parser = GooeyParser(description=desc)

    my_parser.add_argument(
        "Input_Directory", help="Select a directory to filled with notebooks", widget="DirChooser"
    )
    my_parser.add_argument(
        "Template_File", help=template_select_help_msg, widget="FileChooser"
    )

    my_parser.add_argument(
        "Output_Directory", help="Directory to save output", widget="DirChooser"
    )

    my_parser.add_argument(
        "Output_FileName", help="File Name for Output file", widget="DirChooser"
    )

    args = my_parser.parse_args()
    # get all of the .ipynb file paths
    nb_filepath_list = [file for file in (Path(args.Input_Directory)).glob("**/*.ipynb")]

    # construct template file path
    template_file_Path = Path(args.Template_File)

    for f in nb_filepath_list:
        print('Converting Notebook:')
        print('infile Path')
        print(f)
        nbnode = file_to_nbnode(f)
        print('Out file Path')
        outfile_Path = Path(f.parent, Path(f.stem))
        print(outfile_Path)

        # create lab_title.tplx file where the lab title from the input notebook file name is derived
        lab_title_str = extract_lab_title(f)
        create_lab_title_template(lab_title_str, "lab_title.tplx")
        export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)



    # nbnode = file_to_nbnode(args.Notebook_to_Convert)
    # # construct output .tex file file path
    # outfile_Path = Path(args.Output_Directory, Path(args.Notebook_to_Convert).stem)
    #
    # # construct template file path
    # template_file_Path = Path(args.Template_File)
    #
    # # create lab_title.tplx file where the lab title from the input notebook file name is derived
    # lab_title_str = extract_lab_title(args.Notebook_to_Convert)
    # create_lab_title_template(lab_title_str, "lab_title.tplx")
    #
    # # export notebook node object to .tex file
    # export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)
    #
    # print(f"input file \n {args.Notebook_to_Convert}")
    # print()
    # print(f"output directory \n {args.Output_Directory}")
    # print()
    # print(f"template file \n {args.Template_File}")


if __name__ == "__main__":
    main()
