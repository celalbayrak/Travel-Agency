# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 13:22:54 2019

@author: Celal
"""
#AGEnt
import socket

class Agenta:
    def __init__(self):
        self.hotel_uri=None
        self.airline_uri=None
    
    #clientla tcp alma ve http request formatına dönüştürme
    def communicate_tcp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1241))
        s.listen(5)
        clientsocket, address = s.accept()
        
        while True:
            # now our endpoint knows about the OTHER endpoint.
            availability_hotel=0
            availability_airline=0
            print(f'Connection from {address} has been established.')
            #dateler iki tane oldu
            msg = "Welcome to the server! Please enter the number of travelers,hotel name, arrival date, departure date, airplane name: "
            clientsocket.send(bytes(msg,"utf-8"))
        
            entry = clientsocket.recv(1024)
            entry_str=str(entry.decode("utf-8"))
            print((str(entry.decode("utf-8"))))
            entrys=entry_str.split(" ")
            
            
            hotel_input = entrys[2]+"/"+entrys[1]+"/"+entrys[0]+"/"
            airline_input=entrys[2]+"/"+entrys[3]+"/"+entrys[0]+"/"
            self.hotel_uri=hotel_input+str(availability_hotel)
            self.airline_uri=airline_input+str(availability_airline)
            hotel_response=self.communicate_hotel()
            print("first hotel response"+str(hotel_response))
            airline_response=self.communicate_airline()
            print("first airline response"+str(airline_response))
            availability_hotel=self.parse_http_response(hotel_response)
            print("first hotel availability"+str(availability_hotel))
            
            availability_airline=self.parse_http_response(airline_response)
            print("first airline availability"+availability_airline)
            if str(availability_hotel)=="1" and str(availability_airline)=="1":
                second_hotel_response=self.communicate_hotel()
                print("second hotel response"+str(second_hotel_response))
                second_airline_response=self.communicate_airline()
                print("second airline response"+str(second_airline_response))
                tcp_response="hotel response= "+ str(self.parse_http_response(second_hotel_response))+" airline response: "+ str(self.parse_http_response(second_airline_response))
            elif str(availability_hotel)=="1" and not str(availability_airline)=="1":
                 tcp_response="hotel response: "+str(hotel_response)+ " airline response: airline available"+str(airline_response)
                
            elif not str(availability_hotel)=="1" and str(availability_airline)=="1":
                tcp_response="hotel response: "+str(hotel_response)+ " airline response: airline available"+str(airline_response)
                
            else:
                 tcp_response="hotel response: "+str(hotel_response)+ " airline response: airline available"+str(airline_response)
                
            clientsocket.send(bytes(tcp_response,"utf-8"))
        
    def create_http_req_hotel(self,method):
        first_line=method+" "+"/"+self.hotel_uri+ " "+ "HTTP/1.1"
        second_line="Host: localhost"
        third_line="Connection: keep-alive"
        fourth_line="User-Agent: Chrome"
        request="""{str1}
{str2}
{str3}
{str4}""".format(str1=first_line,str2=second_line,str3=third_line,str4=fourth_line)
        return request
    
    def create_http_req_airline(self,method):
        first_line=method+" "+"/"+self.airline_uri+ " "+ "HTTP/1.1"
        second_line="Host: localhost"
        third_line="Connection: keep-alive"
        fourth_line="User-Agent: Chrome"
        request="""{str1}
{str2}
{str3}
{str4}""".format(str1=first_line,str2=second_line,str3=third_line,str4=fourth_line)
        return request
    
    def parse_http_response(self,http_response):
        http_response=http_response.decode("utf-8")
        lines=http_response.split("\n")
        body=lines[3]
        return body
        
    #otelle
    def communicate_hotel(self):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((socket.gethostname(), 1242))
        s2.send(str.encode(self.create_http_req_hotel("POST")))
        response=s2.recv(1024)
        s2.close()
        print(response)
        return response
    
    #airline ile
    def communicate_airline(self):
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3.connect((socket.gethostname(), 1243))
        s3.send(str.encode(self.create_http_req_airline("POST")))
        response=s3.recv(1024)
        s3.close()
        print(response)
        return response
        
    
        
if __name__ == '__main__':
    ag=Agenta()
    ag.communicate_tcp()
    #ag.communicate_http()
    #http_req_to_hotel=ag.create_http_req()
    #ag.http_send(http_req_to_hotel)