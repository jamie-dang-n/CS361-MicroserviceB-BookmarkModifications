import json
import zmq

"""
LISTENS ON PORT 5553
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
# convertInt is used to convert fields
# from the input dictionary (hasValidData and option)
# to an integer. if conversion fails, the int = -1
def convertInt(dict, field):
    returnInt = 0
    try:
        if (dict[field]):
            returnInt = int(dict[field])
    except ValueError:
        returnInt = -1
    return returnInt

def main():
    # set up ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Binds REP socket to tcp://localhost:5553
    socket.bind("tcp://localhost:5553")
    proceed = 1 # continue waiting for next request while option != 0
    while (proceed != 0):
        print("Bookmark Modifications Service Listening...")
        request = socket.recv()
        print(f"Received request: {request}")

        # convert byte string message to json
        decoded = json.loads(request.decode('utf-8'))
        print(f"Decoded request: {decoded}")

        # check if option is 0-- if it is, quit the service
        proceed = convertInt(decoded, "option")
        if (proceed != 0):
            option = decoded['option']
            # do the appropriate operation
            if (option == 1):
                # append the json object to the end of the json array
                returnArray = decoded['json_array']
                returnArray.append(decoded['json_object'])
            elif(option == 2):
                # remove the specific json object from the array if it exists
                returnArray = decoded['json_array']
                target = decoded['json_object']
                for item in returnArray:
                    if item.get("index") == target.get("index"):
                        returnArray.remove(item)
                        break
            
            # convert returnArray to byte string
            jsonReturnString = json.dumps(returnArray)
            returnByteString = jsonReturnString.encode('utf-8')
            print(f"Response: {returnByteString}")
            socket.send(returnByteString)
        else:
            print("Bookmark Modifications Microservice has ended.")
            socket.send_string("") # send back empty string

if __name__ == "__main__":
    main()