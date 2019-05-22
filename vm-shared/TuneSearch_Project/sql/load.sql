--\copy artist FROM '/home/cs143/data/artist.csv' DELIMITER ',' QUOTE '"' CSV;
--\copy song   FROM '/home/cs143/data/song.csv'   DELIMITER ',' QUOTE '"' CSV;
--\copy token  FROM '/home/cs143/data/token.csv'  DELIMITER ',' QUOTE '"' CSV;
DROP TABLE IF EXISTS tfidf;
SELECT A.song_id AS song_id ,A.token AS token, 
	CAST(A.count*LOG((SELECT CAST(COUNT(song_id) AS float) FROM song)/df) AS float)AS score
INTO tfidf 
FROM token A
JOIN 
	(SELECT token, CAST(COUNT(song_id) AS float) AS df
	FROM token
	GROUP BY token) B
ON A.token=B.token;


