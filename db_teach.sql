-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Дек 16 2023 г., 16:10
-- Версия сервера: 8.0.35-0ubuntu0.22.04.1
-- Версия PHP: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `db_teach`
--

-- --------------------------------------------------------

--
-- Структура таблицы `lessons`
--

CREATE TABLE `lessons` (
  `id` int NOT NULL,
  `teacher_id` int NOT NULL,
  `student_id` int NOT NULL,
  `lesson_date` datetime NOT NULL,
  `price` int NOT NULL,
  `status` smallint NOT NULL DEFAULT '0',
  `old_lesson_date` datetime DEFAULT NULL,
  `count_changes` smallint NOT NULL DEFAULT '0',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_id` int DEFAULT NULL,
  `homework_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `lessons`
--

INSERT INTO `lessons` (`id`, `teacher_id`, `student_id`, `lesson_date`, `price`, `status`, `old_lesson_date`, `count_changes`, `description`, `media_id`, `homework_id`) VALUES
(51, 1, 5, '2023-12-11 19:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(52, 1, 5, '2023-12-18 19:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(53, 1, 5, '2023-12-25 19:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(54, 1, 5, '2023-12-10 20:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(55, 1, 5, '2023-12-17 20:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(56, 1, 5, '2023-12-24 20:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(57, 1, 5, '2023-12-31 20:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(58, 1, 6, '2023-12-11 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(59, 1, 6, '2023-12-18 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(60, 1, 6, '2023-12-25 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(61, 1, 7, '2023-12-08 20:00:00', 1600, 0, NULL, 0, NULL, NULL, NULL),
(62, 1, 7, '2023-12-15 20:00:00', 1600, 0, NULL, 0, NULL, NULL, NULL),
(63, 1, 7, '2023-12-22 20:00:00', 1600, 0, NULL, 0, NULL, NULL, NULL),
(64, 1, 7, '2023-12-29 20:00:00', 1600, 0, NULL, 0, NULL, NULL, NULL),
(65, 1, 8, '2023-12-14 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(66, 1, 8, '2023-12-21 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(67, 1, 8, '2023-12-28 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(68, 1, 8, '2023-12-09 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(69, 1, 8, '2023-12-16 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(70, 1, 8, '2023-12-23 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(71, 1, 8, '2023-12-30 16:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(72, 1, 9, '2023-12-10 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(73, 1, 9, '2023-12-17 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(74, 1, 9, '2023-12-24 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(75, 1, 9, '2023-12-31 18:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(76, 1, 10, '2023-12-12 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(77, 1, 10, '2023-12-19 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(78, 1, 10, '2023-12-26 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(79, 1, 10, '2023-12-14 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(80, 1, 10, '2023-12-21 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(81, 1, 10, '2023-12-28 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(82, 1, 10, '2023-12-09 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(83, 1, 10, '2023-12-16 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(84, 1, 10, '2023-12-23 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(85, 1, 10, '2023-12-30 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(86, 1, 11, '2023-12-13 12:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(87, 1, 11, '2023-12-20 12:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(88, 1, 11, '2023-12-27 12:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(89, 1, 11, '2023-12-10 17:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(90, 1, 11, '2023-12-17 17:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(91, 1, 11, '2023-12-24 17:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(92, 1, 11, '2023-12-31 17:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(93, 1, 12, '2023-12-14 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(94, 1, 12, '2023-12-21 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(95, 1, 12, '2023-12-28 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(96, 1, 12, '2023-12-09 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(97, 1, 12, '2023-12-16 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(98, 1, 12, '2023-12-23 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(99, 1, 12, '2023-12-30 15:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(100, 1, 13, '2023-12-09 17:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(101, 1, 13, '2023-12-16 17:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(102, 1, 13, '2023-12-23 17:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(103, 1, 13, '2023-12-30 17:30:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(104, 1, 14, '2023-12-12 20:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(105, 1, 14, '2023-12-19 20:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(106, 1, 14, '2023-12-26 20:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(107, 1, 15, '2023-12-08 18:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(108, 1, 15, '2023-12-15 18:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(109, 1, 15, '2023-12-22 18:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(110, 1, 15, '2023-12-29 18:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(111, 1, 15, '2023-12-10 15:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(112, 1, 15, '2023-12-17 15:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(113, 1, 15, '2023-12-24 15:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(114, 1, 15, '2023-12-31 15:00:00', 2000, 0, NULL, 0, NULL, NULL, NULL),
(115, 1, 16, '2023-12-14 14:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(116, 1, 16, '2023-12-21 14:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(117, 1, 16, '2023-12-28 14:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(118, 1, 17, '2023-12-08 12:00:00', 1800, 0, NULL, 0, NULL, NULL, NULL),
(119, 1, 17, '2023-12-15 12:00:00', 1800, 0, NULL, 0, NULL, NULL, NULL),
(120, 1, 17, '2023-12-22 12:00:00', 1800, 0, NULL, 0, NULL, NULL, NULL),
(121, 1, 17, '2023-12-29 12:00:00', 1800, 0, NULL, 0, NULL, NULL, NULL),
(122, 1, 14, '2023-12-08 19:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(123, 1, 14, '2023-12-15 19:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(124, 1, 14, '2023-12-22 19:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(125, 1, 14, '2023-12-29 19:00:00', 1000, 0, NULL, 0, NULL, NULL, NULL),
(126, 4, 18, '2023-12-11 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(127, 4, 18, '2023-12-18 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(128, 4, 18, '2023-12-25 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(129, 4, 18, '2023-12-09 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(130, 4, 18, '2023-12-16 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(131, 4, 18, '2023-12-23 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(132, 4, 18, '2023-12-30 17:00:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(133, 4, 19, '2023-12-09 16:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(134, 4, 19, '2023-12-16 16:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(135, 4, 19, '2023-12-23 16:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(136, 4, 19, '2023-12-30 16:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(137, 4, 19, '2023-12-12 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(138, 4, 19, '2023-12-19 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(139, 4, 19, '2023-12-26 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(140, 4, 20, '2023-12-11 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(141, 4, 20, '2023-12-18 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(142, 4, 20, '2023-12-25 19:00:00', 800, 0, NULL, 0, NULL, NULL, NULL),
(143, 4, 21, '2023-12-11 15:30:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(144, 4, 21, '2023-12-18 15:30:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(145, 4, 21, '2023-12-25 15:30:00', 500, 0, NULL, 0, NULL, NULL, NULL),
(146, 4, 22, '2023-12-12 15:00:00', 700, 0, NULL, 0, NULL, NULL, NULL),
(147, 4, 22, '2023-12-19 15:00:00', 700, 0, NULL, 0, NULL, NULL, NULL),
(148, 4, 22, '2023-12-26 15:00:00', 700, 0, NULL, 0, NULL, NULL, NULL),
(149, 4, 22, '2023-12-15 14:00:00', 700, 0, NULL, 0, NULL, NULL, NULL),
(150, 4, 22, '2023-12-22 14:00:00', 700, 0, NULL, 0, NULL, NULL, NULL),
(151, 4, 22, '2023-12-29 14:00:00', 700, 0, NULL, 0, NULL, NULL, NULL),
(152, 4, 23, '2023-12-12 18:00:00', 600, 0, NULL, 0, NULL, NULL, NULL),
(153, 4, 23, '2023-12-19 18:00:00', 600, 0, NULL, 0, NULL, NULL, NULL),
(154, 4, 23, '2023-12-26 18:00:00', 600, 0, NULL, 0, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `media`
--

CREATE TABLE `media` (
  `id` int NOT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `media_1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `media_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_6` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_7` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_8` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_9` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `media_10` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `students`
--

CREATE TABLE `students` (
  `id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `registration_date` datetime DEFAULT NULL,
  `class` smallint NOT NULL,
  `purpose` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `price` int NOT NULL,
  `transfer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `platform` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `platform_nick` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `timezone` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `teacher_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `students`
--

INSERT INTO `students` (`id`, `user_id`, `name`, `subject`, `registration_date`, `class`, `purpose`, `price`, `transfer`, `phone`, `platform`, `platform_nick`, `timezone`, `teacher_id`) VALUES
(5, 100, 'Алиса', 'Математика', '2023-12-08 00:42:49', 10, 'ЕГЭ Профиль', 500, 'Сергей Валерьевич В.', 'None', 'Discord', 'Alice-Vaniushkina', '+0', 1),
(6, 101, 'Максим', 'Математика', '2023-12-08 00:45:57', 9, 'ОГЭ', 1000, 'Иляна Сергеевна Р.', 'None', 'Discord', 'Hshfda', '+0', 1),
(7, 102, 'Вова', 'Математика', '2023-12-08 00:47:52', 3, 'Повышение успеваемости', 1600, 'None', 'None', 'Discord', 'Vova075', '+0', 1),
(8, 104, 'Катя', 'Математика', '2023-12-08 00:49:53', 8, 'Повышение успеваемости', 1000, 'None', 'None', 'Discord', 'karga', '+4', 1),
(9, 105, 'Артем Крестинин', 'Математика', '2023-12-08 00:52:24', 9, 'ОГЭ', 1000, 'None', 'None', 'Discord', 'tomai', '+0', 1),
(10, 106, 'Артем М', 'Математика', '2023-12-08 00:54:19', 9, 'ОГЭ, Повышение успеваемости', 800, 'None', 'None', 'Discord', 'wystrez', '+0', 1),
(11, 107, 'Артем', 'Математика', '2023-12-08 00:57:42', 8, 'Повышение успеваемости', 1000, 'Наталья Саулюсовна К.', 'None', 'Discord', 'aboba', '+4', 1),
(12, 108, 'Александр', 'Математика', '2023-12-08 00:59:38', 11, 'ЕГЭ Профиль', 1000, 'None', 'None', 'Discord', 'Александр', '+0', 1),
(13, 109, 'Анастасия', 'Геометрия', '2023-12-08 01:01:13', 8, 'Повышение успеваемости', 1000, 'None', 'None', 'Discord', 'None', '+0', 1),
(14, 110, 'Егор', 'Математика', '2023-12-08 01:02:50', 11, 'ЕГЭ Профиль', 1000, 'Светлана Дмитриевна С.', 'None', 'Discord', 'sattagez', '+0', 1),
(15, 111, 'Арсений', 'Математика', '2023-12-08 01:04:42', 5, 'Повышение успеваемости', 2000, 'Светлана Викторовна О.', 'None', 'Discord', 'Арсений', '+0', 1),
(16, 112, 'Елисей', 'Математика', '2023-12-08 01:06:25', 7, 'Повышение успеваемости', 1000, 'None', 'None', 'Discord', 'FID_ZERO', '+0', 1),
(17, 113, 'Мария', 'Математика', '2023-12-08 01:08:20', 11, 'ЕГЭ База', 1800, 'Ольга Леонидовна С.', 'None', 'Discord', 'Maria', '+0', 1),
(18, 120, 'Артём', 'Физика', '2023-12-09 19:57:10', 8, 'Повышение успеваемости', 500, 'None', 'None', 'Discord', 'None', '+0', 4),
(19, 121, 'Ислам', 'Физика', '2023-12-09 19:59:56', 7, 'Повышение успеваемости', 800, 'None', 'None', 'Discord', 'None', '+0', 4),
(20, 122, 'Аня', 'Физика', '2023-12-09 20:01:49', 9, 'Повышение успеваемости', 800, 'None', 'None', 'Интерактивная доска', 'None', '+0', 4),
(21, 123, 'Полина', 'Физика', '2023-12-09 20:03:07', 7, 'Повышение успеваемости', 500, 'None', 'None', 'Discord', 'None', '+0', 4),
(22, 124, 'Яна', 'Физика', '2023-12-09 20:04:28', 8, 'Повышение успеваемости', 700, 'None', 'None', 'Discord', 'None', '+0', 4),
(23, 125, 'Алёна', 'Физика', '2023-12-09 20:06:00', 7, 'Повышение успеваемости', 600, 'None', 'None', 'Discord', 'None', '+0', 4);

-- --------------------------------------------------------

--
-- Структура таблицы `teachers`
--

CREATE TABLE `teachers` (
  `id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `registration_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `teachers`
--

INSERT INTO `teachers` (`id`, `user_id`, `name`, `subject`, `registration_date`) VALUES
(1, 812267139, 'Свиридов Евгений Сергеевич', 'Математика', '2023-09-12 00:00:00'),
(3, 1774727561, 'Арсланов Мейлис Ахмедович', 'Русский язык', '2023-09-04 04:38:09'),
(4, 534931446, 'Плешнева Татьяна Сергеевна', 'Физика', '2023-11-24 17:22:23');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `lessons`
--
ALTER TABLE `lessons`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_media_id` (`media_id`),
  ADD KEY `FK_student_id` (`student_id`),
  ADD KEY `FK_teaher_id_lesson` (`teacher_id`);

--
-- Индексы таблицы `media`
--
ALTER TABLE `media`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_teacher_id` (`teacher_id`);

--
-- Индексы таблицы `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `lessons`
--
ALTER TABLE `lessons`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=155;

--
-- AUTO_INCREMENT для таблицы `media`
--
ALTER TABLE `media`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `students`
--
ALTER TABLE `students`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT для таблицы `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `FK_media_id` FOREIGN KEY (`media_id`) REFERENCES `media` (`id`),
  ADD CONSTRAINT `FK_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `FK_teaher_id_lesson` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ограничения внешнего ключа таблицы `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `FK_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
