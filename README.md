# Markdown to HTML conversion

Manual Run
Find all markdown files in the repo that have been modified since the last commit (or are not in the repo) that are either in the whitelist or not in the blacklist and are younger than their corresponding html 
Generate corresponding html files in the same locations with same same names as found in step 1
Add the files the generated files to the repo (git add)
GitHook Run
Steps one and two are the same
Add the files to the current commit that is being generated

