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

DELIMITER $$
CREATE PROCEDURE check_database_exists(db_name VARCHAR(40))
BEGIN
	SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA 
    WHERE schema_name = db_name;
END $$

CREATE PROCEDURE get_user_monthly_total(
	IN p_user_id int,
    IN p_date date
)
BEGIN
	SELECT SUM(`transaction_amount`)
    FROM `transactions`
    GROUP BY `user_id` = p_user_id, month(`transaction_date`) = month(p_date) AND year(`transaction_date`) = year(p_date);
END $$

CREATE PROCEDURE get_username_by_id
(
	IN p_user_id int
)
BEGIN
	SELECT `username`
    FROM `bot_users`
    WHERE `user_id` = p_user_id;
END $$

CREATE PROCEDURE user_exists
(
	IN p_user_id int
)
BEGIN
	SELECT 1
    FROM `bot_users`
    WHERE `user_id` = p_user_id;
END $$

CREATE PROCEDURE add_user
    (
		IN p_user_id int,
        IN p_username varchar(64),
        IN p_date_added date
    )
BEGIN
	INSERT INTO `bot_users`(`user_id`, `username`, `date_added`)
    VALUES (p_user_id, p_username, p_date_added);
END $$

CREATE PROCEDURE add_transaction
(
	IN p_user_id int,
    IN p_transaction_amount float,
    IN p_transaction_name varchar(64),
    IN p_transaction_date date
)
BEGIN
	INSERT INTO `transactions`(`user_id`, `transaction_amount`, `transaction_name`, `transaction_date`)
	VALUES (p_user_id, p_transaction_amount, p_transaction_name, p_transaction_date);
END $$

CREATE PROCEDURE update_username
    (
        IN p_user_id int,
        IN new_username varchar(64)
    )
BEGIN
    UPDATE `bot_users`
    SET `username` = new_username
    WHERE `user_id` = p_user_id;
END $$

CREATE PROCEDURE get_all_user_ids()
BEGIN
    SELECT `user_id` FROM `bot_users`;
END $$


CREATE PROCEDURE get_all_usernames()
BEGIN
    SELECT `username` FROM `bot_users`;
END $$

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


