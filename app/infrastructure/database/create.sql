-- database: ./manicure.db
CREATE TABLE IF NOT EXISTS
    "services" (
        "id" INTEGER NOT NULL UNIQUE,
        "name" VARCHAR NOT NULL,
        "duration_minutes" INTEGER NOT NULL,
        "price" INTEGER NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE IF NOT EXISTS
    "appointments" (
        "id" INTEGER NOT NULL UNIQUE,
        "user_id" INTEGER NOT NULL,
        "date" DATE NOT NULL,
        "time_start" VARCHAR NOT NULL,
        "time_end" VARCHAR NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE IF NOT EXISTS
    "service_to_appointments" (
        "id" INTEGER NOT NULL UNIQUE,
        "service_id" INTEGER NOT NULL,
        "appointment_id" INTEGER NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("appointment_id") REFERENCES "appointments" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("service_id") REFERENCES "services" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );
