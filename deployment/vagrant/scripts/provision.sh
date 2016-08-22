#!/usr/bin/env bash

update-locale LANG=en_US.UTF-8
echo "UTC" | tee /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata

apt-get update --fix-missing
apt-get install -y python-pip
apt-get install -y postgresql postgresql-contrib

# prereqs for psycopg2
apt-get install -y python-dev
apt-get install -y libpq-dev

# upgrade pip
pip install --upgrade pip

# globally installed python packages
pip install virtualenv virtualenvwrapper

# install our pg_hba.conf
POSTGRES_VERSION=$(psql --version | egrep -o '[0-9]{1,2}\.[0-9]{1,2}')
POSTGRES_ETC_DIR=/etc/postgresql/$POSTGRES_VERSION/main
mv $POSTGRES_ETC_DIR/pg_hba.conf $POSTGRES_ETC_DIR/pg_hba.bak
cp /vagrant/deployment/vagrant/conf/pg_hba.conf $POSTGRES_ETC_DIR/
chown postgres:postgres $POSTGRES_ETC_DIR/pg_hba.conf

service postgresql restart

echo "DJANGO_SETTINGS_MODULE=up.settings" >> /etc/environment
echo "IN_PROD=False" >> /etc/environment

# Execute "as-user" provisioning scripts
VAGRANT_SCRIPTS_DIR=/vagrant/deployment/vagrant/scripts
sudo -i -u postgres . $VAGRANT_SCRIPTS_DIR/postgres_run.sh
sudo -i -u vagrant . $VAGRANT_SCRIPTS_DIR/vagrant_run.sh
