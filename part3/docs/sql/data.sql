-- Admin user (mot de passe déjà hashé avec bcrypt)
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'Admin',
  'HBnB',
  'admin@hbnb.io',
  '$2b$12$u0NNQOjD5qvYEBCQHB4EP.tKD90ad/IfOM6ctqkKC9MwiskM2dVny',
  TRUE
);

-- Amenities
INSERT INTO amenity (id, name) VALUES ('f4f2e1ec-e157-4fad-b922-63f068b7af4e', 'WiFi');
INSERT INTO amenity (id, name) VALUES ('9a1a5477-cd79-4524-9d65-347481844a6a', 'Swimming Pool');
INSERT INTO amenity (id, name) VALUES ('a5247942-63cb-4b5f-b78e-af3f4fd7429c', 'Air Conditioning');
