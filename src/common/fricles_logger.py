import glob
import logging
import logging.handlers
import sys
import traceback
from src.common.fricles_properties import *

logfile = fricles_basic_properties['fricles_logfile_name']

fricles_logger = logging.getLogger('root')
fricles_logger.setLevel(fricles_basic_properties['fricles_logger_level'])
FORMAT = "%(levelname)s:%(asctime)s:[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
handler = logging.handlers.RotatingFileHandler(
              logfile, maxBytes = fricles_basic_properties['fricles_logsize'], backupCount = 0)

formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)

fricles_logger.addHandler(handler)
fricles_logger.disabled = fricles_basic_properties['fricles_logger_disabled']

def assert_error():
    _,_,tb = sys.exc_info()
    traceback.print_tb(tb)
    tb_info = traceback.extract_tb(tb)
    filename,line,func,text = tb_info[-1]
    print ('error occurred ' + str(filename) + ':' + str(func) + ':' + str(line) + ':' + text)




