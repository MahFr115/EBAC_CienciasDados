--Select * from pg_tables
--SELECT * FROM actor
--SELECT * FROM film_actor
--SELECT * FROM film

-- rental_duration
-- rental_rate
-- length
-- replacement_cost

------------------------------------------------------------------------------------
SELECT first_name, last_name, AVG(rental_duration) AS avg_duration, AVG(rental_rate) AS avg_rate, 
AVG(f.length) AS avg_length, AVG(replacement_cost) AS avg_cost
FROM actor AS a INNER JOIN film_actor as fa ON a.actor_id = fa.actor_id
INNER JOIN film AS f ON fa.film_id = f.film_id
GROUP BY first_name, last_name