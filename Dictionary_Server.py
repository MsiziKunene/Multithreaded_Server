import socket
import threading
import json
import os

# JSON file to store the dictionary
json_file = 'dictionary.json'

# Load the dictionary from the JSON file if it exists
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        dictionary = json.load(f)
else:
    dictionary = {'ibhaxa':'Umuntu ofana no Lungelo kungaba ukubukeka noma ukwenza kwakhe.'}

dictionary_lock = threading.Lock()  # Lock to ensure thread-safe access

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            request = conn.recv(1024).decode().strip()
            if not request:
                break
            
            parts = request.split(" ")
        
            if len(parts) < 2:
                response = "Error: Invalid command format. Use ADD, LOOKUP, or UPDATE.\n"
            else:
                command = parts[0].upper()
                key = parts[1]
                
                if command == "ADD" and len(parts) != 0:
                    value = parts[2:]
                    with dictionary_lock:
                        if key not in dictionary:
                            dictionary[key] = ' '.join([str(x) for x in value])
                            response = f"Added {key} : {dictionary[key]}\n"
                            # Write the updated dictionary to the JSON file
                            with open(json_file, 'w') as f:
                                json.dump(dictionary, f, indent=4)
                        else:
                            response = f"Error: Key {key} already exists.\n"
                
                elif command == "LOOKUP" and len(parts) == 2:
                    with dictionary_lock:
                        value = dictionary.get(key, "Word not found.")
                        response = f"{key} : {value}\n"
                
                elif command == "UPDATE" and len(parts) != 0:
                    new_value = parts[2:]
                    with dictionary_lock:
                        if key in dictionary:
                            dictionary[key] = ' '.join([str(x) for x in new_value])
                            response = f"Updated {key} -> {dictionary[key]}\n"
                            # Write the updated dictionary to the JSON file
                            with open(json_file, 'w') as f:
                                json.dump(dictionary, f, indent=4)
                        else:
                            response = f"Error: Key {key} not found.\n"
                
                else:
                    response = "Error: Invalid command or incorrect number of arguments.\n"
            
            conn.sendall(response.encode())
    
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    
    finally:
        conn.close()

def start_server():
    SERVER_ADDRESS = '0.0.0.0' 
    SERVER_PORT = 65433

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen()
    print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
        
        except Exception as e:
            print(f"Error accepting connection: {e}")

if _name_ == "_main_":
    start_server()