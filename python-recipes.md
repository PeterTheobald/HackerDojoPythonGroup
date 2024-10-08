## Python recipes for common workflows

First install tool: pyenv https://github.com/pyenv/pyenv?tab=readme-ov-file#installation

### Start a new project:
Make repo at github.com and copy the CODE ssh URL
On your local machine open a terminal:
```
% cd ~/Documents # or wherever you keep projects
% git clone <paste repo_URL> # makes a new folder and downloads repo into it
% ls
% cd <project_dir>
% pyenv local 3.12 # set the Python version for this project
```
If Python 3.12 isn't installed, `pyenv install 3.12` will do it  
create a virtual environment where all packages will be installed:
```
% python -m venv <projname_venv> # pick a good but short name
% source <projname_venv>/bin/activate # activate the environment
% pip install -r requirements.txt
```
Ready to work on project!

### Enter an existing project:
```
% cd ~/Documents/<proj_dir>
% source <projname_venv>/bin/activate
```
Read to work on project!

### If a project uses Jupyter Notebooks:
```
% cd ~/Documents/<proj_dir>
% source <projname_venv>/bin/activate
#    Add "notebook" to requirements.txt
% pip install -r requirements.txt
% jupyter notebook # start notebook
```

### Basic GIT commands for working on projects:
Create feature branch on github.com
```
% git checkout <branch>
#    Edit files
% git status
% git add . # or git add <file>
% git commit -m "description" 
% git push origin # send to github.com
```
Go to repo on github.com and create PULL REQUEST
(If you are the only one working on a project you could skip the feature branch and use main for everything)

