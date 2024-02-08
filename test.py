import os
import subprocess
from datetime import datetime, timedelta 
import fnmatch

def find_modified_md_files():
    '''
    This function finds any modified markdown files since the last commit
    '''

    modified = []

    # Run git commands to find modified files 
    git_cmd = ['git', 'diff', '--name-only', 'HEAD']
    ret = subprocess.run(git_cmd, capture_output=True, text=True)

    # Filtering the markdown files 
    for file_path in ret.stdout.splitlines():
        if file_path.endswith('.md'):
            modified.append(file_path)
    
    return modified


def find_md_files_not_in_repo():
    '''
    This function finds markdown files that are not in the repository
    '''

    not_in_repo = []

    git_cmd = ['git', 'ls-files', '--others', '--exclude-standard']
    ret = subprocess.run(git_cmd, capture_output=True, test=True)

    for file_path in ret.stdout.splitlines():
        if file_path.endswith('.md'):
            not_in_repo.append(file_path)
    
    return not_in_repo

def generate_html_files(md_files):
    '''
    This function generates HTML files from the filtered markdown files. It calls a function
    from another python code file in this project (is_valid) to check whether 
    the markdown file is in the whitelist or the blacklist
    '''
    for md_file in md_files:
        if md_file.is_valid():
            html_file = md_file.replace('.md', '.html')
        
            # Use the Pandoc library for conversion
            pandoc_cmd = ['pandoc', md_file, '-o', html_file]
            subprocess.run(pandoc_cmd)

def add_files_to_git(files):
    '''
    This function uses the git add command to add the files to git
    '''
    git_add = ['git', 'add'] + files
    subprocess.run(git_add)

def valid_file(directory_with_files, white_list, black_list):
    md_files = []

    for r, d, f in os.walk(directory_with_files):
        for file in f:
            if file.lower().endswith('.md'):
                filepath = os.path.join(r, file)

                # Check if the file is in the black list or white list
                if(white_list is None or any(fnmatch.fnmatch(file, pattern) for pattern in white_list)) and (black_list is None or not(fnmatch.fnmatch(file, pattern) for pattern in black_list)):
                    md_files.append(filepath)
    return md_files

if __name__ == "__main__":
    files_to_process = find_modified_md_files() + find_md_files_not_in_repo()
    generate_html_files(files_to_process)
    if 'pre-commit' in os.environ.get('GET_HOOK_NAME', ''):
        add_files_to_git([file.replace('.md', '.html') for file in files_to_process])