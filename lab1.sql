CREATE TABLE `Buyer` (
	`id` INT PRIMARY KEY,
	`name` VARCHAR(50),
	`size` INT UNSIGNED,
	FOREIGN KEY(id)
	REFERENCES SportProduct(id)
);