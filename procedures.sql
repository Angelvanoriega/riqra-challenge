DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users
(
    user_id     serial,
    email       text UNIQUE,
    password    text,
    supplier_id integer
);

DROP TABLE IF EXISTS suppliers;
CREATE TABLE IF NOT EXISTS suppliers
(
    supplier_id serial unique,
    name        text
);
ALTER TABLE users
    ADD CONSTRAINT fk_supplier
        FOREIGN KEY (supplier_id)
            REFERENCES suppliers (supplier_id);

insert into suppliers (supplier_id, name)
values (1, 'Apple');
insert into suppliers (supplier_id, name)
values (2, 'Sprint');
insert into suppliers (supplier_id, name)
values (3, 'T-mobile');

drop function if exists login;
CREATE OR REPLACE FUNCTION login(my_email text,
                                 my_password text) RETURNS SETOF JSON
AS
$$
DECLARE
    email_exist      integer;
    user_password_db text;
BEGIN


    email_exist = (SELECT count(*) FROM users where email = my_email);
    if email_exist > 0 then
        user_password_db = (SELECT password FROM users where email = my_email);
        -- When the email exists and the password is incorrect the API must respond "Oops! wrong password".
        if user_password_db != my_password then
            RAISE EXCEPTION 'Oops! wrong password';
        else
            RETURN QUERY
                -- When the email exists and password is correct a new token is generated for further requests.
                SELECT row_to_json(result)
                FROM (
                         SELECT md5(my_email || CURRENT_TIMESTAMP) as token,
                                'user_logged'                      as message,
                                user_id,
                                email,
                                password,
                                s.supplier_id,
                                s.name
                         FROM users u
                                  inner join suppliers s on s.supplier_id = u.supplier_id
                     ) AS result;
        end if;
    else
        -- When the email does not exist a new user is automatically created (auto signup) and a new token is generated for further requests.
        -- When a new user is registered a supplier is randomly assigned to its account.
        INSERT INTO users (email, password, supplier_id) VALUES (my_email, my_password, random_between(1, 3));
        RETURN QUERY
            SELECT row_to_json(result)
            FROM (
                     SELECT md5(my_email || CURRENT_TIMESTAMP) as token,
                            'user_signed_up'                   as message,
                            user_id,
                            email,
                            password,
                            s.supplier_id,
                            s.name
                     FROM users u
                              inner join suppliers s on s.supplier_id = u.supplier_id
                 ) AS result;
    end if;
END;
$$ LANGUAGE plpgsql;


drop function if exists reset;
CREATE OR REPLACE FUNCTION reset() RETURNS SETOF JSON
AS
$$
BEGIN

    TRUNCATE TABLE users;

    RETURN QUERY
        SELECT row_to_json(result)
        FROM (
                 SELECT 'Database restablished' as message
             ) AS result;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION random_between(low INT, high INT)
    RETURNS INT AS
$$
BEGIN
    RETURN floor(random() * (high - low + 1) + low);
END;
$$ language 'plpgsql' STRICT;