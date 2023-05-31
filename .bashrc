alias install='poetry install'
alias runserver='poetry run python manage.py runserver'
alias migration='poetry run python manage.py makemigrations'
alias migrate='poetry run python manage.py migrate'
alias createsuperuser='poetry run python manage.py createsuperuser'
alias test='poetry run python manage.py test'
alias coverage='poetry run coverage run --source="." manage.py test && poetry run coverage report && poetry run coverage html'
alias clean='poetry run coverage erase && rm -rf htmlcov'

# Alias for running Celery
alias celery='poetry run python -m celery -A your_project_name worker --loglevel=info'

# Add other aliases or customizations as needed

# Load virtual environment (if using Poetry)
if command -v poetry >/dev/null 2>&1; then
  poetry shell
fi
