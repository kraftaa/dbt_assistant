-- make sure schema exists
create schema if not exists raw;

-- Customers table
create table if not exists raw.customers (
    id          bigint primary key,
    name        text,
    email       text,
    created_at  timestamp
);

-- Orders table
create table if not exists raw.orders (
    id            bigint primary key,
    product_id    bigint references raw.products(id),
    customer_id   bigint references raw.customers(id),
    order_date    timestamp,
    total_amount  numeric(12,2)
);

-- Products table
create table if not exists raw.products (
    id            bigint primary key,
    product_name  text,
    category      text,
    price         numeric(12,2)
);

-- Refunds table
create table if not exists raw.refunds (
    id            bigint primary key,
    order_id      bigint references raw.orders(id),
    customer_id   bigint references raw.customers(id),
    refund_date   timestamp,
    refund_amount numeric(12,2)
);
