import socket  
from time import sleep  

# create and configure socket on local host  
serverSocket = socket.socket()  
host = socket.gethostname()  
port = 25000 #arbitrary port  
serverSocket.bind((host, port))
serverSocket.listen() # (1)

while True:
    con, addr = serverSocket.accept()    
    print("connected to: " + str(addr))

    # receive from client  
    message = con.recv(1024).decode("UTF-8")
    result = message.split()
    test = result[0]
    value = float(result[1])
    print(message)

    # attempt to send and receive wave, otherwise reconnect  
    try:
        # RBC
        if test == 'RBC':
            if value >= 4.0 and value <= 5.2:
                print("RBC >= 4.0 and RBC <= 5.2")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 4.0:
                print("RBC < 4.0")
                con.send(bytes("Low RBC value!", "UTF-8"))
                con.close()
            if value > 5.2:
                print("RBC > 5.2")
                con.send(bytes("High RBC value!", "UTF-8"))
                con.close()
        # WBC
        if test == 'WBC':
            if value >= 4.0 and value <= 11.0:
                print("WBC >= 4.0 and WBC <= 11.0")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 4.0:
                print("WBC < 4.0")
                con.send(bytes("Low WBC value!", "UTF-8"))
                con.close()
            if value > 11.0:
                print("WBC > 11.0")
                con.send(bytes("High WBC value!", "UTF-8"))
                con.close()
        # Hgb
        if test == 'Hgb':
            if value >= 12.0 and value <= 16.0:
                print("Hgb >= 12.0 and Hgb <= 16.0")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 12.0:
                print("Hgb < 12.0")
                con.send(bytes("Low Hgb value!", "UTF-8"))
                con.close()
            if value > 16.0:
                print("Hgb > 16.0")
                con.send(bytes("High Hgb value!", "UTF-8"))
                con.close()
        # Hematocrit
        if test == 'Hematocrit':
            if value >= 38.8 and value <= 50.0:
                print("Hematocrit >= 38.8 and Hematocrit <= 50.0")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 38.8:
                print("Hematocrit < 38.8")
                con.send(bytes("Low Hematocrit value!", "UTF-8"))
                con.close()
            if value > 50.0:
                print("Hematocrit > 50.0")
                con.send(bytes("High Hematocrit value!", "UTF-8"))
                con.close()
        # Platelets
        if test == 'Platelets':
            if value >= 150.0 and value <= 450.0:
                print("Platelets >= 150.0 and Platelets <= 450.0")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 150.0:
                print("Platelets < 150.0")
                con.send(bytes("Low Platelets value!", "UTF-8"))
                con.close()
            if value > 450.0:
                print("Platelets > 450.0")
                con.send(bytes("High Platelets value!", "UTF-8"))
                con.close()
    except:
        print("An error occurred!")
        sleep( 1 ) # wait 1 second