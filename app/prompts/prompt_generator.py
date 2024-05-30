"""
Module stores `PromptGenerator` which 
generate prompt from pieces like `PREFIX`, `SUFFIX`, etc.
"""

from typing import (
    Optional,
    List,
    Dict
)

from app.databases.vector_db import get_selector
from app.databases.external_db import get_db
from app.prompts.sql_expert_prompt import (
    PREFIX,
    TABLE_DESCRIPTIONS,
    SUFFIX,
)

from langchain.embeddings.base import Embeddings

from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.example_selectors import BaseExampleSelector

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)


class PromptGenerator:
    def __init__(self):
        self.example_selector = None
        self.prompt = None

    def set_example_selector(
        self,
        *,
        examples: Optional[List[Dict[str, str]]],
        k: Optional[int],
        embedding_llm: Optional[Embeddings] = None,
        example_selector: Optional[BaseExampleSelector] = None,
        input_keys: List[str] = ["input"]
    ):
        if not examples:
            raise ValueError(
                "List of 'examples' should contain 1 or more items")

        if embedding_llm is None and example_selector is None:
            raise ValueError(
                "Must provide exactly one of 'embedding_llm' or 'example_selector'. Received neither."
            )
        if embedding_llm and example_selector:
            raise ValueError(
                "Must provide exactly one of 'embedding_llm' or 'example_selector'. Received both."
            )

        if example_selector:
            self.example_selector = example_selector
        else:
            self.example_selector = get_selector(
                embedding_llm=embedding_llm,
                examples=examples,
                k=k,
                input_keys=input_keys
            )

        return self

    def get_prompt(
        self,
        *,
        prefix: str = None,
        suffix: str = None,
        table_names: List[str] = None,
        table_descriptions: Dict[str, str] = None,
        example_prompt: Optional[PromptTemplate] = None,
        input_variables: List[str] = ["dialect", "input", "top_k"]
    ) -> ChatPromptTemplate:
        """Generate prompt with few-shots example selector.

        Args:
            prefix - `"f-string"` or plain `str`
            suffix - `"f-string"` or plain `str`
            table_names - `List[str]`: List of table names.
            table_descriptions - `Dict[str, str]`: For example {"name_of_table": "description"}, all names from the `table_names` list should be listed.
            example_prompt - `PromptTemplate`: Default or if `None` "User input: {input} SQL query: {query}".
            input_variables - `List[str]`: List of variables in `prefix` and `suffix`. Defaults to [`"dialect"`, `"input"`, `"top_k"`, `"table_names"`, `"table_descriptions"`].
        """
        if self.example_selector is None:
            raise ValueError(
                "'example_selector' is not specified. Before calling, use the method: 'set_example_selector'")

        if not (prefix and suffix and table_names and table_descriptions):
            prefix = PREFIX
            suffix = SUFFIX
            table_names = get_db().get_usable_table_names()
            table_descriptions = TABLE_DESCRIPTIONS

        if not all(key in table_descriptions for key in table_names):
            raise ValueError(
                "All names from the `table_names` list should be listed in 'table_descriptions' keys.")

        if example_prompt is None:
            example_prompt = PromptTemplate.from_template(
                "User input: {input}\nSQL query: {query}"
            )

        few_shots_prompt = FewShotPromptTemplate(
            prefix=prefix,
            suffix=suffix,
            example_selector=self.example_selector,
            example_prompt=example_prompt,
            input_variables=input_variables
        )

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(prompt=few_shots_prompt),
            # TODO: refactor this examples messages to another module
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            HumanMessage(
                content="Print the names of the passengers who flew to " +
                    " California by Airbus A320 aircraft", 
                example=True
            ),
            AIMessage(
                content="{\'tool\': \'__list_sql_database_tool\', \'tool_input\': {}}",
                example=True
            ),
            HumanMessage(
                content="I can help you execute the tool. Give me a second... " +
                    "And so, I think I managed to call it, but I can't read " +
                    "what's written there, only a smart AI can understand it." +
                    "\nI checked, the result of the tool\n" +
                    "It looks like a list of table names. " +
                    "Maybe it will help to get an response. I think if you don't " +
                    "have enough information, you can use this: \'__info_sql_database_tool\'" +
                    "\n\nResult of tool: \n" +
                    "\'company, pass_in_trip, passenger, trip\'", 
                example=True
            ),
            AIMessage(
                content="{\'tool\': \'__info_sql_database_tool\', \'tool_input\': " +
                    "{\'list_of_tables\': \'pass_in_trip, passenger, trip\'}}",
                example=True
            ),
            HumanMessage(
                content="I can help you execute the tool. Give me a second... " +
                    "And so, I think I managed to call it, but I can't read " +
                    "what's written there, only a smart AI can understand it." +
                    "\nI checked, the result of the tool\n" +
                    "It looks like the structure of the database " +
                    "tables(s). Maybe this will help you write the right query? " +
                    "Please make sure you remember the names!" +
                    "\n\nResult of tool: \n" +
                    "'\nCREATE TABLE pass_in_trip (\n\tpass_in_trip_id BIGSERIAL " +
                    "NOT NULL, \n\ttrip_id BIGINT, \n\tpassenger_id BIGINT, " +
                    "\n\tplace VARCHAR(60), \n\tCONSTRAINT pass_in_trip_pkey " +
                    "PRIMARY KEY (pass_in_trip_id), \n\tCONSTRAINT fk_passanger " +
                    "FOREIGN KEY(passenger_id) REFERENCES passenger (passenger_id), " +
                    "\n\tCONSTRAINT fk_trip FOREIGN KEY(trip_id) REFERENCES trip " +
                    "(trip_id)\n)\n\n/*\n3 rows from pass_in_trip " +
                    "table:\npass_in_trip_id\ttrip_id\tpassenger_id\tplace" +
                    "\n1\t1\t1\tA1\n2\t1\t2\tA2\n3\t1\t3\tA3\n*/\n\n\nCREATE " +
                    "TABLE passenger (\n\tpassenger_id BIGSERIAL NOT NULL, " +
                    "\n\tpassenger_name VARCHAR(60), \n\tCONSTRAINT passenger_pkey " +
                    "PRIMARY KEY (passenger_id)\n)\n\n/*\n3 rows from passenger " +
                    "table:\npassenger_id\tpassenger_name\n1\tJohn\n2\tJames\n3" +
                    "\tPoul\n*/\n\n\nCREATE TABLE trip (\n\ttrip_id BIGSERIAL NOT " +
                    "NULL, \n\tcompany_id BIGINT, \n\tplane VARCHAR(60), \n\ttown_from " +
                    "VARCHAR(60), \n\ttown_to VARCHAR(60), \n\ttime_out TIMESTAMP " +
                    "WITHOUT TIME ZONE, \n\ttime_in TIMESTAMP WITHOUT TIME ZONE, " +
                    "\n\tCONSTRAINT trip_pkey PRIMARY KEY (trip_id), \n\tCONSTRAINT " +
                    "fk_company FOREIGN KEY(company_id) REFERENCES company " +
                    "(company_id)\n)\n\n/*\n3 rows from trip table:\ntrip_id" +
                    "\tcompany_id\tplane\ttown_from\ttown_to\ttime_out\ttime_in" +
                    "\n1\t1\tAirbus A320\tWashington\tCalifornia\t2021-02-14 " +
                    "00:00:00\t2021-02-15 00:00:00\n2\t2\tAirbus A321-100\tTokio" +
                    "\tParis\t2022-05-04 00:00:00\t2022-05-05 00:00:00\n3\t3\tAirbus " +
                    "A319\tGongkong\tRiga\t2023-12-30 00:00:00\t2023-12-31 00:00:00\n*/'", 
                example=True
            ),
            AIMessage(
                content="{\'tool\': \'__query_sql_checker_tool\', \'tool_input\': " +
                "{\'query_to_check\': \'SELECT passenger_name FROM passenger " +
                "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
                "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
                "Tr.trip_id WHERE town_to = \'California\' AND plane = " +
                "\'Airbus A320\';\'} }",
                example=True
            ),
            HumanMessage(
                content="I can help you execute the tool. Give me a second... " +
                    "And so, I think I managed to call it, but I can't read " +
                    "what's written there, only a smart AI can understand it." +
                    "\nI checked, the result of the tool\n" +
                    "It looks like an SQL query! I think it's the " +
                    "right one. Try to execute this query." +
                    "\n\nResult of tool: \n" +
                    "SELECT passenger_name FROM passenger Pa LEFT " +
                    "JOIN pass_in_trip PaTr ON Pa.passenger_id = PaTr.passenger_id " +
                    "LEFT JOIN trip Tr ON PaTr.trip_id = Tr.trip_id WHERE town_to " +
                    "= \'California\' AND plane = \'Airbus A320\';", 
                example=True
            ),
            AIMessage(
                content="{\'tool\': \'__query_sql_checker_tool\', \'tool_input\': " +
                "{\'query_to_check\': \'SELECT passenger_name FROM passenger " +
                "Pa LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = " +
                "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id = " +
                "Tr.trip_id WHERE town_to = \'California\' AND plane = " +
                "\'Airbus A320\';\'} }",
                example=True
            ),
            HumanMessage(
                content="I can help you execute the tool. Give me a second... " +
                    "And so, I think I managed to call it, but I can't read " +
                    "what's written there, only a smart AI can understand it." +
                    "\nI checked, the result of the tool\n" +
                    "It looks like an SQL query! I think it's the " +
                    "right one. Try to execute this query." +
                    "\n\nResult of tool: \n" +
                    "SELECT passenger_name FROM passenger Pa LEFT JOIN " +
                    "pass_in_trip PaTr ON Pa.passenger_id = " +
                    "PaTr.passenger_id LEFT JOIN trip Tr ON PaTr.trip_id " +
                    "= Tr.trip_id WHERE town_to = \'California\' AND " +
                    "plane = \'Airbus A320\';", 
                example=True
            ),
            AIMessage(
                content="{\'tool\': \'__query_sql_database_tool\', \'tool_input\': " +
                "{\'sql_query\': \'SELECT passenger_name FROM passenger Pa " +
                "LEFT JOIN pass_in_trip PaTr ON Pa.passenger_id = PaTr.passenger_id " +
                "LEFT JOIN trip Tr ON PaTr.trip_id = Tr.trip_id WHERE town_to = " +
                "\'California\' AND plane = \'Airbus A320\';\'} }",
                example=True
            ),
            HumanMessage(
                content="I can help you execute the tool. Give me a second... " +
                    "And so, I think I managed to call it, but I can't read " +
                    "what's written there, only a smart AI can understand it." +
                    "\nI checked, the result of the tool\n" +
                    "This is similar to the database " +
                    "response. Maybe there's something I need there. " +
                    "I can't see it, please help me understand, if " +
                    "there is an response to my question, please give it " +
                    "to me, use it for this: \'__conversational_response\'" +
                    "\n\nResult of tool: \n" +
                    "[('John',), ('James',), ('Poul',), ('Christofer',), " +
                    "('Superman',), ('Donald',), ('Douglas',), ('Dwight',), " +
                    "('Earl',), ('Edgar',), ('Edmund',), ('Edwin',), ('Elliot',), " +
                    "('Eric',), ('Ernest',)]", 
                example=True
            ),
            AIMessage(
                content="{\'tool\': \'__conversational_response\', \'tool_input\': " +
                "{\'response\': \'These passengers are flying to California on " +
                "an Airbus A320: 'John', 'James', 'Poul', 'Christofer', " +
                "'Superman', 'Donald', 'Douglas', 'Dwight', 'Earl', 'Edgar', " +
                "'Edmund', 'Edwin', 'Elliot', 'Eric', 'Ernest'.\'} }",
                example=True
            ),
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ("human", "Well, thanks! Help me with another question now. {input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        table_descriptions = "\n\n".join([
            f"{name}: {description}" for (name, description)
            in table_descriptions.items() if name in table_names
        ])
        table_names = ", ".join(table_names)

        self.prompt = self.prompt.partial(
            table_names=table_names,
            table_descriptions=table_descriptions,
            agent_scratchpad=[]
        )

        return self.prompt
