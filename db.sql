CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL
);

CREATE TABLE product_versions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    version VARCHAR(5) NOT NULL,
    release_date DATE NOT NULL,
    release_notes VARCHAR(100) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE product_details (
    product_id INT PRIMARY KEY NOT NULL,
    product_lead VARCHAR(20) NOT NULL,
    latest_version INT NOT NULL,
    license_contact VARCHAR(30) NOT NULL,
    url VARCHAR(100) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (latest_version) REFERENCES product_versions(id)
);

CREATE TABLE clients (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    client_manager VARCHAR(20) NOT NULL
);

CREATE TABLE client_services (
    entry_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT NOT NULL,
    product_id INT NOT NULL,
    product_version INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (product_version) REFERENCES product_versions(id)
);

INSERT INTO products VALUES (1, "TriplePoint");
INSERT INTO products VALUES (2, "Fidessa");

INSERT INTO product_versions VALUES (1, 1, "18.1", "2022-05-06", "Bumped dependencies");
INSERT INTO product_versions VALUES (2, 1, "18.0", "2022-04-06", "Fixed bugs");
INSERT INTO product_versions VALUES (3, 1, "17.0", "2021-09-16", "Resolved issues");
INSERT INTO product_versions VALUES (4, 2, "10.1", "2022-05-23", "Updated dependencies");
INSERT INTO product_versions VALUES (5, 2, "10.0", "2022-04-23", "Fixed bugs");
INSERT INTO product_versions VALUES (6, 2, "9.0", "2021-09-23", "Resolved issues");

INSERT INTO product_details VALUES (1, "Person 1", 1, "+1-800-555-1234", "https://www.tpt.com/products/agriculture/");
INSERT INTO product_details VALUES (2, "Person 2", 4, "+1-800-555-1256", "https://iongroup.com/markets/products/fidessa/");

INSERT INTO clients VALUES (1, "Client 1", "Person 3");
INSERT INTO clients VALUES (2, "Client 2", "Person 4");

INSERT INTO client_services VALUES (1, 1, 1, 2);
INSERT INTO client_services VALUES (2, 1, 2, 6);
INSERT INTO client_services VALUES (3, 2, 1, 1);

-- Query 1
SELECT * FROM products;

-- Query 2
SELECT products.product_id,
    name,
    product_lead,
    license_contact,
    url
FROM products
    JOIN product_details ON products.product_id = product_details.product_id;

-- Query 3
SELECT products.product_id,
    name,
    version,
    release_date,
    release_notes
FROM products
    join product_versions on product_versions.product_id = products.product_id;

-- Query 4
SELECT * FROM clients;
SELECT clients.name,
    client_manager,
    products.name,
    version,
    release_date,
    release_notes
from client_services
    join clients on client_services.client_id = clients.client_id
    join products on client_services.product_id = products.product_id
    join product_versions on client_services.product_version = product_versions.id;

-- Query 5
SELECT clients.name,
    client_manager,
    products.name,
    version,
    release_date,
    release_notes
from client_services
    join clients on client_services.client_id = clients.client_id
    join products on client_services.product_id = products.product_id
    join product_versions on client_services.product_version = product_versions.id
WHERE clients.name = "Client 1";