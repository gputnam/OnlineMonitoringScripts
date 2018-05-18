import socket
import time
import datetime
import redis

REDIS_HOST = "lariat-daq01.fnal.gov"
REDIS_PORT = 6379

UDP_HOST = "lariat-daq04.fnal.gov"
UDP_PORT = 30001

message_senders = ["DaqDecoder:daq@"]
r = redis.Redis(REDIS_HOST, REDIS_PORT)

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
    return (message, int(parsed["timestamp"]))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_HOST, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    parsed = parse_larsoft_message(data)
    if parsed is not None:
        (message, timestamp) = encode_redis_message(parsed)
        r.zadd("RECENT_WARNINGS", message, timestamp)
    

