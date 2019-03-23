DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS contacts;

-- create relations
CREATE TABLE contacts(
    id serial PRIMARY KEY,
    mail text,
    phone text,
    university text
);

CREATE TABLE users(
    id serial PRIMARY KEY,
    login text UNIQUE NOT NULL,
    name text UNIQUE NOT NULL,
    id_contact integer REFERENCES contacts(id),
    salt text NOT NULL,
    pswd_hash text NOT NULL
);

-- create account 1
WITH salt AS (
    SELECT gen_salt('bf') AS salt
)
INSERT INTO users
    (login, name, salt, pswd_hash)
VALUES (
    'Raccoon5',
    'Dan',
    (SELECT salt FROM salt),
    (SELECT crypt('stormfox150', salt) FROM salt)
);

-- create account 2
WITH salt AS (
    SELECT gen_salt('bf') AS salt
)
INSERT INTO users
    (login, name, salt, pswd_hash)
VALUES (
    'Ondra',
    'Ondra',
    (SELECT salt FROM salt),
    (SELECT crypt('', salt) FROM salt)
);

-- create account 3
WITH salt AS (
    SELECT gen_salt('bf') AS salt
)
INSERT INTO users
    (login, name, salt, pswd_hash)
VALUES (
    'Andrej',
    'Andrej',
    (SELECT salt FROM salt),
    (SELECT crypt('', salt) FROM salt)
);