CREATE DATABASE IF NOT EXISTS fandu_awd default charset utf8 COLLATE utf8_general_ci;

use fandu_awd;


CREATE TABLE `admin` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`adminname` varchar(128) NOT NULL,
`password` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `admin` (`id`, `adminname`, `password`)
VALUES
(1,'admin','123456');

CREATE TABLE `notice` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`title` int(11) NOT NULL,
`content` varchar(100) NULL,
`date` TEXT NULL,

PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `flag` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`tid` int(11) unsigned NOT NULL,
`flag` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `attackrecord` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`sourcetid` int(11) NOT NULL,
`goaltid` int(11) NOT NULL,
`round` int(11) NOT NULL,
`flag` varchar(128) NOT NULL,
`atttime` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `team` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`teamname` varchar(128) NOT NULL,
`password` varchar(128) NOT NULL,
`token` varchar(128) NOT NULL,
`source` int(11) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `vulhub` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`tid` int(11) NOT NULL,
`cansee` tinyint(1) NOT NULL,
`vulname` varchar(128),
`addr` varchar(64),
`serviceport` varchar(64) NOT NULL,
`sshport` int(11) NOT NULL,
`sshname` varchar(128) NOT NULL,
`sshpass` varchar(128) NOT NULL,
`dockerid` varchar(128) NOT NULL,
`status` tinyint(1) NOT NULL,
`detail` TEXT,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `log` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`username` varchar(128) NOT NULL,
`password` varchar(128) NOT NULL,
`ischeck` tinyint(1) NOT NULL,
`date` DATE,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ulog` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`text` varchar(128) NOT NULL,
`date` DATE,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `game` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`gametitle` varchar(128) NOT NULL,
`starttime` varchar(128) NOT NULL,
`endtime` varchar(128) NOT NULL,
`is_start` tinyint(1) NOT NULL,
`is_end` tinyint(1) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;