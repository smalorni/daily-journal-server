--USED TO DELETE EXISTING TABLE AND ALL ROWS IN TABLE, DIFFERENT FROM DELETING ALL RECORDS OF TABLE
DROP TABLE IF EXISTS Entry;
DROP TABLE IF EXISTS Mood;
DROP TABLE IF EXISTS EntryTag;

-- This is the main table, mood is joining into this table by id
CREATE TABLE `Entry` (
    `id`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept`   TEXT NOT NULL,
    `entry`     TEXT NOT NULL,
    `mood_id`   INTEGER NOT NULL,
    `date`      TEXT NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

CREATE TABLE `Mood` (
    `id`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`     TEXT NOT NULL  
);

CREATE TABLE `Tag` (
    `id`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`      TEXT NOT NULL
);

CREATE TABLE `EntryTag` (
    `id`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id`  INTEGER NOT NULL,
    `tag_id`    INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tag` (`id`)
);

--The strings must be in quotes, not backticks, put dates in strings

INSERT INTO `Entry` VALUES(null, "Javascript", "Too many functions, too many never-ending loops!", 2, "Wed Sep 15 2021 10:10:47");
INSERT INTO `Entry` VALUES(null, "Python", "The snake is always sneaky. Python never works when you're missing a comma!", 3, "Fri Aug 30 2022 12:11:47");
INSERT INTO `Entry` VALUES(null, "React", "React makes lives easier!", 1, "Sun June 19 2022 05:10:47");
INSERT INTO `Entry` VALUES(null, "Ruby", "Ruby who?", 5, "Mon Oct 31 2021 09:05:47");
INSERT INTO `Entry` VALUES(null, "C", "Can you see me?", 4, "Tues Nov 10 2022 11:11:42");


INSERT INTO `Mood` VALUES(null, "Happy");
INSERT INTO `Mood` VALUES(null, "Sad");
INSERT INTO `Mood` VALUES(null, "Angry");
INSERT INTO `Mood` VALUES(null, "Calm");
INSERT INTO `Mood` VALUES(null, "Confused");

INSERT INTO `Tag` VALUES(null, "Javascript");
INSERT INTO `Tag` VALUES(null, "Python");
INSERT INTO `Tag` VALUES(null,  "Ruby");
INSERT INTO `Tag` VALUES(null, "C");
INSERT INTO `Tag` VALUES(null, "Java");
INSERT INTO `Tag` VALUES(null, "Low Stress");
INSERT INTO `Tag` VALUES(null, "Medium Stress");
INSERT INTO `Tag` VALUES(null, "High Stress");
INSERT INTO `Tag` VALUES(null, "Top Priority");

INSERT INTO `EntryTag` VALUES(null, 2, 6);
INSERT INTO `EntryTag` VALUES(null, 3, 7);
INSERT INTO `EntryTag` VALUES(null, 1, 9);
INSERT INTO `EntryTag` VALUES(null, 4, 7);
INSERT INTO `EntryTag` VALUES(null, 5, 8);



--JOIN BOTH TABLES: MOOD INTO ENTRY TABLE - MUST MATCH IN EXACT SAME ORDER AS ABOVE
SELECT
    j.id,
    j.concept,
    j.entry,
    j.mood_id,
    j.date,
    m.label
FROM Entry j
JOIN Mood m
    ON m.id = j.mood_id
JOIN EntryTag t
;

--
SELECT * FROM Entry;
SELECT * FROM Mood;