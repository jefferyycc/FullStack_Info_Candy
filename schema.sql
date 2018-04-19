DROP TABLE IF EXISTS `Password`;
DROP TABLE IF EXISTS `Payment`;
DROP TABLE IF EXISTS `Candy`;
DROP TABLE IF EXISTS `Item`;
DROP TABLE IF EXISTS `DefaultBox`;
DROP TABLE IF EXISTS `DIYBox`;
DROP TABLE IF EXISTS `Customer`;
DROP TABLE IF EXISTS `Order`;

CREATE TABLE `Item` (
  `box_id`   INTEGER NOT NULL,
  `order_id` INTEGER NOT NULL,
  `quantity` INTEGER NOT NULL,
  PRIMARY KEY (`box_id`),
  FOREIGN KEY (`order_id`) REFERENCES `Order`(`order_id`)
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
	( 'Milk',       100, 'Milk',            2.5),
	( 'Chocolate',  150, 'White chocolate', 2.0),
	( 'Almond',     120, 'Almond',          2.8),
	( 'Caramel',    160, 'Sugar',           1.5);

CREATE TABLE `Customer` (
  `email`      TEXT NOT NULL,
  `first_name` TEXT NOT NULL,
  `last_name`  TEXT NOT NULL,
  `street1`    TEXT NOT NULL,
  `street2`    TEXT,
  `city`       TEXT NOT NULL,
  `state`      TEXT NOT NULL,
  `zip`        TEXT NOT NULL,
  `phone`      TEXT NOT NULL,
  PRIMARY KEY (`email`)
);

INSERT INTO `Customer`
	(`email`, `first_name`, `last_name`, `street1`, `street2`, `city`, `state`, `zip`, `phone`)
VALUES
	( 'jiaxun.song@outlook.com', 'Jiaxun', 'Song', '605 Ohlone Ave Apt 629', NULL, 'Albany', 'CA', '94706', '5105410128'),
	( 'alice@outlook.com', 'Alice', 'Yang', '605 Ohlone Ave Apt 629', NULL, 'Berkeley', 'CA', '94706', '5105410128');

CREATE TABLE `Payment` (
  `payment_id` INTEGER NOT NULL,
  `method`     TEXT    NOT NULL,
  PRIMARY KEY (`payment_id`)
);

INSERT INTO `Payment`
	(`payment_id`, `method`)
VALUES
	( 1, 'Venmo'),
	( 2, 'WeChat');

CREATE TABLE `Order` (
  `order_id`    INTEGER NOT NULL,
  `email`       TEXT    NOT NULL,
  `create_date` TEXT    NOT NULL,
  `total_price` REAL    NOT NULL,
  `discount`    REAL    NOT NULL,
  `paid`        INTEGER NOT NULL,
  `payment_id`  INTEGER NOT NULL,
  PRIMARY KEY (`order_id`),
  FOREIGN KEY (`email`) REFERENCES `Customer`(`email`),
  FOREIGN KEY (`payment_id`) REFERENCES `Payment`(`payment_id`)
);

-- merge DIY box and default box
CREATE TABLE `DIYBox` (
  `box_id`       INTEGER NOT NULL,
  `candy_name`   TEXT    NOT NULL,
  `candy_amount` INTEGER NOT NULL,
  PRIMARY KEY (`box_id`, `candy_name`),
  FOREIGN KEY (`candy_name`) REFERENCES `Candy`(`candy_name`)
);

CREATE TABLE `DefaultBox` (
  `box_id`       INTEGER NOT NULL,
  `candy_name`   TEXT    NOT NULL,
  `candy_amount` INTEGER NOT NULL,
  PRIMARY KEY (`box_id`, `candy_name`),
  FOREIGN KEY (`candy_name`) REFERENCES `Candy`(`candy_name`)
);

-- 6 boxes
INSERT INTO `DefaultBox`
	(`box_id`, `candy_name`, `candy_amount`)
VALUES
	( 1, 'Milk', 5),
	( 1, 'Chocolate', 5),
	( 1, 'Almond', 5),
	( 2, 'Chocolate', 5),
	( 3, 'Almond', 5),
	( 4, 'Caramel', 5);

CREATE TABLE `Password` (
  `email`    TEXT NOT NULL,
  `password` TEXT NOT NULL,
  PRIMARY KEY (`email`),
  FOREIGN KEY (`email`) REFERENCES `Customer`(`email`)
);

INSERT INTO `Password`
	(`email`, `password`)
VALUES
	( 'jiaxun.song@outlook.com', '12345678'),
	( 'alice@outlook.com', '87654321');