CREATE DATABASE IF NOT EXISTS inventory_management;
USE inventory_management;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(80) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    available_quantity INT NOT NULL DEFAULT 0 CHECK (available_quantity >= 0),
    INDEX ix_products_name (name),
    INDEX ix_products_category (category)
);

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(25) NOT NULL,
    INDEX ix_customers_email (email)
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    status VARCHAR(30) NOT NULL DEFAULT 'CREATED',
    CONSTRAINT fk_orders_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id),
    INDEX ix_orders_customer_id (customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    line_total DECIMAL(10, 2) NOT NULL CHECK (line_total >= 0),
    CONSTRAINT fk_order_items_order_id FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_items_product_id FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX ix_order_items_order_id (order_id),
    INDEX ix_order_items_product_id (product_id)
);
