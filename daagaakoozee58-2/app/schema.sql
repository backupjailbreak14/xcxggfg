DROP SCHEMA IF EXISTS `Who_Pays_What`;    
CREATE SCHEMA `Who_Pays_What`;
USE `Who_Pays_What`;

CREATE TABLE `Event`(
	`eventId` INT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(100) NOT NULL,
    `eventDate` DATETIME,
    `creationDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,        
    PRIMARY KEY(`eventId`)
);

INSERT INTO `Event`(`description`, `eventDate`) VALUES('Kerst', '2025-12-25 18:30:00');
INSERT INTO `Event`(`description`, `eventDate`) VALUES('Monkey day', '2025-12-14 14:00:00');
INSERT INTO `Event`(`description`, `eventDate`) VALUES('Pi day', '2026-03-14 01:59:26');
INSERT INTO `Event`(`description`, `eventDate`) VALUES('Tau day', '2026-06-28 03:18:53');
INSERT INTO `Event`(`description`, `eventDate`) VALUES('Inane Answering Message Day', '2026-01-30 04:00:00')