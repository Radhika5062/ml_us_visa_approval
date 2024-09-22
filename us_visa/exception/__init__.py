import os 
import sys

def error_message_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in python script {file_name} line number {exc_tb.tb_lineno} error message {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail):
        super().__init__(error)
        self.error = error_message_detail(error, error_detail=error_detail)
    
    def __str__(self):
        return self.error