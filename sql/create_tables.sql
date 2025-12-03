CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR UNIQUE,
    phone VARCHAR,
    address_line1 VARCHAR,
    city VARCHAR,
    state VARCHAR,
    pincode VARCHAR,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE employment_info (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR,
    designation VARCHAR,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

CREATE TABLE user_bank_info (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    bank_name VARCHAR,
    account_number VARCHAR,
    ifsc VARCHAR,
    account_type VARCHAR
);




