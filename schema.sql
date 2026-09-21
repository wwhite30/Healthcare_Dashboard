
-- Healthcare Database Schema (PostgreSQL)


DROP TABLE IF EXISTS billing CASCADE;
DROP TABLE IF EXISTS prescriptions CASCADE;
DROP TABLE IF EXISTS diagnoses CASCADE;
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS doctors CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

CREATE TABLE departments (
    department_id   SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE doctors (
    doctor_id       SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    specialty       VARCHAR(100),
    department_id   INT REFERENCES departments(department_id),
    hire_date       DATE
);

CREATE TABLE patients (
    patient_id      SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    date_of_birth   DATE NOT NULL,
    gender          VARCHAR(10),
    phone           VARCHAR(20),
    email           VARCHAR(100),
    address         VARCHAR(200)
);

CREATE TABLE appointments (
    appointment_id  SERIAL PRIMARY KEY,
    patient_id      INT REFERENCES patients(patient_id),
    doctor_id       INT REFERENCES doctors(doctor_id),
    appointment_date TIMESTAMP NOT NULL,
    reason          VARCHAR(255),
    status          VARCHAR(20) DEFAULT 'scheduled'
        CHECK (status IN ('scheduled','completed','cancelled','no-show'))
);

CREATE TABLE diagnoses (
    diagnosis_id    SERIAL PRIMARY KEY,
    appointment_id  INT REFERENCES appointments(appointment_id),
    diagnosis_code  VARCHAR(10),
    description     VARCHAR(255),
    diagnosed_date  DATE DEFAULT CURRENT_DATE
);

CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id  INT REFERENCES appointments(appointment_id),
    medication_name VARCHAR(100),
    dosage          VARCHAR(50),
    frequency       VARCHAR(50),
    duration_days   INT
);

CREATE TABLE billing (
    bill_id         SERIAL PRIMARY KEY,
    appointment_id  INT REFERENCES appointments(appointment_id) UNIQUE,
    amount          NUMERIC(10,2) NOT NULL,
    insurance_covered NUMERIC(10,2) DEFAULT 0,
    payment_status  VARCHAR(20) DEFAULT 'unpaid'
        CHECK (payment_status IN ('unpaid','paid','partial'))
);