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
runserver: kill-runservers
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



# ==============================================================================
# MISC RECIPES
# ==============================================================================

# Kill all Django runserver processes
[private]
kill-runservers:
    powershell -Command "Get-Process python* | Where-Object { $_.ProcessName -eq 'python' -and $_.CommandLine -like '*manage.py runserver*' } | Stop-Process -Force -ErrorAction SilentlyContinue"