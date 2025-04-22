Best practices, especially for groups/teams

- import this
	- simplicity, readability
- use an IDE: Pycharm, VSCode
- style
	- PEP8,
  - ruff > flake8,pylint (linter)/black (formatter)/isort (import sorter)
  - pytest-cov
  - mypy (type hint checker). Automatic reformatting. Integrate w IDE
- type annotations, docstrings
- git source control
	- commit often, single logical change, clear commit message
- unittest, pytest
- Code reviews
- blameless port-mortems
- CI/CD github actions

GIT

Git Spaces:
Working Directory (tree) | Staging Area/Index/Cache | Local Repo (commit) | Remote Repo (upstream) | Open Source Repo

- working directory is just regular files you can edit
- Staging is a copy ready for committing (and merge conflicts)
- Local Repo and Remote Repo have "branches", usually "main" and development features, eg: "main", "test", "dev", or eg: "main", "new-ui", "migrate-to-mysql" etc.
- Remote Repo is on Github or Gitlab or private hosted hub
- Each branch in a repo has a history, a series of commits from start to current, current is called HEAD.

Example:

git clone https://github.com/PeterTheobald/GhostSolver.git
cd Ghostsolver
ls
git status # local files vs. staging area
git diff --name-only # local files vs. staging area
(edit a README.md)
git status
git add README.md
git add -A # different than git add . or git add -u or git add -a or -N r -p or -e
git rm --cached README.md
git status
git diff --name-only --staged # or --cached
git commit -m 'fixed README' # staging -> local repo

ls # current working directory
git status # changed files added to staging, and untracked files
git diff (--name-only) # changed from working to staging
git diff --staged # changed from 
git ls-files # staging
git ls-files --stage # staging with more info
git ls-files --others # work-tree untracked
git ls-files --modified # should be staging different than commit (but doesnt work)

git workflow:
- `git pull` get any remote changes from the repo (`git pull --no-rebase` to merge commits `git pull --rebase` to append local commits to remote commits)
- make changes
- `git add newfile` (or `git add -A`) (note: `git add .` `git add -u` and `git add -a` are difference, incomplete)
- `git commit -m 'desc' newfile`
- `git push`


info:
- git status -or- git diff --name-only (local files vs. staging area)
- copy local files to staging area: git add {file} or git add -A (not git add . or git add -u or git add -a)
- ...
- git diff --name-only --cached -or- --staged (staging area vs. committed) 
- copy staged files to commit: git commit -m 'desc'
- ...
- git fetch origin (or git fetch remote); git diff --name-only HEAD origin/main (commit vs. local copy of remote)
- copy committed files in HEAD to remote: git push
- ...
- git ls-files
- git branch -r {-v} (list local branches); git branch -a (list local and remote branches)
- git remote -v (list remotes)
- git ls-remote (show info I dont understand about remote)
- git remote show {remote} (list remotes or show details)
- ...
- `git fetch origin` (get remote files and apply to local copy of remote)
- `git diff HEAD origin/main` (show differences between current branch and remote)
- ...
- `git log HEAD..origin/main` (list commits in remote that are not in local)
- `git log origin/main..HEAD` (list commit in local that are not in remote)

sync my fork with original:
- `git remote add upstream <url>
- `git fetch upstream`
- `git checkout main` (or other branch like dev)
- `git merge upstream/main` (or other branch like dev)
- `git push origin main`

