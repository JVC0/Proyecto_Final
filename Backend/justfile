# Set PowerShell as the default shell
set shell := ["pwsh", "-Command"]

project := file_stem(justfile_dir())
venv-name := ".venv"
venv-path := join(justfile_dir(), venv-name)
pip-cmd := "pip"  # Default to pip for Windows

# ==============================================================================
# DJANGO RECIPES
# ==============================================================================

# Launch development server
runserver: 
    python manage.py runserver

# Launch Django interactive shell
sh:
    python manage.py shell

alias mm := makemigrations
# Make Django migrations
makemigrations:
    python manage.py makemigrations

alias m := migrate
# Apply Django migrations
migrate:
    python manage.py migrate

alias c := check
# Check if Django project is correct
check:
    python manage.py check

# Add a new app and install it on settings.py
startapp app:
    python manage.py startapp {{ app }}
    $APP_CLASS = '{{ app }}'
    $APP_CONFIG = "$APP_CLASS.apps.$($APP_CLASS.Substring(0,1).ToUpper()$($APP_CLASS.Substring(1))Config"
    (Get-Content ./main/settings.py) -replace '(INSTALLED_APPS *= *\[)(.*?)(\])', "`$1`$2    '$APP_CONFIG',`n`$3" | Set-Content ./main/settings.py
    Write-Output "✔ {{ app }} installed & added to settings.INSTALLED_APPS"

create-su username="admin" password="admin" email="admin@example.com":
    python manage.py shell -c "from django.contrib.auth.models import User; user, _ = User.objects.get_or_create(username='{{ username }}'); user.email = '{{ email }}'; user.set_password('{{ password }}'); user.is_superuser = True; user.is_staff = True; user.save()"
# ==============================================================================
# MISC RECIPES
# ==============================================================================
reset-db: && create-su
    Get-ChildItem -Path . -Recurse -Filter *.py -File | Where-Object { $_.FullName -like "*\migrations\*" -and $_.FullName -notlike "*\.venv\*" -and $_.Name -ne "__init__.py" } | Remove-Item -Force
    Get-ChildItem -Path . -Recurse -Filter *.pyc -File | Where-Object { $_.FullName -like "*\migrations\*" -and $_.FullName -notlike "*\.venv\*" } | Remove-Item -Force
    Remove-Item -Path db.sqlite3 -ErrorAction SilentlyContinue
    python manage.py makemigrations
    python manage.py migrate