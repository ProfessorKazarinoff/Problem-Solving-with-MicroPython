# convert_functions.py

"""
A set of functions to combine a directory of notebooks into a one big notebook,
then export the one big notebook to a .tex file
"""
import os
from pathlib import Path
import shutil
import re

from pandocfilters import toJSONFilter, applyJSONFilters, RawInline

def convert_link(key, val, fmt, meta):
    if key == 'Link':
        target = val[2][0]
        # Links to other notebooks
        m = re.match(r'(\d+\-.+)\.ipynb$', target)
        if m:
            return RawInline('tex', 'Chapter \\ref{sec:%s}' % m.group(1))

        # Links to sections of this or other notebooks
        m = re.match(r'(\d+\-.+\.ipynb)?#(.+)$', target)
        if m:
            # pandoc automatically makes labels for headings.
            label = m.group(2).lower()
            label = re.sub(r'[^\w-]+', '', label)  # Strip HTML entities
            return RawInline('tex', 'Section \\ref{%s}' % label)

    # Other elements will be returned unchanged.


def convert_links(source):
    return applyJSONFilters([convert_link], source)

def copy_all_images_to_dir(input_dir_Path, output_dir_Path, output_images_dir_name='images'):
    """
    a function to copy the all of the images out of notebooks/subdir/images into
    one big folder in pdf/images
    """
    REG_nb_dir = re.compile((r'(\d\d)-*'))

    images_dir_Path = Path(input_dir_Path,output_dir_Path, output_images_dir_name)
    # erase the output images dir if it exists
    if os.path.exists(images_dir_Path):
        shutil.rmtree(images_dir_Path)
    # make the output images dir
    os.makedirs(Path(output_dir_Path, output_images_dir_name))

    for dir in os.listdir(input_dir_Path):
        if REG_nb_dir.match(dir):
            if os.path.exists(os.path.join(input_dir_Path, dir, output_images_dir_name)):
                scr_dir = Path(input_dir_Path, dir, 'images')
                dst_dir = Path(output_dir_Path, images_dir_Path)
                for f in os.listdir(scr_dir):
                    try:
                        shutil.copy(os.path.join(scr_dir, f), images_dir_Path)
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                        exit(1)
                    except:
                        print("Unexpected error:", sys.exc_info())
                        exit(1)




def file_to_nbnode():
    pass

def export_nbnode():
    pass
