-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.6.4-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para lag_events
DROP DATABASE IF EXISTS `lag_events`;
CREATE DATABASE IF NOT EXISTS `lag_events` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `lag_events`;

-- Volcando estructura para tabla lag_events.admins
DROP TABLE IF EXISTS `admins`;
CREATE TABLE IF NOT EXISTS `admins` (
  `username` varchar(50) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='People with admin privileges';

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla lag_events.bookings
DROP TABLE IF EXISTS `bookings`;
CREATE TABLE IF NOT EXISTS `bookings` (
  `Booth` varchar(50) NOT NULL,
  `userID` varchar(100) NOT NULL,
  `shift` int(11) NOT NULL,
  `canceled` tinyint(1) DEFAULT 0,
  `bookTime` time DEFAULT '00:00:00',
  `enterTime` time DEFAULT '00:00:00',
  UNIQUE KEY `bookings_pk` (`Booth`,`userID`,`shift`),
  CONSTRAINT `bookings_Booths_booth_fk` FOREIGN KEY (`Booth`) REFERENCES `booths` (`booth`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='list of all the bookings in the event';

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla lag_events.booths
DROP TABLE IF EXISTS `booths`;
CREATE TABLE IF NOT EXISTS `booths` (
  `booth` varchar(50) NOT NULL,
  `currentShift` int(11) DEFAULT 0,
  PRIMARY KEY (`booth`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='List of booths in the event with the actual shift number';

-- La exportación de datos fue deseleccionada.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
