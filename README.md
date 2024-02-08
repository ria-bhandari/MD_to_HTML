# Markdown to HTML conversion

This project performs markdown to HTML conversion and consists of two main files: `manual_run.py` and `githook_run.py`.

In `manual_run.py`, the process is as follows:
1. Find modified markdown files
    - Identify markdown files in the repository that have been modified since the last commit or are not in the repository
    - Filter the files based on if they are in the whitelist of the blacklist
    - Make sure that the selected files are "younger" than their corresponding HTML files

2. Generate the corresponding HTML files
    - Create HTML files in the same location with the same names as step 1

3. Add the generated file to the Git repository
    - The newly generated HTML files are integrated using `git add`

In `githook_run.py`, the process is as follows:
Step 1 and step 2 of the manual run are the same, followed by adding the files to the current commit that is being generated.

## Table of Contents
[Whitelists and Blacklists](https://github.com/ria-bhandari/MD_to_HTML?tab=readme-ov-file#whitelists-and-blacklists)

[Usage](https://github.com/ria-bhandari/MD_to_HTML?tab=readme-ov-file#usage)

[Technologies Used](https://github.com/ria-bhandari/MD_to_HTML?tab=readme-ov-file#technologies-used)

## Whitelists and Blacklists

In order to determine whether to convert a markdown file to HTML, they are checked against the following criteria involving whitelists and blacklists: 

- Neither a white list or black list is supplied. In this case we would match all markdown files within the repository.
- Only a black list is given. We match all markdown files within the repository that don't match against the black list.
- Only a white list is given. We match all markdown files within the repository that match against the white list.
- Both a white and black list are given. We match all markdown files that don't match against the black list unless they are on the white list

## Usage

To use this repository, 

## Technologies Used



