CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,
    product TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INTEGER NOT NULL,
    customer TEXT NOT NULL,
    upload_date TIMESTAMPTZ DEFAULT NOW()
);