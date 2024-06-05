-- Database: airlines

-- DROP DATABASE IF EXISTS airlines;

CREATE DATABASE airlines
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE airlines TO PUBLIC;

GRANT CONNECT ON DATABASE airlines TO pg_read_all_data;

GRANT ALL ON DATABASE airlines TO postgres;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT SELECT ON TABLES TO pg_read_all_data;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres
GRANT SELECT, USAGE ON SEQUENCES TO pg_read_all_data;