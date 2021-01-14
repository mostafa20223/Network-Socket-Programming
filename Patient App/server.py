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
    test = message.split()[0]
    value = float(message.split()[1])
    print(message)

    # attempt to send and receive wave, otherwise reconnect  
    try:
        # RBC
        if test == 'RBC':
            if value >= 4.0 and value <= 5.2:
                print("RBC >= 4.0 and RBC <= 5.2 and server replies with (You are in the normal range!)")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 4.0:
                print("RBC < 4.0 and server will check the value")
                if value <= 0.0:
                    print("RBC value is zero or below and is not correct! So, server replies with (RBC value is not correct! please re-enter it)")
                    con.send(bytes("RBC value is not correct! please re-enter it", "UTF-8"))
                    con.close()
                else:
                    print("RBC value is neither zero nor below but still below 4.0. So, server replies with (Low RBC value!)")
                    con.send(bytes("Low RBC value!", "UTF-8"))
                    con.close()
            if value > 5.2:
                print("RBC > 5.2 and server replies with (High RBC value!)")
                con.send(bytes("High RBC value!", "UTF-8"))
                con.close()
        # WBC
        if test == 'WBC':
            if value >= 4.0 and value <= 11.0:
                print("WBC >= 4.0 and WBC <= 11.0 and server replies with (You are in the normal range!)")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 4.0:
                print("WBC < 4.0 and server will check the value")
                if value <= 0.0:
                    print("WBC value is zero or below and is not correct! So, server replies with (WBC value is not correct! please re-enter it)")
                    con.send(bytes("WBC value is not correct! please re-enter it", "UTF-8"))
                    con.close()
                else:
                    print("WBC value is neither zero nor below but still below 4.0. So, server replies with (Low WBC value!)")
                    con.send(bytes("Low WBC value!", "UTF-8"))
                    con.close()
            if value > 11.0:
                print("WBC > 11.0 and server replies with (High WBC value!)")
                con.send(bytes("High WBC value!", "UTF-8"))
                con.close()
        # Hgb
        if test == 'Hgb':
            if value >= 12.0 and value <= 16.0:
                print("Hgb >= 12.0 and Hgb <= 16.0 and server replies with (You are in the normal range!)")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 12.0:
                print("Hgb < 12.0 and server will check the value")
                if value <= 0.0:
                    print("Hgb value is zero or below and is not correct! So, server replies with (Hgb value is not correct! please re-enter it)")
                    con.send(bytes("Hgb value is not correct! please re-enter it", "UTF-8"))
                    con.close()
                else:
                    print("Hgb value is neither zero nor below but still below 12.0. So, server replies with (Low Hgb value!)")
                    con.send(bytes("Low Hgb value!", "UTF-8"))
                    con.close()
            if value > 16.0:
                print("Hgb > 16.0 and server replies with (High Hgb value!)")
                con.send(bytes("High Hgb value!", "UTF-8"))
                con.close()
        # Hematocrit
        if test == 'Hematocrit':
            if value >= 38.8 and value <= 50.0:
                print("Hematocrit >= 38.8 and Hematocrit <= 50.0 and server replies with (You are in the normal range!)")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 38.8:
                print("Hematocrit < 38.8 and server will check the value")
                if value <= 0.0:
                    print("Hematocrit value is zero or below and is not correct! So, server replies with (Hematocrit value is not correct! please re-enter it)")
                    con.send(bytes("Hematocrit value is not correct! please re-enter it", "UTF-8"))
                    con.close()
                else:
                    print("Hematocrit value is neither zero nor below but still below 12.0. So, server replies with (Low Hematocrit value!)")
                    con.send(bytes("Low Hematocrit value!", "UTF-8"))
                    con.close()
            if value > 50.0:
                print("Hematocrit > 50.0 and server replies with (High Hematocrit value!)")
                con.send(bytes("High Hematocrit value!", "UTF-8"))
                con.close()
        # Platelets
        if test == 'Platelets':
            if value >= 150.0 and value <= 450.0:
                print("Platelets >= 150.0 and Platelets <= 450.0 and server replies with (You are in the normal range!)")
                con.send(bytes("You are in the normal range!", "UTF-8"))
                con.close()
            if value < 150.0:
                print("Platelets < 150.0 and server will check the value")
                if value <= 0.0:
                    print("Platelets value is zero or below and is not correct! So, server replies with (Platelets value is not correct! please re-enter it)")
                    con.send(bytes("Platelets value is not correct! please re-enter it", "UTF-8"))
                    con.close()
                else:
                    print("Platelets value is neither zero nor below but still below 12.0. So, server replies with (Low Platelets value!)")
                    con.send(bytes("Low Platelets value!", "UTF-8"))
                    con.close()
            if value > 450.0:
                print("Platelets > 450.0 and server replies with (High Platelets value!)")
                con.send(bytes("High Platelets value!", "UTF-8"))
                con.close()
    except:
        print("An error occurred!")
        sleep( 1 ) # wait 1 second