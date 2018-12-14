# convert_functions.py

"""
A set of functions to combine a directory of notebooks into a one big notebook,
then export the one big notebook to a .tex file
"""
import os
from pathlib import Path
import shutil
import re
import nbformat
from nbconvert import LatexExporter
from nbconvert.writers import FilesWriter
from nbformat import NotebookNode


from pandocfilters import toJSONFilter, applyJSONFilters, RawInline


def convert_link(key, val, fmt, meta):
    if key == "Link":
        target = val[2][0]
        # Links to other notebooks
        m = re.match(r"(\d+\-.+)\.ipynb$", target)
        if m:
            return RawInline("tex", "Chapter \\ref{sec:%s}" % m.group(1))

        # Links to sections of this or other notebooks
        m = re.match(r"(\d+\-.+\.ipynb)?#(.+)$", target)
        if m:
            # pandoc automatically makes labels for headings.
            label = m.group(2).lower()
            label = re.sub(r"[^\w-]+", "", label)  # Strip HTML entities
            return RawInline("tex", "Section \\ref{%s}" % label)

    # Other elements will be returned unchanged.


def convert_links(source):
    return applyJSONFilters([convert_link], source)


def copy_all_images_to_dir(
    notebook_dir_Path, output_dir_Path="pdf", images_dir="images"
):
    """
    a function to copy the all of the images out of notebooks/subdir/images into
    one big folder in pdf/images
    """
    nb_dir = notebook_dir_Path
    images_dir = os.path.join(os.pardir, "pdf", images_dir)
    REG_nb_dir = re.compile((r"(\d\d)-*"))

    # erase the /pdf/images dir if it exists
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)

    # create a new empt /pdf/images dir
    os.makedirs(os.path.join(output_dir_Path, "images"))

    for dir in os.listdir(nb_dir):
        if REG_nb_dir.match(dir):
            if os.path.exists(os.path.join(nb_dir, dir, "images")):
                scr_dir = os.path.join(nb_dir, dir, "images")
                dst_dir = os.path.join(output_dir_Path, images_dir)
                for f in os.listdir(scr_dir):
                    try:
                        shutil.copy(os.path.join(scr_dir, f), dst_dir)
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                        exit(1)
                    except:
                        print("Unexpected error:", sys.exc_info())
                        exit(1)


def merge_notebooks(nb_Path_list):
    """
    a function that creates a single notebook node object from a list of notebook file paths
    :param filename_lst: lst, a list of .ipynb file paths
    :return: a single notebookNode object
    """
    merged = None
    for fname in nb_Path_list:
        with open(fname, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        if merged is None:
            merged = nb
        else:
            # TODO: add an optional marker between joined notebooks
            # like an horizontal rule, for example, or some other arbitrary
            # (user specified) markdown cell)
            merged.cells.extend(nb.cells)
    if not hasattr(merged.metadata, "name"):
        merged.metadata.name = ""
    merged.metadata.name += "_merged"
    # print(nbformat.writes(merged))
    return merged


class MyLatexExporter(LatexExporter):
    def default_filters(self):
        yield from super().default_filters()
        yield ("resolve_references", convert_links)


def export_tex(combined_nb: NotebookNode, output_file_Path: Path, template_Path=None):
    """
    a function that takes in a combined notebook node oject and produces a .tex file using a specified template
    :param combined_nb: notebook node object (a .ipynb file read into a notebook node object)
    :param output_file_Path:
    :param template_file:
    :return:
    """
    resources = {}
    resources["unique_key"] = "combined"
    resources["output_files_dir"] = "combined_files"

    exporter = MyLatexExporter()
    if template_Path is not None:
        exporter.template_file = str(template_Path)
    writer = FilesWriter(build_directory=str(output_file_Path.parent))
    output, resources = exporter.from_notebook_node(combined_nb, resources)
    writer.write(output, resources, notebook_name=output_file_Path.stem)


def file_to_nbnode():
    pass


def export_nbnode():
    pass
