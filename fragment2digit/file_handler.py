# logging
import logging
from logging.handlers import RotatingFileHandler

# watchdog library for filesystem monitoring
import watchdog
from watchdog.events import PatternMatchingEventHandler

import run_fhicl

# define constants
src_file_pattern = "sbnd*.root"

# setup logging
logger = logging.getLogger("DigitsFileHandler")

# Class which monitors patterns for file events and processes them
# Inherits from PatternMatchingEventHandler to define how process() works
# Idea stolen from Johnny Ho's DQM code
class FileHandler(PatternMatchingEventHandler):
    #def set_src_file_dir(self, src_file_dir):
    #def set_fhicl_list(self, fhicl_list):
    def __init__(self, fhicl_list, src_file_dir):
        self.fhicl_list = fhicl_list
        self.input_patterns = [src_file_dir + src_file_pattern]
        super(FileHandler, self).__init__(self.input_patterns)

    def log(self, event):
        log_message = '%s file: %s' % (
            event.event_type.capitalize(),
            event.src_path
            )

        if hasattr(event, 'dest_path'):
            log_message += ' => %s' % event.dest_path

        logger.info(log_message)

    def process(self, event):

        # define the path to the file as the path to where the file
        # currently is 
        if hasattr(event, 'dest_path'):
            src_file_path = event.dest_path
        else:
            src_file_path = event.src_path
        sub_process_infos = run_fhicl.process(src_file_path, self.fhicl_list)
  
        for (code, message) in sub_process_infos:
            # log output from fragment -> digit converter
            logger.info("Ran with return code %i.\nMessage:\n%s" % (code, message))


    def on_created(self, event):
        self.log(event)
        self.process(event)

    def on_modified(self, event):
        self.log(event)

    def on_deleted(self, event):
        self.log(event)

    def on_moved(self, event):
        self.log(event)
        self.process(event)

