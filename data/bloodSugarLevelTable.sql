CREATE TABLE `blood_sugar_level` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `date` date UNIQUE NOT NULL,
  `breakfast` int,
  `after_breakfast` int,
  `lunch` int,
  `after_lunch` int,
  `dinner` int,
  `after_dinner` int,
  `extra` int,
  `comment` varchar(256)
);