INSERT INTO
    public."passenger" (passenger_name)
VALUES
    ('John'),
    ('James'),
    ('Poul'),
    ('Christofer'),
    ('Superman'),
    ('Donald'),
    ('Douglas'),
    ('Dwight'),
    ('Earl'),
    ('Edgar'),
    ('Edmund'),
    ('Edwin'),
    ('Elliot'),
    ('Eric'),
    ('Ernest'),
    ('Ethan'),
    ('Ezekiel'),
    ('Felix'),
    ('Franklin'),
    ('Frederick'),
    ('Gabriel'),
    ('Joseph'),
    ('Joshua'),
    ('Julian'),
    ('Alice'),
    ('Bob'),
    ('Charlie'),
    ('David'),
    ('Emily'),
    ('Frank'),
    ('George'),
    ('Helen'),
    ('Irene'),
    ('Jack'),
    ('Kate'),
    ('Leo'),
    ('Mary'),
    ('Nancy'),
    ('Oliver'),
    ('Paul'),
    ('Qiana'),
    ('Robert'),
    ('Samantha'),
    ('Thomas'),
    ('Victoria');

INSERT INTO
    public."company" (company_name)
VALUES
    ('American Airlines'),
    ('S7 Airlines'),
    ('Nordwind Airlines');

INSERT INTO
    public."trip" (
        company_id,
        plane,
        town_from,
        town_to,
        time_out,
        time_in
    )
VALUES
    (
        1,
        'Airbus A320',
        'Washington',
        'California',
        TIMESTAMP WITH TIME ZONE '14.02.2021',
        TIMESTAMP WITH TIME ZONE '15.02.2021'
    ),
    (
        2,
        'Airbus A321-100',
        'Tokio',
        'Paris',
        TIMESTAMP WITH TIME ZONE '04.05.2022',
        TIMESTAMP WITH TIME ZONE '05.05.2022'
    ),
    (
        3,
        'Airbus A319',
        'Gongkong',
        'Riga',
        TIMESTAMP WITH TIME ZONE '30.12.2023',
        TIMESTAMP WITH TIME ZONE '31.12.2023'
    );

INSERT INTO
    public."pass_in_trip" (trip_id, passenger_id, place)
VALUES
    (1, 1, 'A1'),
    (1, 2, 'A2'),
    (1, 3, 'A3'),
    (1, 4, 'A4'),
    (1, 5, 'A5'),
    (1, 6, 'A6'),
    (1, 7, 'A7'),
    (1, 8, 'A8'),
    (1, 9, 'A9'),
    (1, 10, 'B1'),
    (1, 11, 'B2'),
    (1, 12, 'B3'),
    (1, 13, 'B4'),
    (1, 14, 'B5'),
    (1, 15, 'B6'),
    
    (2, 16, 'A1'),
    (2, 17, 'A2'),
    (2, 18, 'A3'),
    (2, 19, 'A4'),
    (2, 20, 'A5'),
    (2, 21, 'A6'),
    (2, 22, 'A7'),
    (2, 23, 'A8'),
    (2, 24, 'A9'),
    (2, 25, 'B1'),
    (2, 26, 'B2'),
    (2, 27, 'B3'),
    (2, 28, 'B4'),
    (2, 29, 'B5'),
    (2, 30, 'B6'),

    (3, 31, 'A1'),
    (3, 32, 'A2'),
    (3, 33, 'A3'),
    (3, 34, 'A4'),
    (3, 35, 'A5'),
    (3, 36, 'A6'),
    (3, 37, 'A7'),
    (3, 38, 'A8'),
    (3, 39, 'A9'),
    (3, 40, 'B1'),
    (3, 41, 'B2'),
    (3, 42, 'B3'),
    (3, 43, 'B4'),
    (3, 44, 'B5'),
    (3, 45, 'B6');