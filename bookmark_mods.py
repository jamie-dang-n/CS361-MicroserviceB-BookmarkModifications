import json
import zmq

"""
Expected Input Format: jsonified dictionary (let "" represent a null (empty) string)
input_dict = {
    "json_array": json_array,
    "json_object": json_object,
    "option": [value is 0, 1, or 2]
}

option = 0: quit the microservice
option = 1: append json object to the end of the list
option = 2: remove given json object from the list if it exists

"""
def main():
    # set up ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Binds REP socket to tcp://localhost:5555
    socket.bind("tcp://localhost:5555")
    message = socket.recv()
    print(f"Received request: {message}")

    socket.send(message)




if __name__ == "__main__":
    main()