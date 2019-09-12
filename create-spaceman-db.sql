-- User: spaceman_game_user
-- DROP USER spaceman_game_user;

CREATE USER spaceman_game_user WITH LOGIN NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;


ALTER USER spaceman_game_user with PASSWORD = 'password';

-- Database: spaceman_game
-- DROP DATABASE spaceman_game;

CREATE DATABASE spaceman_game WITH OWNER = postgres ENCODING = 'UTF8' LC_COLLATE = 'C' LC_CTYPE = 'C' TABLESPACE = pg_default CONNECTION
LIMIT = -1;

GRANT ALL ON DATABASE spaceman_game TO postgres;

GRANT
TEMPORARY,
      CONNECT ON DATABASE spaceman_game TO PUBLIC;

GRANT ALL ON DATABASE spaceman_game TO spaceman_game_user;