FEW_SHOT_EXAMPLES = [
    {
        "input": "How many passengers are in the database?",
        "query": "SELECT COUNT(*) FROM public.\"passenger\";"
    },
    {
        "input": "What are the departure times of all flights?",
        "query": "SELECT \"time_out\" FROM public.\"trip\""
    },
    {
        "input": "What is John's place?",
        "query": "SELECT \"place\" FROM public.\"pass_in_trip\" JOIN public.\"passenger\" ON public.\"passenger\".\"id\" = public.\"pass_in_trip\".\"passenger\" WHERE public.\"passenger\".\"name\" = \'John\'"
    },
    {
        "input": "Give me all information about airlines",
        "query": "SELECT * FROM public.\"company\""
    },
    {
        "input": "Show me all the trips that are flying out today",
        "query": "SELECT * FROM public.\"trip\"\nWHERE EXTRACT(DAY FROM NOW()) = EXTRACT(DAY FROM \"time_out\")"
    },
    {
        "input": "Which planes depart from Washington?",
        "query": "SELECT \"plane\" FROM public.\"trip\" WHERE \"town_from\" = \'Washington\'"
    },
    {
        "input": "Print out the names of all the planes",
        "query": "SELECT \"plane\" FROM public.\"trip\""
    },
    {
        "input": "How many people fly on Airbus?",
        "query": "SELECT COUNT(*) FROM public.\"pass_in_trip\" AS paip JOIN public.\"trip\" ON trip.\"passenger_id\" = paip.\"trip\" WHERE trip.\"plane\" = \'Airbus\'"
    },
    {
        "input": "List all companies.",
        "query": "SELECT * FROM \"company\";"
    },
    {
        "input": "List all passengers.",
        "query": "SELECT * FROM \"passenger\";"
    },
    {
        "input": "List all trips.",
        "query": "SELECT * FROM \"trip\";"
    },
    {
        "input": "List all passengers on a specific trip with ID 123.",
        "query": "SELECT p.* FROM \"passenger\" p INNER JOIN \"pass_in_trip\" pt ON p.id = pt.\"passenger\" WHERE pt.\"trip\" = 123;"
    },
    {
        "input": "List all trips from 'New York' to 'Los Angeles'.",
        "query": "SELECT * FROM \"trip\" WHERE \"town_from\" = 'New York' AND \"town_to\" = 'Los Angeles';"
    },
    {
        "input": "List all passengers who traveled with 'Jet Airways'.",
        "query": "SELECT DISTINCT p.* FROM \"passenger\" p INNER JOIN \"pass_in_trip\" pt ON p.\"passenger_id\" = pt.\"passenger\" INNER JOIN \"trip\" t ON pt.\"trip\" = p.\"trip_id\" INNER JOIN \"company\" c ON t.\"company\" = p.\"company_id\" WHERE p.\"company_name\" = 'Jet Airways';"
    },
    {
        "input": "List all trips where 'John Smith' was a passenger.",
        "query": "SELECT t.* FROM \"trip\" t INNER JOIN \"pass_in_trip\" pt ON p.\"trip_id\" = pt.\"trip\" INNER JOIN \"passenger\" p ON pt.\"passenger\" = p.\"passenger_id\" WHERE p.\"passenger_name\" = 'John Smith';"
    },
    {
        "input": "List all passengers who traveled from 'Chicago' to 'San Francisco' on 'Delta Airlines'.",
        "query": "SELECT DISTINCT p.* FROM \"passenger\" p INNER JOIN \"pass_in_trip\" pt ON p.\"passenger_id\" = pt.\"passenger\" INNER JOIN trip t ON pt.\"trip\" = p.\"trip_id\" INNER JOIN company c ON t.\"company\" = p.\"company_id\" WHERE t.\"town_from\" = 'Chicago' AND t.\"town_to\" = 'San Francisco' AND p.\"company_name\" = 'Delta Airlines';"
    },
    {
        "input": "List all trips that departed after '2024-01-01 00:00:00'.",
        "query": "SELECT * FROM \"trip\" WHERE \"time_out\" > '2024-01-01 00:00:00';"
    },
    {
        "input": "List all passengers who traveled with 'Air Canada' and sat in seat 'A3'.",
        "query": "SELECT DISTINCT p.* FROM \"passenger\" p INNER JOIN \"pass_in_trip\" pt ON p.\"passenger_id\" = pt.\"passenger\" INNER JOIN \"trip\" t ON pt.\"trip\" = p.\"trip_id\" INNER JOIN \"company\" c ON t.\"company\" = p.\"company_id\" WHERE p.\"company_name\" = 'Air Canada' AND pt.\"place\" = 'A3';"
    },
    {
        "input": "List all companies.",
        "query": "SELECT * FROM \"company\";"
    },
    {
        "input": "List all passengers.",
        "query": "SELECT * FROM \"passenger\";"
    },
    {
        "input": "List all trips.",
        "query": "SELECT * FROM \"trip\";"
    },
    {
        "input": "List all passengers on a specific trip, including their names and places they occupy.",
        "query": "SELECT p.\"passenger_name\", pit.\"place\" FROM \"passenger\" p JOIN \"pass_in_trip\" pit ON p.\"passenger_id\" = pit.\"passenger\" WHERE pit.\"trip\" = <trip_id>;"
    },
    {
        "input": "List all trips from a specific town.",
        "query": "SELECT * FROM \"trip\" WHERE \"town_from\" = '<town_name>';"
    },
    {
        "input": "List all trips operated by a specific company.",
        "query": "SELECT * FROM \"trip\" WHERE \"company\" = <company_id>;"
    },
    {
        "input": "List all passengers who have taken trips operated by a specific company.",
        "query": "SELECT DISTINCT p.* FROM \"passenger\" p JOIN \"pass_in_trip\" pit ON p.\"passenger_id\" = pit.\"passenger\" JOIN \"trip\" t ON pit.\"trip\" = p.\"trip_id\" WHERE t.\"company\" = <company_id>;"
    },
    {
        "input": "List all trips where a specific passenger is booked.",
        "query": "SELECT t.* FROM \"trip\" t JOIN \"pass_in_trip\" pit ON p.\"trip_id\" = pit.\"trip\" WHERE pit.\"passenger\" = <passenger_id>;"
    },
    {
        "input": "List all trips where a specific passenger is booked, along with the company information.",
        "query": "SELECT t.*, p.\"company_name\" AS \"company_name\" FROM \"trip\" t JOIN \"pass_in_trip\" pit ON p.\"trip_id\" = pit.\"trip\" JOIN \"company\" c ON t.\"company\" = p.\"company_id\" WHERE pit.\"passenger\" = <passenger_id>;"
    },
    {
        "input": "List all passengers who have traveled from a specific town to another specific town.",
        "query": "SELECT DISTINCT p.* FROM \"passenger\" p JOIN \"pass_in_trip\" pit ON p.\"passenger_id\" = pit.\"passenger\" JOIN \"trip\" t ON pit.\"trip\" = p.\"trip_id\" WHERE t.\"town_from\" = '<town_from>' AND t.\"town_to\" = '<town_to>';"
    }
]
