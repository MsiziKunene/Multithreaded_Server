import socket

def send_request(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('10.10.57.147', 65433))
    client.send(command.encode('utf-8'))
    
    response = client.recv(4096).decode('utf-8')
    print(response)
    client.close()

while True:
    word = input('LOOKUP/ADD/UPDATE: ')
    send_request(word)
    if word == 'exit':
            print("Thank you for using our service")
            break