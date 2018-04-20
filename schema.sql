DROP TABLE IF EXISTS `Password`;
DROP TABLE IF EXISTS `Box`;
DROP TABLE IF EXISTS `Payment`;
DROP TABLE IF EXISTS `Candy`;
DROP TABLE IF EXISTS `Item`;
DROP TABLE IF EXISTS `Customer`;
DROP TABLE IF EXISTS `Order`;

CREATE TABLE `Item` (
  `box_id`   INTEGER NOT NULL,
  `order_id` INTEGER NOT NULL,
  `quantity` INTEGER NOT NULL,
  PRIMARY KEY (`box_id`)
);

CREATE TABLE `Candy` (
  `candy_name`  TEXT     NOT NULL,
  `calories`    INTEGER  NOT NULL,
  `ingredients` TEXT     NOT NULL,
  `price`       REAL     NOT NULL,
  PRIMARY KEY (`candy_name`)
);

INSERT INTO `Candy`
	(`candy_name`, `calories`, `ingredients`, `price`)
VALUES
	( 'C1', 100, 'Milk',            2.5),
	( 'C2', 150, 'White chocolate', 2.0),
	( 'C3', 120, 'Almond',          2.8),
	( 'C4', 160, 'Sugar',           1.5);

CREATE TABLE `Customer` (
  `email`      TEXT NOT NULL,
  `first_name` TEXT NOT NULL,
  `last_name`  TEXT NOT NULL,
  `street`     TEXT NOT NULL,
  `city`       TEXT NOT NULL,
  `state`      TEXT NOT NULL,
  `zip`        TEXT NOT NULL,
  `phone`      TEXT NOT NULL,
  PRIMARY KEY (`email`)
);

INSERT INTO `Customer`
	(`email`, `first_name`, `last_name`, `street`, `city`, `state`, `zip`, `phone`)
VALUES
	( 'jiaxun.song@outlook.com', 'Jiaxun', 'Song', '605 Ohlone Ave Apt 629', 'Albany', 'CA', '94706', '5105410128'),
	( 'alice@outlook.com', 'Alice', 'Yang', '605 Ohlone Ave Apt 629', 'Berkeley', 'CA', '94706', '5105410128');

CREATE TABLE `Payment` (
  `payment_id` INTEGER NOT NULL,
  `method`     TEXT    NOT NULL,
  `url`        TEXT    NOT NULL,
  PRIMARY KEY (`payment_id`)
);

INSERT INTO `Payment`
	(`payment_id`, `method`, `url`)
VALUES
	( 1, 'Venmo', 'venmo.com'),
	( 2, 'WeChat', 'wechat.com');

CREATE TABLE `Order` (
  `order_id`    INTEGER NOT NULL,
  `email`       TEXT    NOT NULL,
  `create_date` TEXT    NOT NULL,
  `total_price` REAL    NOT NULL,
  `paid`        INTEGER NOT NULL,
  `payment_id`  INTEGER NOT NULL,
  PRIMARY KEY (`order_id`)
);

CREATE TABLE `Box` (
  `box_id`       INTEGER NOT NULL,
  `candy_name`   TEXT    NOT NULL,
  `candy_amount` INTEGER NOT NULL,
  PRIMARY KEY (`box_id`, `candy_name`)
);

CREATE TABLE `Password` (
  `email`    TEXT NOT NULL,
  `password` TEXT NOT NULL,
  PRIMARY KEY (`email`)
);

INSERT INTO `Password`
	(`email`, `password`)
VALUES
	( 'jiaxun.song@outlook.com', '12345678'),
	( 'alice@outlook.com', '87654321');