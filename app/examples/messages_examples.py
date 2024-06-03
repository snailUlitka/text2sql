"""Stores an array with messages that show the agent how to use the tools."""
from app.tools import (
    SQLQueryTool,
    DatabaseTableInfoTool,
    DatabaseTableListTool,
    SQLCheckerTool
)

from langchain.chat_models.base import BaseChatModel

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langchain_community.utilities.sql_database import SQLDatabase


def get_messages_example(
    db: SQLDatabase,
    llm: BaseChatModel
):
    list_tool = DatabaseTableListTool(db)
    info_tool = DatabaseTableInfoTool(db)
    checker_tool = SQLCheckerTool(llm, db)
    query_tool = SQLQueryTool(db)

    return [
        HumanMessage(
            content="Print the names of the passengers who flew to " +
                "California by Airbus A320 aircraft",
            example=True
        ),
        AIMessage(
            content="{'tool': '__list_sql_database_tool', 'tool_input': { }}",
            example=True
        ),
        list_tool.wrap_result_with_human_message(
            list_tool._execute_tool(),
            example=True
        ),
        AIMessage(
            content="{'tool': '__info_sql_database_tool', 'tool_input': " +
                "{'list_of_tables': 'pass_in_trip, passenger, trip'} }",
            example=True
        ),
        info_tool.wrap_result_with_human_message(
            info_tool._execute_tool(["pass_in_trip", "passenger", "trip"]),
            example=True
        ),
        AIMessage(
            content="{'tool': '__query_sql_checker_tool', 'tool_input': " +
                "{'query_to_check': 'SELECT passenger_name FROM passenger " +
                "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
                "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
                "Tr.trip_id WHERE town_to = 'California' AND plane = " +
                "'Airbus A320';'} }",
            example=True
        ),
        checker_tool.wrap_result_with_human_message(
            "SELECT passenger_name FROM passenger " +
            "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
            "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
            "Tr.trip_id WHERE town_to = 'California' AND plane = " +
            "'Airbus A320';",
            example=True
        ),
        AIMessage(
            content="{'tool': '__query_sql_checker_tool', 'tool_input': " +
                "{'query_to_check': 'SELECT passenger_name FROM passenger " +
                "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
                "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
                "Tr.trip_id WHERE town_to = 'California' AND plane = " +
                "'Airbus A320';'} }",
            example=True
        ),
        checker_tool.wrap_result_with_human_message(
            "SELECT passenger_name FROM passenger " +
            "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
            "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
            "Tr.trip_id WHERE town_to = 'California' AND plane = " +
            "'Airbus A320';",
            example=True
        ),
        AIMessage(
            content="{'tool': '__query_sql_database_tool', 'tool_input': " +
                "{'sql_query': 'SELECT passenger_name FROM passenger Pa " +
                "LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
                "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
                "Tr.trip_id WHERE town_to = 'California' AND plane = " +
                "'Airbus A320';'} }",
            example=True
        ),
        query_tool.wrap_result_with_human_message(
            query_tool._execute_tool(
                "SELECT passenger_name FROM passenger " +
                "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
                "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
                "Tr.trip_id WHERE town_to = 'California' AND plane = " +
                "'Airbus A320';"
            ),
            example=True
        ),
        AIMessage(
            content="{'tool': '__conversational_response', 'tool_input': " +
                "{'response': 'These passengers are flying to California on " +
                "an Airbus A320: 'John', 'James', 'Poul', 'Christofer', " +
                "'Superman', 'Donald', 'Douglas', 'Dwight', 'Earl', 'Edgar'," +
                " 'Edmund', 'Edwin', 'Elliot', 'Eric', 'Ernest'.'} }",
            example=True
        )
    ]
