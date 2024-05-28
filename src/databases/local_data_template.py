"""
To generate `local_data.py` which is used to gain access to the database. 
Creates a file at execute `local_data.py` in the same directory.
"""
PASSWORD_FOR_LLM = ""
PASSWORD_OF_VC_STORE = ""

DB_PORT = 5432
DB_NAME = ""
DB_USER = ""

VC_PORT = 5432
VC_NAME = ""
VC_USER = ""

if __name__ == "__main__":
    with open(".\\src\\local_data321.py", "w") as file:
        file.write(
            f"PASSWORD_FOR_LLM= \"{PASSWORD_FOR_LLM}\"\n" +\
            f"PASSWORD_OF_VC_STORE = \"{PASSWORD_OF_VC_STORE}\"\n\n" +\
            f"DB_PORT = {DB_PORT}\n" +\
            f"DB_NAME = \"{DB_NAME}\"\n" +\
            f"DB_USER = \"{DB_USER}\"\n\n" +\
            f"VC_PORT = {VC_PORT}\n" +\
            f"VC_NAME = \"{VC_NAME}\"\n" +\
            f"VC_USER = \"{VC_USER}\"\n"
        )