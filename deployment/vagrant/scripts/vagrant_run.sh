#!/usr/bin/env bash

PROJECT_VIRTUALENV_NAME=up
WORKON_HOME=/home/vagrant/.virtualenvs
PROJECT_HOME=/vagrant
DJANGO_HOME=$PROJECT_HOME/up
DJANGO_APPS_FOLDER=$DJANGO_HOME/apps
BASHRC=/home/vagrant/.bashrc
VIRTUALENVWRAPPER_LOCATION=/usr/local/bin/virtualenvwrapper.sh
INITIAL_DATA_SCRIPT=/vagrant/deployment/vagrant/scripts/load_initial_data.py

# Add virtualenvwrapper config to vagrant user's .bashrc
echo '' > $BASHRC
echo '#' [auto]: virtualenvwrapper configs: >> $BASHRC
echo export WORKON_HOME=$WORKON_HOME >> $BASHRC
echo export PROJECT_HOME=$PROJECT_HOME >> $BASHRC
echo source $VIRTUALENVWRAPPER_LOCATION >> $BASHRC
echo '' >> $BASHRC
echo '#' [auto]: Activate the $PROJECT_VIRTUALENV_NAME venv by default >> $BASHRC
echo workon $PROJECT_VIRTUALENV_NAME >> $BASHRC

# Setup the virtualenv
source $VIRTUALENVWRAPPER_LOCATION
mkvirtualenv $PROJECT_VIRTUALENV_NAME
add2virtualenv $DJANGO_HOME
add2virtualenv $DJANGO_APPS_FOLDER
setvirtualenvproject $VIRTUAL_ENV $DJANGO_HOME

# Install requirements
pip install -r $PROJECT_HOME/requirements.txt

# Run migrations
cd $DJANGO_HOME
python manage.py migrate

# Install initial data
python $INITIAL_DATA_SCRIPT
