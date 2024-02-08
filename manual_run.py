import os
import subprocess
from datetime import datetime, timedelta
import fnmatch
import pathlib
from typing import Iterable


def find_modified_md_files() -> list[str]:
    '''
    This function finds any modified markdown files since the last commit
    '''

    # Run git commands to find modified files 
    git_cmd = ['git', 'diff', '--name-only', 'HEAD']
    ret = subprocess.run(git_cmd, capture_output=True, text=True)
    return [file_path for file_path in ret.stdout.splitlines() if file_path.endswith('.md')]


def find_md_files_not_in_repo() -> list[str]:  # list of Path
    '''
    This function finds markdown files that are not in the repository
    '''

    git_cmd = ['git', 'ls-files', '--others', '--exclude-standard']
    ret = subprocess.run(git_cmd, capture_output=True, test=True)
    return [file_path for file_path in ret.stdout.splitlines() if file_path.endswith('.md')]


def generate_html_files(md_files: list[str]) -> None:
    '''
    This function generates HTML files from the filtered markdown files. It calls a function
    from another python code file in this project (is_valid) to check whether 
    the markdown file is in the whitelist or the blacklist
    '''
    for md_file in md_files:
        html_file = md_file.replace('.md', '.html')

        # Use the Pandoc library for conversion
        pandoc_cmd = ['pandoc', md_file, '-o', html_file]
        subprocess.run(pandoc_cmd)


def add_files_to_git(files: list[str]) -> None:
    '''
    This function uses the git add command to add the files to git
    '''
    git_add = ['git', 'add'] + files
    subprocess.run(git_add)


# git rev-parse --show-toplevel can be used to get the absolute path to the current repo
def get_markdown_files(root_of_git_repo: pathlib.Path, white_list, black_list) -> list[pathlib.Path]:
    markdown_files = (file for file in root_of_git_repo.glob('**.md') if file.is_file())
    return list(filter(
        lambda markdown_file: is_approved_file(markdown_file, white_list, black_list), markdown_files))


def is_approved_file(file_name: os.PathLike, white_list: list[str], black_list: list[str]) -> bool:
    """
    Description of function
    :param file_name:
    :param white_list:
    :param black_list:
    :return:
    """
    # if fnmatch doesn't like paths, then convert to a string
    return (any((fnmatch.fnmatch(file_name, approved_pattern) for approved_pattern in white_list))
            or
            all((not fnmatch.fnmatch(file_name, disallowed_pattern) for disallowed_pattern in black_list))
            )


if __name__ == "__main__":
    files_to_process = find_modified_md_files() + find_md_files_not_in_repo()
    generate_html_files(files_to_process)
    if 'pre-commit' in os.environ.get('GET_HOOK_NAME', ''):
        add_files_to_git([file.replace('.md', '.html') for file in files_to_process])
