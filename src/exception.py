import sys

def error_message_detail(error_message:str, error_details:sys) -> str:
    _, _, exc_tb = error_details.exc_info()
    file_name, line_num = exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno
    error_msg = f'\n\n\nError occured in python script name [{file_name}] line number [{line_num}] error message [{error_message}]\n'
    return error_msg

class CustomException(Exception):
    def __init__(self, error_message:str, error_details:sys) -> None:
        super().__init__(error_message)
        self.error_message:str = error_message_detail(error_message, error_details)
        
    def __str__(self) -> str:
        return self.error_message