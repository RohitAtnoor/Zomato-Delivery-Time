import sys
from source.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    # exc_info() this function gives 3 output and we are storing as __, __, exc_tb
    file_name = exc_tb.tb_frame.f_code.co_filename
    # with the help of exc_tb we will get the file name where the error has occured.

    # below is th format of the error message to get displayed.
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message

# creating the custom exception child class which inherit the parent class Exception.
class CustomException(Exception):
    
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message    
    
'''
Example to check the looging file creation.
if __name__=="__main__":
    logging.info("Logging has started")
    try:
        a=1/0
    except Exception as e:
        logging.info('Dicision by zero') 
        raise CustomException(e,sys)

'''