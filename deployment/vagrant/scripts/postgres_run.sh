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
-- UTC or bust
ALTER ROLE $LOCAL_DB_USER SET timezone TO 'UTC';
-- UTF-8 or bust
ALTER ROLE $LOCAL_DB_USER SET client_encoding TO 'utf8';
-- Copypasta. Isn't this the default?
ALTER ROLE $LOCAL_DB_USER SET default_transaction_isolation TO 'read committed';
EOF
