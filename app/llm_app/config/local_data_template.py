"""
To generate `local_data.py` which is used to gain access to the database. 
Creates a file at execute `local_data.py` in the same directory.
"""
PASSWORD_FOR_LLM = "<PASSWORD_FOR_LLM>"
PASSWORD_OF_VC_STORE = "<PASSWORD_OF_VC_STORE>"

DB_HOST = "<DB_HOST>"
DB_PORT = 5432
DB_NAME = "<DB_NAME>"
DB_USER = "<DB_USER>"

VC_HOST = "<VC_HOST>"
VC_PORT = 5432
VC_NAME = "<VC_NAME>"
VC_USER = "<VC_USER>"


def create_local_data_file(
    path: str,
    *,
    password_for_external_db=PASSWORD_FOR_LLM,
    passwrod_for_vector_db=PASSWORD_OF_VC_STORE,
    external_db_host=DB_HOST,
    external_db_port=DB_PORT,
    external_db_name=DB_NAME,
    external_db_user=DB_USER,
    vector_db_host=VC_HOST,
    vector_db_port=VC_PORT,
    vector_db_name=VC_NAME,
    vector_db_user=VC_USER
):
    with open(path, "w") as file:
        file.write(
            f"PASSWORD_FOR_LLM = \"{password_for_external_db}\"\n" +
            f"PASSWORD_OF_VC_STORE = \"{passwrod_for_vector_db}\"\n\n" +
            f"DB_HOST = \"{external_db_host}\"\n" +
            f"DB_PORT = {external_db_port}\n" +
            f"DB_NAME = \"{external_db_name}\"\n" +
            f"DB_USER = \"{external_db_user}\"\n\n" +
            f"VC_HOST = \"{vector_db_host}\"\n" +
            f"VC_PORT = {vector_db_port}\n" +
            f"VC_NAME = \"{vector_db_name}\"\n" +
            f"VC_USER = \"{vector_db_user}\"\n"
        )


if __name__ == "__main__":
    create_local_data_file(
        ".\\app\\databases\\local_data.py",
        password_for_external_db=PASSWORD_FOR_LLM,
        passwrod_for_vector_db=PASSWORD_OF_VC_STORE,
        external_db_port=DB_PORT,
        external_db_name=DB_NAME,
        external_db_user=DB_USER,
        vector_db_port=VC_PORT,
        vector_db_name=VC_NAME,
        vector_db_user=VC_USER
    )