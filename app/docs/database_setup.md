# Database Setup - Greeting App

## PostgreSQL Installation
Installed PostgreSQL locally.

Version: 18.2
Run:
psql --Version

Default Port:
5432

## Database Created
Database Name: greeting_app

Command Used: CREATE DATABASE greeting_app;

## Aplication User
Username: greeting_user

Created with: CREATE ROLE greeting_user WITH LOGIN PASSWORD '******';

Privileges granted: GRANT ALL PRIVILEGES ON DATABASE greeting_app TO greeting_user;

## Test Connection
Command: psql -U greeting_user -d greeting_app -h localhost

## Notes:
- Do not use postgres superuser in production.
- Use environment Variables for DATABASE_URL.
- Never commit passwords to Git.
