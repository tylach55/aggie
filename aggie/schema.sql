DROP TABLE IF EXISTS harvest;
DROP TABLE IF EXISTS shipment;

CREATE TABLE harvest(
	bushells_left INTEGER NOT NULL,
	crop TEXT NOT NULL,
	expiration DATE NOT NULL,
	picked DATE NOT NULL
);

CREATE TABLE shipment(
	bushells_of_wheat INTEGER NOT NULL DEFAULT 0,
	bushells_of_walnuts INTEGER NOT NULL DEFAULT 0,
	bushells_of_almonds INTEGER NOT NULL DEFAULT 0
);