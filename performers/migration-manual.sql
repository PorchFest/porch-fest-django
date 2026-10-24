porchfest=# BEGIN;
BEGIN
porchfest=*# INSERT INTO performers_performer (
    id, name, bio, member_count, instruments, link, slug,
    profile_picture, email, phone_number, created_by_id, user_id
)
porchfest-*# SELECT
    id, name, bio, member_count, instruments, link, slug,
    profile_picture, email, phone_number, created_by_id, user_id
FROM porchfestcore_performer;
INSERT 0 502
porchfest=*# INSERT INTO performers_genre (id, name, slug)
SELECT id, name, slug
FROM porchfestcore_genre;
INSERT 0 51
porchfest=*# INSERT INTO performers_performer_genres (performer_id, genre_id)
SELECT performer_id, genre_id
FROM porchfestcore_performer_genres;
INSERT 0 373
porchfest=*# COMMIT:
porchfest-*# SELECT 'performers' AS item, COUNT(*) FROM performers_performer
UNION ALL
SELECT 'genres', COUNT(*) FROM performers_genre
UNION ALL
SELECT 'genre assignments', COUNT(*) FROM performers_performer_genres;
ERROR:  syntax error at or near ":"
LINE 1: COMMIT:
              ^
porchfest=!# COMMIT;
ROLLBACK
porchfest=# ROLLBACK;
WARNING:  there is no transaction in progress
ROLLBACK
porchfest=# BEGIN;
BEGIN
porchfest=*# INSERT INTO performers_performer (
    id, name, bio, member_count, instruments, link, slug,
    profile_picture, email, phone_number, created_by_id, user_id
)
SELECT
    id, name, bio, member_count, instruments, link, slug,
    profile_picture, email, phone_number, created_by_id, user_id
FROM porchfestcore_performer;
INSERT 0 502
porchfest=*# INSERT INTO performers_genre (id, name, slug)
SELECT id, name, slug
FROM porchfestcore_genre;
INSERT 0 51
porchfest=*# INSERT INTO performers_performer_genres (performer_id, genre_id)
SELECT performer_id, genre_id
FROM porchfestcore_performer_genres;
INSERT 0 373
porchfest=*# COMMIT;
COMMIT
porchfest=# SELECT 'performers' AS item, COUNT(*) FROM performers_performer
UNION ALL
SELECT 'genres', COUNT(*) FROM performers_genre
UNION ALL
SELECT 'genre assignments', COUNT(*) FROM performers_performer_genres;
       item        | count 
-------------------+-------
 performers        |   502
 genres            |    51
 genre assignments |   373
(3 rows)

porchfest=# SELECT setval(
    pg_get_serial_sequence('performers_genre', 'id'),
    (SELECT MAX(id) FROM performers_genre)
);
 setval 
--------
     64
(1 row)

porchfest=# SELECT COUNT(*)
FROM performers_performer p
LEFT JOIN performers_performer_genres pg
    ON pg.performer_id = p.id
LEFT JOIN performers_genre g
    ON g.id = pg.genre_id
WHERE pg.performer_id IS NOT NULL
  AND g.id IS NULL;
 count 
-------
     0
(1 row)