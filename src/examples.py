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
        "query": "SELECT COUNT(*) FROM public.\"pass_in_trip\" AS paip JOIN public.\"trip\" ON trip.\"id\" = paip.\"trip\" WHERE trip.\"plane\" = \'Airbus\'"
    },
]