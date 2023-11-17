CREATE TABLE `day` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `breakfast` int NOT NULL,
  `after_breakfast` int,
  `lunch` int NOT NULL,
  `after_lunch` int,
  `dinner` int NOT NULL,
  `after_dinner` int,
  `extra` int,
  `date` date NOT NULL,
  `month_id` int NOT NULL,
  `comment` varchar(256)
);

CREATE TABLE `month` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `mean` float NOT NULL,
  `lower` int NOT NULL,
  `higher` int NOT NULL,
  `variance` float NOT NULL,
  `standard_deviation` float NOT NULL,
  `mean_deviation` float NOT NULL,
  `target` int NOT NULL,
  `target_percent` float NOT NULL,
  `hipo` int NOT NULL,
  `hipo_percent` float NOT NULL,
  `hiper` int NOT NULL,
  `hiper_percent` float NOT NULL,
  `normal` int NOT NULL,
  `normal_percent` float NOT NULL,
  `total` int NOT NULL,
  `year_id` int NOT NULL
);

CREATE TABLE `year` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `mean` float NOT NULL,
  `lower` int NOT NULL,
  `higher` int NOT NULL,
  `variance` float NOT NULL,
  `standard_deviation` float NOT NULL,
  `mean_deviation` float NOT NULL,
  `target` int NOT NULL,
  `target_percent` float NOT NULL,
  `hipo` int NOT NULL,
  `hipo_percent` float NOT NULL,
  `hiper` int NOT NULL,
  `hiper_percent` float NOT NULL,
  `normal` int NOT NULL,
  `normal_percent` float NOT NULL,
  `total` int NOT NULL
);

ALTER TABLE `day` ADD FOREIGN KEY (`month_id`) REFERENCES `month` (`id`);

ALTER TABLE `month` ADD FOREIGN KEY (`year_id`) REFERENCES `year` (`id`);