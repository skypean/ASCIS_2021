import socket
from PIL import Image, ImageDraw, ImageFont
import cv2
import zxing
from pyzbar.pyzbar import decode

def recvuntil(clientSocket, string):
    output = b'' 
    while True:
        output += clientSocket.recv(8092).rstrip()       
        if string in output:
            return output

def qrdecode1():
    print('[+] Decoding using cv2')
    file_path = 'result.png'
    image = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is not None:
        return data
    else:
        return None

def qrdecode2():
    print('[+] Decoding using pyzbar')
    file_path = 'result.png'
    decocdeQR = decode(Image.open(file_path)) 
    return decocdeQR[0].data.decode('ascii')


def qrdecode3():
    print('[+] Decoding using zxing')
    file_path = 'result.png'
    reader = zxing.BarCodeReader()
    barcode = reader.decode(file_path)
    return barcode.raw


def text2png(text):
	from PIL import Image, ImageDraw, ImageFont
 
	# create image
	img = Image.new('RGB', (700, 700), color=(255, 255, 255))

	# Draw function and assigned to d
	d = ImageDraw.Draw(img)

	# Font selection from the downloaded file
	myFont = ImageFont.truetype('FreeMono.ttf', 20)

	# Decide the text location, color and font
	d.text((10, 10), text, fill = (0, 0, 0), font=myFont)

	#save the image
	img.save("result.png")


def solve():
    host, port = '125.235.240.166', 20123
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.connect((host, port))

    for _ in range(100):
        output = recvuntil(clientSock, b'ID Number:')
        print(output.decode())

        qrbytes = output[output.index(b'Person') + len(b'Person #1:\n'):output.index(b'ID Number:')]
        text2png(qrbytes.decode())
        
        text = qrdecode1()
        if text is None or len(text) == 0:
            text = qrdecode2()
        if text is None or len(text) == 0:
            text = qrdecode3()
        print(text)
        id, name, expired = text.split('|')

        clientSock.sendall(id.encode() + b'\n')
        output = recvuntil(clientSock, b'Full Name:')
        clientSock.sendall(name.encode() + b'\n')
        output = recvuntil(clientSock, b'Expired Date:')
        clientSock.sendall(expired.encode() + b'\n')
    output = clientSock.recv(8092).rstrip()  
    print(output[output.index(b'ASCIS'):].decode())
	

if __name__=="__main__":
    solve()