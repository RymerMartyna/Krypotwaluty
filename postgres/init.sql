CREATE TABLE emails (
	id serial PRIMARY KEY,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
    cryptocurrency VARCHAR ( 255 ) NOT NULL,
	created_on TIMESTAMP NOT NULL
);
CREATE TABLE sending_status (
    id serial PRIMARY KEY,
    email VARCHAR ( 255 ) UNIQUE NOT NULL,
    cryptocurrency VARCHAR ( 255 ) NOT NULL,
    sending_time TIMESTAMP NOT NULL,
    s_status VARCHAR ( 255 ) NOT NULL
);
CREATE TABLE price_history (
    id serial PRIMARY KEY,
    cryptocurrency VARCHAR ( 255 ) NOT NULL,
    price NUMERIC (12,6) NOT NULL,
    date_of_price TIMESTAMP NOT NULL
);

CREATE TABLE predictions (
    id serial PRIMARY KEY,
    cryptocurrency VARCHAR ( 255 ) NOT NULL,
    date_of_prediction TIMESTAMP NOT NULL,
    prediction NUMERIC (12,6) NOT NULL
);