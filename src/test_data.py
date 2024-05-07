"""Module with data for test LLM models"""
import db_connect


class TestData:
    """This class named TestData contains lists for `QUESTIONS`, `SQL_QUERIES`, `QUERY_RESULTS`, and `ANSWER`."""
    QUESTIONS = [
        "Print any 9 human names that are contained in the airlines database",
        "Print the names of all companies",
        "Print all planes from flights from Washington",
        "Print the names of people that end in \"man\"",
        "Print the number of flights made on Airbus A319",
        "Which companies have flown on Airbus A321-100",
        "Print all the names of the planes on which you can fly to California",
        "Which companies organize flights from Gongkong?",
        "Print the ids and the count of passengers for all past trips",
        "Which cities did Bob fly to",
        "Print the date and time of arrival of passenger John in California",
        "How many flights have airlines flown from Washington to California?",
        "Which cities can I fly to from Washington and how long will it take?",
        "Print the passengers with the longest name. Spaces, hyphens, and dots are considered part of the name",
        "Print the names of the passengers who flew to California by Airbus A320 aircraft",
    ]
    SQL_QUERIES = [
        "SELECT passenger_name FROM passenger LIMIT 9;",
        "SELECT company_name FROM company;",
        "SELECT plane FROM trip WHERE town_from = \'Washington\';",
        "SELECT passenger_name FROM passenger WHERE passenger_name LIKE \'%man\';",
        "SELECT COUNT(*) FROM trip WHERE plane = \'Airbus A319\';",
        "SELECT company_name FROM company Co LEFT JOIN trip Tr ON Tr.company_id = Co.company_id WHERE Tr.plane = \'Airbus A321-100\';",
        "SELECT plane FROM trip WHERE town_to = 'California';",
        "SELECT company_name FROM company Co LEFT JOIN trip Tr ON Tr.company_id = Co.company_id WHERE Tr.town_from = \'Gongkong\';",
        "SELECT Tr.trip_id, COUNT(PaTr.passenger_id) FROM pass_in_trip PaTr LEFT JOIN trip Tr ON Tr.trip_id = PaTr.trip_id GROUP BY Tr.trip_id;",
        "SELECT town_to FROM passenger Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = Tr.trip_id WHERE passenger_name = \'Bob\';",
        "SELECT time_in FROM trip Tr LEFT JOIN pass_in_trip PaTr ON PaTr.trip_Id = Tr.trip_id LEFT JOIN passenger Pa ON PaTr.passenger_id = Pa.passenger_id WHERE passenger_name = \'John\' AND town_to = \'California\';",
        "SELECT COUNT(*) FROM trip WHERE town_from = \'Washington\' AND town_to = \'California\';",
        "SELECT town_to, (time_in - time_out) FROM trip WHERE town_from = \'Washington\';",
        "SELECT passenger_name, MAX(CHAR_LENGTH(passenger_name)) FROM passenger;",
        "SELECT passenger_name FROM passenger Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = Tr.trip_id WHERE town_to = \'California\' AND plane = \'Airbus A320\';"
    ]
    QUERY_RESULTS = [
        str(db_connect.get_db().run(query))
        for query in SQL_QUERIES
    ]
    ANSWER = [
        "Here are the names you asked for: \'John\', \'James\', \'Poul\', \'Christofer\', \'Superman\', \'Donald\', \'Douglas\', \'Dwight\', \'Earl\'",
        "Here are the names you asked for: \'American Airlines\', \'S7 Airlines\', \'Nordwind Airlines\'",
        "Here are planes you asked for: \'Airbus A320\'",
        "Here are names you asked for: \'Superman\'",
        "1 flight was made with the Airbus A319 aircraft.",
        "Here are the companies that use the Airbus A321-100: \'S7 Airlines\'",
        "You can fly to California on: \'Airbus A320\'",
        "These companies organize flights from Gongkong: \'Nordwind Airlines\'",
        "Here are the id and qty pairs you requested: (3, 15), (2, 15), (1, 15)",
        "Bob flew to these cities: \'Paris\'",
        "John will arrive on 2021-02-15 at 00:00",
        "1 flight from Washington to California",
        "You can fly to California, the flight will last 1 day",
        "This is Christopher, his name is 10 characters long",
        "These passengers are flying to California on an Airbus A320: \'John\', \'James\', \'Poul\', \'Christofer\', \'Superman\', \'Donald\', \'Douglas\', \'Dwight\', \'Earl\', \'Edgar\', \'Edmund\', \'Edwin\', \'Elliot\', \'Eric\', \'Ernest\'"
    ]


if __name__ == "__main__":
    db = db_connect.get_db()
    print(db.run("SELECT * FROM passenger LIMIT 3"))
