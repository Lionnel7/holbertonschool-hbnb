USE hbnb_db;

-- Test CREATE
-- Création d'un nouvel utilisateur
INSERT INTO users (id, first_name, last_name, email, password)
VALUES (UUID(), 'John', 'Doe', 'john.doe@test.com', 'password123');

-- Création d'une place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
SELECT 
    UUID(),
    'Beautiful Apartment',
    'A cozy apartment in the city center',
    100.00,
    48.8566,
    2.3522,
    id
FROM users
WHERE email = 'john.doe@test.com';

-- Test READ
-- Lecture des utilisateurs
SELECT * FROM users;

-- Lecture des places avec leurs propriétaires
SELECT p.*, u.first_name, u.last_name
FROM places p
JOIN users u ON p.owner_id = u.id;

-- Test UPDATE
-- Mise à jour d'un utilisateur
UPDATE users
SET first_name = 'Johnny'
WHERE email = 'john.doe@test.com';

-- Mise à jour d'une place
UPDATE places
SET price = 120.00
WHERE title = 'Beautiful Apartment';

-- Test DELETE
-- Suppression d'une place
DELETE FROM places
WHERE title = 'Beautiful Apartment';

-- Suppression d'un utilisateur (cascade sur ses places)
DELETE FROM users
WHERE email = 'john.doe@test.com'; 
