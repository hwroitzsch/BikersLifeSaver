-- phpMyAdmin SQL Dump
-- version 4.5.0.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Erstellungszeit: 30. Nov 2015 um 13:37
-- Server-Version: 10.0.17-MariaDB
-- PHP-Version: 5.6.14

CREATE DATABASE accidentspots;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `accidentspots`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `accident_spots`
--

CREATE TABLE `accident_spots` (
  `NodeId` int(10) UNSIGNED NOT NULL,
  `Latitude` double NOT NULL,
  `Longitude` double NOT NULL,
  `Number_of_members` int(10) UNSIGNED NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `accident_spots`
--

INSERT INTO `accident_spots` (`NodeId`, `Latitude`, `Longitude`, `Number_of_members`, `TimeStamp`) VALUES
(4, 52.31959, 13.63091, 5, '2015-11-17 21:00:07'),
(10, 52.31902, 13.63459, 3, '2015-11-17 21:00:07');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `node_neighbor_relation`
--

CREATE TABLE `node_neighbor_relation` (
  `NodeId` int(10) UNSIGNED NOT NULL,
  `Neighbor` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `node_neighbor_relation`
--

INSERT INTO `node_neighbor_relation` (`NodeId`, `Neighbor`) VALUES
(2, 4),
(3, 4),
(3, 7),
(3, 8),
(4, 2),
(4, 3),
(4, 7),
(4, 8),
(7, 3),
(7, 4),
(7, 8),
(8, 3),
(8, 4),
(8, 7),
(10, 11),
(10, 12),
(11, 10),
(11, 12),
(12, 10),
(12, 11);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `quantity_of_neighbors`
--

CREATE TABLE `quantity_of_neighbors` (
  `NodeId` int(10) UNSIGNED NOT NULL,
  `NumberOfNeighbors` int(10) UNSIGNED NOT NULL,
  `Neighbors` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `received_coordinates`
--

CREATE TABLE `received_coordinates` (
  `NodeId` int(10) UNSIGNED NOT NULL,
  `Latitude` double NOT NULL,
  `Longitude` double NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `received_coordinates`
--

INSERT INTO `received_coordinates` (`NodeId`, `Latitude`, `Longitude`, `TimeStamp`) VALUES
(1, 52.31956, 13.63098, '2015-10-12 10:33:42'),
(2, 52.31964, 13.63054, '2015-11-12 11:34:36'),
(3, 52.31957, 13.63122, '2015-11-12 11:35:10'),
(4, 52.31959, 13.63091, '2015-11-12 11:35:22'),
(5, 52.31977, 13.63433, '2015-11-14 11:40:35'),
(6, 52.319923, 13.628854, '2015-11-14 21:12:18'),
(7, 52.319565, 13.631232, '2015-11-14 21:11:49'),
(8, 52.31951, 13.63129, '2015-11-16 10:46:09'),
(9, 52.31935, 13.63229, '2015-11-16 10:46:50'),
(10, 52.31902, 13.63459, '2015-11-16 14:34:50'),
(11, 52.31899, 13.63457, '2015-11-16 14:35:21'),
(12, 52.31908, 13.63462, '2015-11-16 14:35:53'),
(13, 52.31899, 13.63461, '2015-10-14 13:36:29'),
(14, 52.318, 13.6341, '2015-11-16 14:42:06'),
(16, 52.31956, 13.63098, '2015-10-12 10:33:42'),
(17, 55.31956, 33.63098, '2015-11-29 10:33:42'),
(18, 53.33555, 14.72057, '2015-11-29 19:30:42'),
(19, 53.33555, 14.72057, '2015-11-29 22:05:42'),
(20, 53.33555, 14.72057, '2015-11-29 22:34:25'),
(21, 53.33555, 14.72057, '2015-11-29 22:43:11'),
(22, 57.33555, 18.72057, '2015-11-30 12:31:14');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `accident_spots`
--
ALTER TABLE `accident_spots`
  ADD UNIQUE KEY `NodeId` (`NodeId`);

--
-- Indizes für die Tabelle `node_neighbor_relation`
--
ALTER TABLE `node_neighbor_relation`
  ADD KEY `NodeId` (`NodeId`);

--
-- Indizes für die Tabelle `quantity_of_neighbors`
--
ALTER TABLE `quantity_of_neighbors`
  ADD UNIQUE KEY `NodeId` (`NodeId`);

--
-- Indizes für die Tabelle `received_coordinates`
--
ALTER TABLE `received_coordinates`
  ADD PRIMARY KEY (`NodeId`),
  ADD UNIQUE KEY `NodeId` (`NodeId`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `received_coordinates`
--
ALTER TABLE `received_coordinates`
  MODIFY `NodeId` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
