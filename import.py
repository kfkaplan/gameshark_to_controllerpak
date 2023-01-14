#Test generate a Nintendo 64 .mpk file with gameshark codes

#Import python libraries
import struct
import yaml
import io
import sys

#Grab command line arguments
gsfile_filename = sys.argv[1].lower()
mpkinfile_filename = sys.argv[2].lower()
mpkoutfile_filename = sys.argv[3].lower()

#Check file extensions are correct
mpkinfile_extension = mpkinfile_filename.split('.')[-1]
mpkoutfile_extension = mpkoutfile_filename.split('.')[-1]
gsfile_extension = gsfile_filename.split('.')[-1]
if mpkinfile_extension != 'mpk':
  raise Exception('Extension for file '+mpkinfile_filename+' needs to end in .mpk')
if mpkoutfile_extension != 'mpk':
  raise Exception('Extension for file '+mpkoutfile_extension+' needs to end in .mpk')
if gsfile_extension != 'yml' and gsfile_extension != 'yaml' and gsfile_extension != 'cht' and gsfile_extension != 'txt':
  raise Exception('Extension for file '+gsfile_filename+' must be either have the extension .yml, .yaml, .cht, or .txt which are the formats exported by gamehacking.org.')


#Import .mpk file
with open(mpkinfile_filename, mode='rb') as file:
  mpk = bytearray(file.read()) #Here we make it a byte array for easier manipulation

# #Functions convert a string to ASCII (source https://www.delftstack.com/howto/python/convert-string-to-ascii-python/#use-a-user-defined-function-to_ascii-to-get-ascii-of-a-string-in-python)
# def to_ascii(text):  
#     ascii_values = [ord(character) for character in text]
#     return ascii_values







#Open gameshark codes file
game_name = gsfile_filename.rsplit('.', 1)[0][:15] #Grab game name from gsfile_filename with the extension stripped (note the 30 char limit of the GS)
build_byte_array = bytearray(game_name.encode()) #Initialize byte array with game name
build_byte_array += b'\x00' #Add a blank byte

if gsfile_extension == 'yml' or gsfile_extension == 'yaml': #Process .yml database files
  with open(gsfile_filename, 'r') as stream: #Read file
    yaml_data = yaml.safe_load(stream)
  build_byte_array += len(yaml_data).to_bytes(1, byteorder='big') #Add number of codes for this game
  # build_byte_array.append(b"\x00\x00\x00\x00"
  for code in yaml_data: #Loop through each code
    build_byte_array +=  bytearray(code[:15].encode()) #Add name of code note the 30 char limit of the GS)
    print(code[:15]) #Print name of code
    lines = yaml_data[code] #Grab all lines for this code
    build_byte_array += b'\x00' #Add a blank byte
    build_byte_array += len(lines).to_bytes(1, byteorder='big') #Add number of lines for this code
    for line in lines: #Loop through all lines for this code
      build_byte_array += bytearray.fromhex(line.replace(' ', '')) #Add hex for gameshark code line
elif gsfile_extension == 'txt': #Process .txt files outputted by gamehacking.org (each line is a line of gs code and code names are on the first line for each code)
  with open("Mario Kart 64 (USA).txt", mode='r') as file:
    data = file.read().split('\n')
  n_codes = 0 #Count number of codes
  for codeline in data:
    if len(codeline) > 13:
      n_codes += 1
  build_byte_array += n_codes.to_bytes(1, byteorder='big') #Add number of codes for this game
  for i in range(n_codes):
    if len(data[i]) > 13: #If this is the first line in a code
      build_byte_array +=  bytearray(data[i][14:][:15].encode()) #Add name of code (note the 30 char limit of the GS)
      print(data[i][14:][:15]) #Print name of code
      build_byte_array += b'\x00' #Add a blank byte
      j = 1 #Count number of lines in the code
      if i+j < len(data):
        print('len(data[i+j])', len(data[i+j]))
        while len(data[i+j]) == 13: #If no name is on this line, add another line to the code
          j += 1
          if i+j >= len(data): #Error catch to keep from going beyond end of code list
            break
      print('i', i)
      print('j', j)
      print('len(data)', len(data))
      build_byte_array += j.to_bytes(1, byteorder='big') #Add number of lines in the code
      for k in range(i, i+j):
        build_byte_array += bytearray.fromhex(data[k][0:14].replace(' ', '')) #Add hex for gameshark code line
# elif gsfile_extension == 'cht':
#   #do stuff

n_build_byte_array = len(build_byte_array) #Cound number of bytes to in build_byte_array
mpk[0x504:0x508] = n_build_byte_array.to_bytes(4, byteorder='big') #Save the length of the gameshark codes in bytes to the .mpk file
mpk[0x508:0x508+n_build_byte_array] = build_byte_array #Splice the gameshark codes into the .mpk file



#Save mpk file
with open(mpkoutfile_filename, mode='wb') as file:
  file.write(mpk) #Here we make it a byte array for easier manipulation