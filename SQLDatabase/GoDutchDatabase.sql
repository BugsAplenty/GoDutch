-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `godutch` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `godutch` ;

-- -----------------------------------------------------
-- Table `godutch`.`bot_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `godutch`.`bot_users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `username` VARCHAR(64) NOT NULL,
  `date_added` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `godutch`.`transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `godutch`.`transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `transaction_amount` FLOAT NOT NULL,
  `transaction_name` VARCHAR(64) NOT NULL,
  `transaction_date` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `transactions_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `godutch`.`bot_users` (`user_id`)
)
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

DELIMITER //
CREATE PROCEDURE check_database_exists(db_name VARCHAR(40))
BEGIN
	SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA 
    WHERE schema_name = db_name;
END;

CREATE PROCEDURE get_user_monthly_total
(
	INT @query_user_id
    INT @query_month
    INT @query_year
)
BEGIN
	SELECT SUM(`transaction_amount`) 
    FROM `transactions` 
    WHERE `user_id` = @query_user_id AND month(`date`) = @query_month AND year(`date`) = @query_year;
END;

CREATE PROCEDURE get_username_by_id
(
	INT @query_user_id
)
BEGIN
	SELECT `username`
    FROM `transactions`
    WHERE `user_id` = @query_user_id;
END;

CREATE PROCEDURE user_exists
(
	INT @query_user_id
)
BEGIN
	SELECT 1
    FROM `bot_users`
    WHERE `user_id` = @query_user_id;
END;

CREATE PROCEDURE add_user
    (
        INT @query_user_id
        VARCHAR(64) @query_username
        DATE @query_date_added
    )
BEGIN
	INSERT INTO `bot_users`(`user_id`, `username`, `date_added`)
    VALUES (@query_user_id, @query_username, @query_date_added);
END;

CREATE PROCEDURE add_transaction
(
	INT @query_user_id
    FLOAT @query_transaction_amount
    VARCHAR(64) @query_transaction_name
    DATE @query_transaction_date
)
BEGIN
	INSERT INTO `transactions`(`user_id`, `transaction_amount`, `transaction_name`, `transaction_date`)
	VALUES (@query_user_id, @query_transaction_amount, @query_transaction_name, @query_transaction_date)
END;

CREATE PROCEDURE update_username
    (
        INT @query_user_id
        VARCHAR(64) @new_username
    )
BEGIN
    UPDATE `users`
    SET `username` = @new_username
    WHERE `user_id` = @query_user_id
END;

DELIMITER //
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


