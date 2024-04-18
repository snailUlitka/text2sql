INSERT INTO public."passenger" (passenger_name) VALUES
	('John'),
	('James'),
	('Poul'),
	('Christofer'),
	('Superman');

INSERT INTO public."company" (company_name) VALUES
	('American Airlines');

INSERT INTO public."trip" (company_id, plane, town_from, town_to, time_out, time_in) VALUES
	(4, 'Airbus', 'Washington', 'California', TIMESTAMP WITH TIME ZONE '14.02.2021', NOW());

INSERT INTO public."pass_in_trip" (trip_id, passenger_id, place) VALUES
	(3, 18, 'A11');