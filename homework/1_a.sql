--1(a)
SELECT 
	EXTRACT(HOUR FROM DateTime) AS hour, 
	SUM(Throughput) AS trips
FROM hw1.rides2017
GROUP BY EXTRACT(HOUR FROM DateTime);
--1(b)
SELECT 
	Origin, Destination, SUM(Throughput) AS Total
FROM hw1.rides2017
WHERE EXTRACT(DOW FROM DateTime)>=1 AND EXTRACT(DOW FROM DateTime)<=5 
GROUP BY Origin, Destination
ORDER BY Total DESC
LIMIT 1;
--1(c)
SELECT 
	Destination, AVG(Throughput) AS Average
FROM hw1.rides2017
WHERE EXTRACT(DOW FROM DateTime)=1 AND EXTRACT(HOUR FROM DateTime)>=7 AND EXTRACT(HOUR FROM DateTime)<10
GROUP BY Destination
ORDER BY average DESC
LIMIT 5;
