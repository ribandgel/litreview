# WebSite for critical reviews on books
[OpenClassRoom mission for project_9](https://openclassrooms.com/fr/paths/322/projects/837/assignment)

## Install:
  Install virtual env [here](https://virtualenvwrapper.readthedocs.io/en/latest/)
  ```
  - mkvirtualenv project_9
  - workon project_9
  - pip install -r requirements.txt
  - python manage.py runserver 8001
  ```
  
## Development utilities:
  Run autoformat.sh in order to format code with blake, flake8 and isort
  
  To generate a new flake8 report, please use this command:
  ```flake8 --format=html --htmldir=flake-report```
