import sys, socket, argparse, time, bitstring
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument("-ip", "--ip", help="ip")

def agw_connect(s):
    s.send(b'\x00\x00\x00\x00k\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    return

def start_socket(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        time.sleep(5)
        sys.exit()
    host = str(ip)
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        time.sleep(5)
        sys.exit()
    s.connect((remote_ip , port))
    print(f'Connected to {remote_ip}:{port}')
    print("")
    return s

def main(s, name):
    while True:
        frame = s.recv(8192).hex()
        frame = frame[74:]
        reply = [frame[i:i+2] for i in range(0, len(frame), 2)]
        frame = ' '.join(reply)
        img_sync = frame[:59]
        if(int(str(frame.find(' ff d8 ff e0 '))) >= int(0)):
            name=str(time.strftime("%m-%d_%H-%M-%S"))
            x=int(str(frame[78:].find(' ff d8 ff e0')))
            with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(str(frame[78+x:]).replace(' ', ''))).tofile(out_file)
            with open('data.ts', 'w') as o:
                o.write('out_image_'+str(name)+'.jpg')
        elif(str(img_sync) == str('82 6c 64 aa 9e a6 e0 82 6c 60 aa 9e a6 61 03 f0 45 53 45 52')):    
            chb1=frame[73:75]
            chb2=frame[70:72]
            chb3=frame[66:68]
            check_value=bitstring.BitStream(hex=str(str(chb1)+str(chb2)+str(chb3))).read('uint')
            print(f"Frame: {(int(check_value))}     ", end='\r')
            with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(str(frame[78:]).replace(' ', ''))).tofile(out_file)
        if(int(str(frame[78:].find(' ff d9 '))) >= int(0)):
            with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(str(frame[78:]).replace(' ', ''))).tofile(out_file)

if(__name__=='__main__'):
    ip=parser.parse_args().ip
    port=parser.parse_args().port
    name=f'Delete_this_file_{time.strftime("%m-%d_%H-%M")}'
    s=start_socket(ip=ip, port=int(port))
    agw_connect(s=s)
    main(s=s, name=name)