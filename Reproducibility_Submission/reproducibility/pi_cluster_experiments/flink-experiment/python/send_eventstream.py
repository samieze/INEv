from datetime import datetime
import json
import pathlib
import socket
import time
import uuid
import sys



def get_eventstream(ID):
    # read json
    with open("config.json", "r") as f:
        config = json.load(f)[ID]
   
    input_file = config["input_file"]
    print("read:", input_file)
    own_ip = config["connection"][int(ID)]
    print("own IP", own_ip)
    # read event stream input txt
    with open(str(pathlib.Path(__file__).parent.resolve()) + "/" + input_file) as f:
        event_stream = f.readlines()

    return event_stream, config, own_ip
    
def read_and_send_event_stream(event_stream, queryID, own_ip):
    event_counter = 0
    #make ip list for specific sensor or use general ip list

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 5005))

    if queryID == 1:
        event_type_universe = ["E", "F", "G", "H"]
    elif queryID == 2:
        event_type_universe = ["C", "D", "E", "I"]
    elif queryID == 3:
        event_type_universe = ["A", "D", "I", "F"]
    elif queryID == 4:
        event_type_universe = ["E", "F", "C", "H", "A", "B", "I"]


    repeated_time_counters = dict()
    
    for event in event_stream:
        attributes = event.split(",")
        timestamp = attributes[0]
        event_type = attributes[1]
        
        if event_type not in event_type_universe:
            continue

        if timestamp not in repeated_time_counters:
            repeated_time_counters[timestamp] = 0
        else:
            repeated_time_counters[timestamp] += 1
            
        timestamp = timestamp + ":" + str(repeated_time_counters[timestamp])

        
        bike_id = attributes[2]
        target_node_id = attributes[3]
        event_id = str(uuid.uuid4())[0:8]
        creation_timestamp = datetime.now()

        source_node_ip = str(own_ip)

        event_counter += 1
        if event_counter % 100 == 0:
            event_counter = 0
            time.sleep(1)
        
        sender(event_type, timestamp, event_id, creation_timestamp, bike_id, target_node_id, source_node_ip, client_socket)
            
    #signal the end of the stream by sending a "end-of-the-stream" message
    send_end_of_the_stream_message(client_socket)

#send data with this function
def sender(eventtype, timestamp, event_id, creation_timestamp, bike_id, target_node_id, source_node_ip, client_socket):
    message = "%s | %s | %s | %s | %s | %s | %s \n" % (eventtype, timestamp, event_id, creation_timestamp, bike_id, target_node_id, source_node_ip)
    message = message.replace('\r', '').replace('\n', '')
    message += " \n"
    print(message)
    error = ""
    try:
        client_socket.send(message.encode(encoding="UTF-8"))
        print("Message sent!")
    except error:
        print("Error - message not sent!",error)


def send_end_of_the_stream_message(client_socket):
    error = ""
    try:
        client_socket.send("end-of-the-stream\n".encode(encoding="UTF-8"))
        print("end-of-the-stream!!")
    except error:
        print("Error - message not sent!",error)
        
def main():
    queryID = 1
    ownID = "0"
    if len(sys.argv) > 1:
        queryID = int(sys.argv[1])
    if len(sys.argv) > 2:
        ownID = sys.argv[2]
    event_stream, config, own_ip = get_eventstream(ownID)
    read_and_send_event_stream(event_stream, queryID, own_ip)
    

if __name__ == "__main__":
    main()
