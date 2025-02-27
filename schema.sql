-- Database schema for Energy Billing System

-- Tariffs table
CREATE TABLE tariffs (
    id_market INTEGER NOT NULL,
    cdi INTEGER NOT NULL,
    voltage_level INTEGER NOT NULL,
    G FLOAT,
    T FLOAT,
    D FLOAT,
    R FLOAT,
    C FLOAT,
    P FLOAT,
    CU FLOAT,
    PRIMARY KEY (id_market, cdi, voltage_level)
);

-- Services table
CREATE TABLE services (
    id_service INTEGER NOT NULL,
    id_market INTEGER,
    cir INTEGER,
    voltage_level INTEGER,
    PRIMARY KEY (id_service)
);

-- XM data hourly per agent table
CREATE TABLE xm_data_hourly_per_agent (
    id SERIAL PRIMARY KEY,
    record_timestamp TIMESTAMP,
    value FLOAT
);

-- Records table
CREATE TABLE records (
    id_record INTEGER NOT NULL,
    id_service INTEGER REFERENCES services(id_service),
    record_timestamp TIMESTAMP,
    PRIMARY KEY (id_record)
);

-- Create indexes
CREATE INDEX ix_records_id_record ON records (id_record);
CREATE INDEX ix_services_id_service ON services (id_service);
CREATE INDEX ix_records_timestamp ON records (record_timestamp);
CREATE INDEX ix_xm_data_timestamp ON xm_data_hourly_per_agent (record_timestamp);

-- Consumption table
CREATE TABLE consumption (
    id_record INTEGER NOT NULL REFERENCES records(id_record),
    value FLOAT,
    PRIMARY KEY (id_record)
);

-- Injection table
CREATE TABLE injection (
    id_record INTEGER NOT NULL REFERENCES records(id_record),
    value FLOAT,
    PRIMARY KEY (id_record)
);

-- Sample data for testing

-- Insert sample tariffs
INSERT INTO tariffs (id_market, cdi, voltage_level, G, T, D, R, C, P, CU)
VALUES
    (1, 1, 1, 100.5, 50.2, 30.1, 10.0, 15.5, 5.0, 200.0),
    (1, 2, 1, 100.5, 50.2, 30.1, 10.0, 15.5, 5.0, 190.0),
    (1, 1, 2, 95.0, 48.0, 28.5, 9.5, 14.8, 4.8, 185.0),
    (1, 2, 2, 95.0, 48.0, 28.5, 9.5, 14.8, 4.8, 185.0),
    (1, 1, 3, 90.0, 46.0, 27.0, 9.0, 14.0, 4.5, 180.0),
    (1, 2, 3, 90.0, 46.0, 27.0, 9.0, 14.0, 4.5, 180.0);

-- Insert sample services
INSERT INTO services (id_service, id_market, cir, voltage_level)
VALUES
    (1, 1, 1, 1),
    (2, 1, 2, 1),
    (3, 1, 1, 2),
    (4, 1, 2, 3);

-- Insert sample XM data hourly per agent (for one day)
INSERT INTO xm_data_hourly_per_agent (record_timestamp, value)
VALUES
    ('2023-02-01 00:00:00', 110.5),
    ('2023-02-01 01:00:00', 105.2),
    ('2023-02-01 02:00:00', 98.7),
    ('2023-02-01 03:00:00', 95.3),
    ('2023-02-01 04:00:00', 97.8),
    ('2023-02-01 05:00:00', 102.4),
    ('2023-02-01 06:00:00', 115.6),
    ('2023-02-01 07:00:00', 120.8),
    ('2023-02-01 08:00:00', 125.3),
    ('2023-02-01 09:00:00', 130.1),
    ('2023-02-01 10:00:00', 135.4);

-- Insert sample records, consumption, and injection for client 1
-- First record
INSERT INTO records (id_record, id_service, record_timestamp)
VALUES (1, 1, '2023-02-01 00:00:00');

INSERT INTO consumption (id_record, value)
VALUES (1, 10.0);

INSERT INTO injection (id_record, value)
VALUES (1, 15.0);

-- Second record
INSERT INTO records (id_record, id_service, record_timestamp)
VALUES (2, 1, '2023-02-01 01:00:00');

INSERT INTO consumption (id_record, value)
VALUES (2, 10.0);

INSERT INTO injection (id_record, value)
VALUES (2, 15.0);

-- Third record
INSERT INTO records (id_record, id_service, record_timestamp)
VALUES (3, 1, '2023-02-01 02:00:00');

INSERT INTO consumption (id_record, value)
VALUES (3, 10.0);

INSERT INTO injection (id_record, value)
VALUES (3, 15.0);

-- Insert more records for different hours
INSERT INTO records (id_record, id_service, record_timestamp)
VALUES
    (4, 1, '2023-02-01 03:00:00'),
    (5, 1, '2023-02-01 04:00:00'),
    (6, 1, '2023-02-01 05:00:00'),
    (7, 1, '2023-02-01 06:00:00'),
    (8, 1, '2023-02-01 07:00:00'),
    (9, 1, '2023-02-01 08:00:00'),
    (10, 1, '2023-02-01 09:00:00');

INSERT INTO consumption (id_record, value)
VALUES
    (4, 10.0),
    (5, 10.0),
    (6, 10.0),
    (7, 10.0),
    (8, 10.0),
    (9, 10.0),
    (10, 10.0);

INSERT INTO injection (id_record, value)
VALUES
    (4, 15.0),
    (5, 15.0),
    (6, 15.0),
    (7, 15.0),
    (8, 15.0),
    (9, 15.0),
    (10, 15.0);