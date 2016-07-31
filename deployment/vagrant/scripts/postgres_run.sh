#!/usr/bin/env bash

LOCAL_DB_NAME=utopia
LOCAL_DB_USER=utopiadev
LOCAL_DB_PASSWORD=localdev

cat <<EOF | psql
-- Create the database:
CREATE DATABASE $LOCAL_DB_NAME;
-- Create the database user:
CREATE USER $LOCAL_DB_USER WITH PASSWORD '$LOCAL_DB_PASSWORD';
-- Give the user permission to create dbs (i.e. the test database)
ALTER USER $LOCAL_DB_USER WITH CREATEDB;
-- Give the user permission to create schemas on db
GRANT CREATE ON DATABASE $LOCAL_DB_NAME TO $LOCAL_DB_USER;
EOF
