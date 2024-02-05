# This file checks whether the markdown file is in the blacklist or in the whitelist

import os
import pypandoc 
import subprocess
from typing import Set
from pathlib import Path
import fnmatch

def check_location_file(file_name: str, black_list: Set[str], white_list: Set[str]) -> bool:
    """
    This function takes the file name and two sets: black list and white list. It checks if the file name must be included
    based on the black and white lists. The function returns True if the file should be included. 
    """
    if not black_list and not white_list:
        return True
    elif white_list and not black_list:  # only white list provided
        return file_name in white_list
    elif black_list and not white_list:  # black list only
        return file_name not in black_list
    else:  # both black and white list
        return file_name not in black_list or file_name in white_list
