# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:31:13 2019

@author: Celal
"""

import socket
import pandas as pd
#OTEL
class Hotel:
    headers = {
        'Server': 'Hotel',
        'Content-Type': 'text/html',
    }
    status_codes = {
        200: 'OK',
        404: 'Not Found',
    }
    
    def communicate(self,df,df2):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1242))
        s.listen(5)
        while True:
            clientsocket, address = s.accept()
            print(f'Connection from {address} has been established.')
            request = clientsocket.recv(1024)
            req=str(request)
            clientsocket.sendall(str.encode(self.create_http_response(req,df,df2)))
            print("Gönderildi "+str(self.create_http_response(req,df,df2)))
            clientsocket.close()
        s.close()
        
                
    def parse_http_request(self,http_request):
        lines=http_request.split("\n")
        uri=lines[0].split(" ")[1]
        dummy,date, hotel_name, num_person,update_database=uri.split("/")
        return date, hotel_name,num_person,update_database
    
    def response_line(self, status_code):
        """Returns response line"""
        reason = self.status_codes[status_code]
        return "HTTP/1.1 %s %s\r\n" % (status_code, reason)
    
    def response_headers(self, extra_headers=None):
        """Returns headers
        The `extra_headers` can be a dict for sending 
        extra headers for the current response
        """
        headers_copy = self.headers.copy() # make a local copy of headers
        if extra_headers:
            headers_copy.update(extra_headers)
        headers = ""
        for h in self.headers:
            headers += "%s: %s\r\n" % (h, self.headers[h])
        return headers

    def create_http_response(self, http_request,df,df2):
        """Handles the incoming request.
        Compiles and returns the response
        """
        #tarih/otel/kişi sayısı şeklinde bir uri olacak
        #burada database sorgusuyla tarihte otel yeterli mi bak. yeterli ise response body rezerve edildi olacak ve databasede
        #otel kapasitesini düşür.
        print(http_request)
        date,hotel_name,num_person,availability=self.parse_http_request(http_request)
        print(hotel_name+" "+num_person+" "+date)
        print(str(type(hotel_name))+" "+str(type(num_person))+" "+str(type(date)))
        hotel_name=str(hotel_name)
        num_person=int(num_person)
        availability=int(availability)
        date=str(date)
        print(df)
        if hotel_name=="hotel1":
            if not df.loc[df["date"]==date].empty:#dene
                capacity=df.loc[df["date"]==date]["capasity"]
                cond=capacity>=num_person
                if cond.bool():
                    if availability:
                    #response type html mi?
                        df.loc[df["date"]==date,"capasity"]=df.loc[df["date"]==date].capasity-num_person
                        response_body=" hotel1 reserved"
                    else:
                        response_body="1"
                else:
                    if not df2.loc[df2["date"]==date].empty:#dene
                        capacity2=df2.loc[df2["date"]==date]["capasity"]
                        cond2=capacity2>=num_person
                        if cond2.bool():
                        #öneri buraada
                            response_body="hotel1 is not available but hotel2 is available"
                    else:
                        response_body="Date is not in database of hotel2"
            else:
                response_body="Date is not in database of hotel1"
        elif hotel_name=="hotel2":
            if not df2.loc[df2["date"]==date].empty:#dene
                capacity3=df2.loc[df2["date"]==date]["capasity"]
                cond3=capacity3>=num_person
                if cond3.bool():
                    if availability:
                        df2.loc[df2["date"]==date,"capasity"]=df2.loc[df["date"]==date].capasity-num_person
                        response_body=" hotel reserved"
                    else:
                        response_body="1"
                else:
                    if not df.loc[df["date"]==date].empty:#dene
                        capacity4=df.loc[df["date"]==date]["capasity"]
                        cond4=capacity4>=num_person
                        if cond4.bool():
                        #öneri buraada
                            response_body="hotel2 is not available but hotel1 is available"
                    else:
                        response_body="Date is not in database of hotel1"
            else:
                response_body="Date is not in database"
        response_line = self.response_line(status_code=200)
        response_headers = self.response_headers()
        return "%s%s%s" % (
                response_line, 
                response_headers, 
                response_body
            ) 
if __name__ == '__main__':
    database1=pd.read_excel("C:/Users/Celal/Desktop/network/hotel_database.xlsx")
    database2=pd.read_excel("C:/Users/Celal/Desktop/network/hotel_database2.xlsx")
    hotel=Hotel()
    hotel.communicate(database1,database2)
    