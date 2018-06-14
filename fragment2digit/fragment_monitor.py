import logging
import time
import sys
from watchdog.observers import Observer
import sys
import argparse

import file_handler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log_file", default=None)
    parser.add_argument("-i", "--input_dir", default="/tmp/")
    parser.add_argument("-f", "--fhicl_configuration", action="append")
    args = parser.parse_args()
    
    # configure logging
    if args.log_file is None:
        # use stdout by default
        logging.basicConfig(
	    stream=sys.stdout,
	    level=logging.INFO,
	    format='%(asctime)s - %(message)s',
	    datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(
            filename=args.log_file,
	    level=logging.INFO,
	    format='%(asctime)s - %(message)s',
	    datefmt='%Y-%m-%d %H:%M:%S')

    # setup event handler
    event_handler = file_handler.FileHandler(args.fhicl_configuration, args.input_dir)

    # setup observer for file system changes
    observer = Observer()
    observer.schedule(event_handler, args.input_dir)
    observer.start()
  
    # Sleep Forever
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    
