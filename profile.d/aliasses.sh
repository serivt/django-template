alias runserver="poetry run python manage.py runserver 0.0.0.0:8000"
alias makemigrations="poetry run python manage.py makemigrations"
alias migrate="poetry run python manage.py migrate"
alias shell="poetry run python manage.py shell"
alias black="poetry run black"
alias isort="poetry run isort -rc"
alias flake8="poetry run flake8"
alias check="poetry run black flake8"

check() {
    poetry run isort -rc $1
    poetry run black $1
    poetry run flake8 $1
}