############################################################################################################
## The following script makes an HTTP request to a webpage and stores the body of the request into a file. 
## Once the file is created it creates a new file that contains the checksum of that file.
#############################################################################################################

import requests
import hashlib

## the url to be passed to the HTTP request
HttpURL = "https://www.hrblock.com/"

## the file storing the body of the request
file_destination = "content.html"

## the file storing the body of the request
file_checksum = "checksum.txt"

## send request to url and raise error in case it doesnt succeed
def send_request(UrlToSend):
    try: 
        response = requests.get(UrlToSend,timeout=3) 
        response.raise_for_status()  
        return response         
    except requests.exceptions.HTTPError as httpErr: 
        print ("Http Error:",httpErr) 
    except requests.exceptions.ConnectionError as connErr: 
        print ("Error Connecting:",connErr) 
    except requests.exceptions.Timeout as timeOutErr: 
        print ("Timeout Error:",timeOutErr) 
    except requests.exceptions.RequestException as reqErr: 
        print ("Something Else:",reqErr) 
        
## Write response to file
def write_request_to_file(requestResponse,FileToWriteTo):
    if requestResponse.status_code == 200:
        with open(FileToWriteTo, 'w', encoding="utf-8") as f: 
            try:
                f.write(requestResponse.text)  
            except Exception as ex:
                print ('Ooops something went wrong while writing request response to file: ' + str(ex))

## Create MD5              
def MD5_to_file (PathToRequestedFile):
     with open(PathToRequestedFile, 'rb') as f:
         try:
            m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()  
         except Exception as ex:
            print ('Ooops something went wrong while creating MD5: ' + str(ex))
            
## Write MD5 to file
def writeMD5_To_File(MD5Towrite,FileToWriteMD5On):
    with open(FileToWriteMD5On, 'w') as f: 
            try:
                f.write(MD5Towrite)  
            except Exception as ex:
                print ('Ooops something went wrong while writing MD5 to file: ' + str(ex))
 
def main(): 
    write_request_to_file(send_request(HttpURL),file_destination)
    writeMD5_To_File (MD5_to_file(file_destination),file_checksum)
    
if __name__ == "__main__":
    main()