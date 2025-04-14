-- Create admins table
CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_super BOOLEAN DEFAULT TRUE
);

-- Create users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    driving_license_no VARCHAR(50) UNIQUE NOT NULL
);

-- Create cars table
CREATE TABLE cars (
    id INT PRIMARY KEY AUTO_INCREMENT,
    brand VARCHAR(50) NOT NULL,
    number_plate VARCHAR(20) UNIQUE NOT NULL,
    added_by_admin_id INT,
    FOREIGN KEY (added_by_admin_id) REFERENCES admins(id) ON DELETE SET NULL
);

-- Create borrowings table
CREATE TABLE borrowings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    date_of_issue DATE NOT NULL,
    date_of_return DATE,
    state_on_issue ENUM('Good', 'Better', 'Average', 'Poor') NOT NULL,
    state_on_return ENUM('Good', 'Better', 'Average', 'Poor'),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id)
);