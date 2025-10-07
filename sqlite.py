from enum import Enum, auto
from typing import Tuple, Optional
import struct

#constant declarations
PAGE_SIZE = 4096
TABLE_MAX_PAGES = 100

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

class Row:
    """Represents a row in our database table"""
    
    #constant declarations at the row level
    ID_SIZE = 4
    USERNAME_SIZE = 32
    EMAIL_SIZE = 255
    ROW_SIZE = ID_SIZE + USERNAME_SIZE + EMAIL_SIZE
    
    #offset calculations
    ID_OFFSET = 0
    USERNAME_OFFSET = ID_OFFSET + ID_SIZE
    EMAIL_OFFSET = USERNAME_OFFSET + USERNAME_SIZE
     
    def __init__(self, id:int=0, username:str="", email:str=""):
        self.id = id
        self.username = username
        self.email = email

    def __str__(self):
        f"({self.id}, {self.username}, {self.email})"

    def serialize(self)->bytes:
        """Convert row into a compact binary representation"""
        packed_id = struct.pack("I", self.id)
        packed_username = self.username.encode('utf-8')[:USERNAME_SIZE].ljust(USERNAME_SIZE, b'\x00')
        packed_email = self.email.encode('utf-8')[:EMAIL_SIZE].ljust(EMAIL_SIZE, b'\x00')

        return packed_id + packed_username + packed_email

    @staticmethod
    def deserialize(data:bytes)->'Row':
        """Convert binary data back to Row object"""
        id_val = struct.unpack('I', data[ID_OFFSET:ID_OFFSET+ID_SIZE])[0]
        username = data[USERNAME_OFFSET: USERNAME_OFFSET+USERNAME_SIZE].rtsrip(b'\x00').decode('utf-8')
        email = data[EMAIL_OFFSET: EMAIL_OFFSET+EMAIL_SIZE].rstrip(b'\x00').decode('utf-8')

        return Row(id_val, username, email)

class Table:
    """Represents the database table"""
    ROWS_PER_PAGE = PAGE_SIZE//Row.ROW_SIZE
    TABLE_MAX_ROWS = TABLE_mAX_PAGES * ROWS_PER_PAGE

    def __init__(self):
        self.num_rows = 0
        self.pages = [None] * TABLE_MAX_PAGES

    def row_slot(self, row_num:int)->tuple[int, int]:
        """Calculate which page and byte offset a row must be inserted.
            Returns a tuple (page_num, byte_offset)"""
        page_num = row_num//self.ROWS_PER_PAGE

        if self.pages[page_num] is None:
            self.pages[page_num] = bytearray(PAGE_SIZE)

        row_offset = row_num%self.ROWS_PER_PAGE
        byte_offset = row_offset * Row.ROW_SIZE
        
        return pagenum, byte_offset

    def insert_row(self, row:Row):
        """Insert a row into the table"""
        page_num, byte_offset = self.row_slot(self.num_rows)
        serialized = row.serialize()
        self.pages[page_num][byte_offset:byte_offset+Row.ROW_SIZE] = serialized
        self.num_rows +=1

    def select_all(self)->list[Row]:
        rows = []
        for i in range(self.num_rows):
            page_num, byte_offset = self.row_slot(i)
            row_data = bytes(self.pages[page_num][byte_offset: byte_offset+Row.ROW_SIZE])
            rows.append(Row.deserialize(row_data))
        return rows
        
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
        
