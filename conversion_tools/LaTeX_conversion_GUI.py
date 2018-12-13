# -*- coding: utf-8 -*-
"""
LaTex_Converion_GUI.py

This script produces a GUI window that converts a directory of Jupyter notebooks into one big LaTeX document
Created on Thurs Dec 13 10:26:57 2018

@author: peter.kazarinoff
"""

from pathlib import Path

from gooey import Gooey, GooeyParser

from convert_functions import copy_all_images_to_dir
from convert_functions import (
    file_to_nbnode,
    export_nbnode,

)


@Gooey(dump_build_config=True, program_name="Jupter Notebook Conversion Tool")
def main():
    desc = "A Python GUI App to convert a directory of Jupyter Notebooks into one big LaTeX document"

    my_parser = GooeyParser(description=desc)

    my_parser.add_argument(
        "Input_Directory", help="Select a directory to filled with notebooks", widget="DirChooser"
    )
    my_parser.add_argument(
        "Template_File", help="Select a template (.tplx-file) to apply", widget="FileChooser"
    )

    my_parser.add_argument(
        "Output_Directory", help="Directory to save output", widget="DirChooser"
    )

    my_parser.add_argument(
        "Output_FileName", help="Output file name (no .tex extension)",
    )

    ## parse the arguments
    args = my_parser.parse_args()

    ## Construct all the file paths

    # construct input directory file path
    input_dir_Path = Path(args.Input_Directory)
    print(f'Input directory: {input_dir_Path}')

    # construct template file path
    template_file_Path = Path(args.Template_File)
    print(f'Template file path: {template_file_Path}')

    # construct output directory path
    output_dir_Path = Path(args.Output_Directory)
    print(f'Output directory: {output_dir_Path}')

    outfile_name = args.Output_FileName
    print(f'Output file name: {outfile_name}')

    print(f'Copying images from: {input_dir_Path} \n into: {output_dir_Path}')
    copy_all_images_to_dir(input_dir_Path, output_dir_Path, 'images')

    # get all of the .ipynb file paths
    nb_filepath_list = [file for file in (Path(args.Input_Directory)).glob("**/*.ipynb")]

    #construct template file path
    template_file_Path = Path(args.Template_File)
    #
    # for f in nb_filepath_list:
    #     print('Converting Notebook:')
    #     print('infile Path')
    #     print(f)
    #     nbnode = file_to_nbnode(f)
    #     print('Out file Path')
    #     outfile_Path = Path(f.parent, Path(f.stem))
    #     print(outfile_Path)
    #
    #     # create lab_title.tplx file where the lab title from the input notebook file name is derived
    #     lab_title_str = extract_lab_title(f)
    #     create_lab_title_template(lab_title_str, "lab_title.tplx")
    #     export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)



if __name__ == "__main__":
    main()
