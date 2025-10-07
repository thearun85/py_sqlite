from enum import Enum, auto
from typing import Tuple, Optional


class MetaCommandResult(Enum):
    """Statuses for meta command execution"""
    SUCCESS = auto()
    UNRECOGNIZED_COMMAND = auto()

class PrepareResult(Enum):
    """Statuses to be returned while parsing the command input by the users."""
    SUCCESS = auto()
    UNRECOGNIZED_STATEMENT = auto()

class StatementType(Enum):
    """Various statement types supported by the db engine."""
    INSERT = auto()
    SELECT = auto()

class Statement:
    def __init__(self, statement_type:StatementType)->None:
        self.type = statement_type


def print_prompt():
    """The main prompt to accept user inputs"""
    print("db >", end="", flush=True)

def do_meta_command(command:str)->MetaCommandResult:
    """This function handles the meta commands which starts with a ."""
    if command == '.exit':
        print("Goodbye!")
        exit(0)
    return MetaCommandResult.UNRECOGNIZED_COMMAND

def prepare_statement(input_string:str)->Tuple[PrepareResult, Optional[Statement]]:

        if input_string.startswith("insert"):
            return PrepareResult.SUCCESS, Statement(StatementType.INSERT)
        elif input_string.startswith("select"):
            return PrepareResult.SUCCESS, Statement(StatementType.SELECT)

        return PrepareResult.UNRECOGNIZED_STATEMENT, None

def execute_statement(statement: Statement)->None:
    if statement.type == StatementType.INSERT:
        print("Insert is handled here")
    elif statement.type == StatementType.SELECT:
        print("Select is handled here")
    

def main():
    print_prompt()
    while True:
        try:
            user_input = input().strip()
        except(EOFError):
            print("\nerror reading input")

        if user_input.startswith('.'):
            result = do_meta_command(user_input)
            if result == MetaCommandResult.UNRECOGNIZED_COMMAND:
                print(f"unrecognized command '{user_input}.'")
            continue

        result, statement = prepare_statement(user_input)
        if result == PrepareResult.UNRECOGNIZED_STATEMENT:
            print(f"unrecognized statement '{user_input}'.")
            continue

        execute_statement(statement)

if __name__ == '__main__':
    main()
        
