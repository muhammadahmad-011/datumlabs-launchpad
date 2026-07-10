select * from iris_data;
select * from species_details;

--which category or group has the highest total value? Use GROUP BY + aggregation--

select species, SUM (sepal_length_cm) as total_sepal_length
from iris_data
group by species
order by total_sepal_length DESC
LIMIT 1;

--which records meet a specific condition AND have a value above a threshold? Use WHERE + AND--

select * from iris_data
where species = 'Iris-setosa' and sepal_width_cm > 3;

--which groups have more than X records? Use GROUP BY + HAVING--

select species, count(*) as total
from iris_data
group by species
having count(*) > 10;

--which are the top 10 rows by a specific metric? Use ORDER BY + LIMIT--

select * from iris_data
order by sepal_length_cm desc
limit 10;

--write a JOIN query that combines two tables to answer a question neither could answer alone--
--What is the average petal length of flower species that prefer 'Full Sun'--
select sunlight_requirement, avg(petal_length_cm) as avg_petal_length
from iris_data i
join species_details sd on i.species = sd.species_name
where sunlight_requirement = 'Full Sun'
group by sunlight_requirement;

