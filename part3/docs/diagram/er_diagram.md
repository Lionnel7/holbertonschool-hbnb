```mermaid
erDiagram
    user {
        CHAR(36) id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
    }

    place {
        CHAR(36) id PK
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK
    }

    review {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
    }

    amenity {
        CHAR(36) id PK
        VARCHAR name
    }

    place_amenity {
        CHAR(36) place_id FK
        CHAR(36) amenity_id FK
    }

    user ||--o{ place : owns
    user ||--o{ review : writes
    place ||--o{ review : has
    place ||--o{ place_amenity : includes
    amenity ||--o{ place_amenity : provides
