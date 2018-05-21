import logging
from watchdog.observers import Observer

import file_handler

if __name__ == "__main__":
    # configure logging
    logging.basicConfig(level=logging.INFO,
	format='%(asctime)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')
    # setup event handler
    event_handler = file_handler.FileHandler()

    # setup observer for file system changes
    observer = Observer()
    observer.schedule(event_handler, file_handler.src_file_dir) 
  
    # Sleep Forever
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    
