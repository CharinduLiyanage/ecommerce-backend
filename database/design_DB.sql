USE ecommerce_db;

-- Create the Product table
CREATE TABLE Product (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,         -- Primary key
    name VARCHAR(255) NOT NULL,                         -- Product name
    description TEXT,                                   -- Product description
    price DECIMAL(10, 2) NOT NULL,                      -- Product price
    stock INT NOT NULL,                                 -- Product stock quantity
    image_url VARCHAR(255),                             -- URL to the product image
    created_at TIMESTAMP DEFAULT NOW(),                 -- Creation timestamp
    updated_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW(), -- Update timestamp
    deleted BOOLEAN DEFAULT FALSE                       -- Soft delete flag
);

-- Create the CustomerOrder table
CREATE TABLE CustomerOrder (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, -- Primary key
    user_sub VARCHAR(255) NOT NULL,             -- User identifier (e.g., Cognito user ID)
    total DECIMAL(10, 2) NOT NULL,              -- Total order price
    created_at TIMESTAMP DEFAULT NOW()          -- Creation timestamp
);

-- Create the OrderItem table
CREATE TABLE OrderItem (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,                             -- Primary key
    order_id INT UNSIGNED NOT NULL,                                         -- Foreign key to CustomerOrder table
    product_id INT UNSIGNED NOT NULL,                                       -- Foreign key to Product table
    quantity INT NOT NULL,                                                  -- Quantity of the product in the order
    price DECIMAL(10, 2) NOT NULL,                                          -- Price of the product at the time of the order
    FOREIGN KEY (order_id) REFERENCES CustomerOrder (id) ON DELETE CASCADE, -- Cascade delete if order is deleted
    FOREIGN KEY (product_id) REFERENCES Product (id)                        -- Product reference
);
