--SELECT * FROM tfidf
--LIMIT 5;
--SELECT * FROM token
--WHERE token='could' AND song_id=0;
--SELECT COUNT(song_id) FROM token
--GROUP BY token
--HAVING token='could';
--SELECT COUNT(song_id) from song;
--token

SELECT artist.artist_name AS artist_name ,C.song_name AS song_name, C.page_link AS page_link, C.total AS total
FROM
	artist
	INNER JOIN
	(SELECT song.artist_id AS artist_id, song.song_name AS song_name, song.page_link AS page_link,B.total AS total
	FROM song
	INNER JOIN
		(SELECT tfidf.song_id AS song_id, SUM(tfidf.score) AS total
		FROM tfidf
		INNER JOIN (
		SELECT song_id
		FROM token
		WHERE token IN ('she', 'is', 'right', 'like', 'bottle','lights')
		--WHERE token='she' OR token='is' OR token='right' OR token='lights' or token='like' or token='bottle'
		GROUP BY song_id
		HAVING COUNT(token)=6) A
		ON tfidf.song_id=A.song_id 
		WHERE tfidf.token='she' OR tfidf.token='is'
		GROUP BY tfidf.song_id) B
	ON song.song_id=B.song_id) C
	ON artist.artist_id=C.artist_id

ORDER BY total DESC;



SELECT artist.artist_name AS artist_name ,C.song_name AS song_name, C.page_link AS page_link, C.total AS total
                FROM
                artist
                INNER JOIN
                (SELECT song.artist_id AS artist_id, song.song_name AS song_name, song.page_link AS page_link,B.total AS total
                FROM song
                INNER JOIN
                (SELECT tfidf.song_id AS song_id, SUM(tfidf.score) AS total
                FROM tfidf
                INNER JOIN (
                SELECT song_id
                FROM token
                WHERE token IN ('she', 'is', 'right', 'like', 'bottle', 'lights')
                GROUP BY song_id
                HAVING COUNT(token)=6) A
                ON tfidf.song_id=A.song_id
                WHERE tfidf.token IN ('she', 'is', 'right', 'like', 'bottle', 'lights')
                GROUP BY tfidf.song_id) B
                ON song.song_id=B.song_id) C
                ON artist.artist_id=C.artist_id

                ORDER BY total DESC;



