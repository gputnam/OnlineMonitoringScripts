import socket
import time
import datetime
import redis
import json
import argparse
import logging

message_senders = ["DaqDecoder:daq@", "OnlineAnalysis:OnlineAnalysis@"]

def parse_larsoft_message(message):
    data = message.split("|")
    sender = data[10]
    if not sender in message_senders:
        return

    message_level = data[5]
    message_type = data[6]
    run_info = data[9]
    (run, subrun, event) = tuple([int(x) for i,x in enumerate(run_info.split(" ")) if i % 2 == 1])
    message_content = data[-1]

    ret = {
        "level": message_level,
        "type": message_type,
        "run": run,
        "subrun": subrun,
        "event": event,
        "content": message_content,
        "timestamp": time.time()
    }
    return ret

def encode_redis_message(parsed):
    message_param = {
        "level": parsed["level"],
        "type": parsed["type"],
        "run": parsed["run"],
        "subrun": parsed["subrun"],
        "event": parsed["event"],
        "time": datetime.datetime.fromtimestamp(parsed["timestamp"]).strftime("%Y-%m-%d %H:%M"),
        "content": parsed["content"]
    }
    message = "%(level)s at %(time)s Run %(run)i Subrun %(subrun)i Event %(event)i:\n%(type)s:\n%(content)s" % message_param
    return message

def main(args):
    r = redis.Redis(args.redis["host"], args.redis["port"])

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.bind((args.udp["host"], args.udp["port"]))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        try:
            parsed = parse_larsoft_message(data)
        except:
            logging.warning("Unable to parse message:\n%s\n" % data)
            continue
        if parsed is not None:
            r.zadd("WARNINGS", json.dumps(parsed), parsed["timestamp"])
            if args.verbose:
                logging.info("Sent message to Redis:\n%s" % encode_redis_message(parsed))

def host_and_port(arg):
    data = arg.split(":")
    ret = {
        "host": data[0],
        "port": int(data[1])
    }
    return ret


if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--redis", type=host_and_port, default="localhost:6379")
    parser.add_argument("-u", "--udp", type=host_and_port, default="localhost:30001")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-l", "--log_file", default=None)

    args = parser.parse_args()
    # setup logging
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
        
    main(args)

    

