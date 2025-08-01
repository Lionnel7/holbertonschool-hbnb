USE hbnb_db;

-- Insertion de l'administrateur par défaut
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    UUID(),
    'Holberton',
    'School',
    'holberton.school@localhost.local',
    -- Le mot de passe devrait être hashé dans l application
    'Password123456789!',
    TRUE
);

-- Insertion des amenities de base
INSERT INTO amenities (id, name) VALUES
(UUID(), 'WiFi'),
(UUID(), 'Air conditioning'),
(UUID(), 'Heating'),
(UUID(), 'Kitchen'),
(UUID(), 'TV'),
(UUID(), 'Pool'),
(UUID(), 'Gym'),
(UUID(), 'Free parking'),
(UUID(), 'Washing machine'),
(UUID(), 'Dryer'); 
