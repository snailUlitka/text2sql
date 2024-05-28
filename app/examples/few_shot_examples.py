"""Stores an array with examples for use in the Few-Shots method."""
FEW_SHOT_EXAMPLES = [
    {
        "input": "How many passengers are in the database?",
        "query": "SELECT COUNT(*) FROM public.\"passenger\";"
    },
    {
        "input": "What are the departure times of all flights?",
        "query": "SELECT \"time_out\" FROM public.\"trip\";"
    },
    {
        "input": "What is John's place?",
        "query": "SELECT \"place\" FROM public.\"pass_in_trip\"" +
            "JOIN public.\"passenger\" ON public.\"passenger\"." +
            "\"passenger_id\" = public.\"pass_in_trip\".\"passenger_id\" " +
            "WHERE public.\"passenger\".\"passenger_name\" = \'John\';"
    },
    {
        "input": "Give me all the information about 1 company",
        "query": "SELECT * FROM public.\"company\" LIMIT 1;"
    },
    {
        "input": "Show me all the trips that are flying out today",
        "query": "SELECT * FROM public.\"trip\" WHERE EXTRACT(DAY " +
            "FROM NOW()) = EXTRACT(DAY FROM \"time_out\");"
    },
    {
        "input": "Which planes depart from Washington?",
        "query": "SELECT \"plane\" FROM public.\"trip\" WHERE \"town_from\" = \'Washington\';"
    },
    {
        "input": "Print out the names of all the planes",
        "query": "SELECT \"plane\" FROM public.\"trip\" LIMIT 20;"
    },
    {
        "input": "How many people fly on Airbus A320?",
        "query": "SELECT COUNT(*) FROM public.\"pass_in_trip\"" +
            " AS paip JOIN public.\"trip\" ON trip.\"trip_id\"" +
            " = paip.\"trip_id\" WHERE trip.\"plane\" = \'Airbus A320\';"
    },
    {
        "input": "List all companies.",
        "query": "SELECT DISTINCT \"company_name\" FROM \"company\" LIMIT 20;"
    },
    {
        "input": "List all passengers.",
        "query": "SELECT DISTINCT \"passenger_name\" FROM \"passenger\" LIMIT 20;"
    },
    {
        "input": "List all trips.",
        "query": "SELECT DISTINCT \"plane\", \"town_from\", \"town_to\", " + 
            "\"time_out\", \"time_in\" FROM \"trip\" LIMIT 20;"
    },
    {
        "input": "List all passengers on a specific trip with ID 123.",
        "query": "SELECT p.* FROM \"passenger\" p INNER JOIN \"pass_in_trip\"" +
            " pt ON p.\"passenger_id\" = pt.\"passenger_id\" WHERE pt.\"trip_id\" = 123 LIMIT 20;"
    },
    {
        "input": "List all trips from \'New York\' to \'Los Angeles\'.",
        "query": "SELECT \"plane\", \"town_from\", \"town_to\", \"time_out\"," + 
            " \"time_in\" FROM \"trip\" WHERE \"town_from\" = 'New York' AND" +
            " \"town_to\" = \'Los Angeles\' LIMIT 20;"
    },
    {
        "input": "List all passengers who traveled with \'Jet Airways\'.",
        "query": "SELECT DISTINCT p.\"passenger_name\" FROM \"passenger\"" +
            " p INNER JOIN \"pass_in_trip\" pt ON p.\"passenger_id\" = " +
            "pt.\"passenger_id\" INNER JOIN \"trip\" t ON pt.\"trip_id\"" +
            " = p.\"trip_id\" INNER JOIN \"company\" c ON t.\"company_id\"" +
            " = p.\"company_id\" WHERE p.\"company_name\" = \'Jet Airways\' LIMIT 20;"
    },
    {
        "input": "List all trips where \'John Smith\' was a passenger.",
        "query": "SELECT t.* FROM \"trip\" t INNER JOIN \"pass_in_trip\"" +
            " pt ON p.\"trip_id\" = pt.\"trip_id\" INNER JOIN \"passenger\"" + 
            " p ON pt.\"passenger_id\" = p.\"passenger_id\" WHERE " + 
            "p.\"passenger_name\" = \'John Smith\' LIMIT 20;"
    },
    {
        "input": "List all passengers who traveled from \'Chicago\'" +
            " to \'San Francisco\' on \'Delta Airlines\'.",
        "query": "SELECT DISTINCT p.\"passenger\" FROM \"passenger\" p INNER JOIN" +
            " \"pass_in_trip\" pt ON p.\"passenger_id\" = pt.\"passenger_id\"" +
            " INNER JOIN trip t ON pt.\"trip_id\" = p.\"trip_id\" INNER JOIN" +
            " company c ON t.\"company_id\" = p.\"company_id\" WHERE t.\"town_from\"" +
            " = \'Chicago\' AND t.\"town_to\" = \'San Francisco\' AND p.\"company_name\"" +
            " = \'Delta Airlines\' LIMIT 20;"
    },
    {
        "input": "List all trips that departed after \'2024-01-01 00:00:00\'.",
        "query": "SELECT * FROM \"trip\" WHERE \"time_out\" > \'2024-01-01 00:00:00\' LIMIT 20;"
    },
    {
        "input": "List all passengers who traveled with 'Air Canada' and sat in seat 'A3'.",
        "query": "SELECT DISTINCT p.\"passenger_name\" FROM \"passenger\" p INNER JOIN \"pass_in_trip\"" + 
            " pt ON p.\"passenger_id\" = pt.\"passenger_id\" INNER JOIN \"trip\" t ON " +
            "pt.\"trip_id\" = p.\"trip_id\" INNER JOIN \"company\" c ON t.\"company_id\" " +
            "= p.\"company_id\" WHERE p.\"company_name\" = \'Air Canada\' AND " +
            "pt.\"place\" = \'A3\' LIMIT 20;"
    },
]
