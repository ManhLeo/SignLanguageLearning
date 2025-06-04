import os
import subprocess
import sys

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def create_project():
    # Create Django project
    run_command('django-admin startproject sign_language .')
    
    # Create apps
    apps = ['accounts', 'tutorials', 'learning', 'recognition']
    for app in apps:
        run_command(f'python manage.py startapp {app}')
    
    # Create necessary directories
    os.makedirs('media/videos', exist_ok=True)
    os.makedirs('media/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

if __name__ == '__main__':
    create_project()
    print("Project structure created successfully!") 