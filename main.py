from flask import Flask,render_template,flash,request,redirect,url_for,make_response
import base64
from Crypto.Cipher import AES


def encrypt(str, key, iv):
	cipher = AES.new(key, AES.MODE_CBC,iv)
	x = 16 - (len(str) % 16)
	if x != 0:
		str = str + chr(x)*x
		msg = base64.b64encode(cipher.encrypt(str))
		return msg

def encryptData(decryptedData, iv, sessionKey):
	aesIV = base64.b64decode(iv)
	aesKey = base64.b64decode(sessionKey)
	return encrypt(decryptedData, aesKey, aesIV)

def decrypt(enStr, key, iv):
	cipher = AES.new(key, AES.MODE_CBC, iv)
	msg = cipher.decrypt(enStr)
	paddingLen = ord(msg[len(msg)-1])
	return msg[0:-paddingLen]

def decryptData(encryptedData, iv, sessionKey):
	aesIV = base64.b64decode(iv)
	aesCipher = base64.b64decode(encryptedData)
	aesKey = base64.b64decode(sessionKey)
	return decrypt(aesCipher, aesKey, aesIV)


app = Flask(__name__,template_folder="templates")
app.secret_key = 'mycz'

@app.route('/',methods=['GET','POST'])
def index():
	if request.method == 'POST':
		#print(request.form.get('iv'))
		#print(request.form.get('key'))
		if request.form.get('iv') != None and request.form.get('key') != None:
			if request.form.get('esubmit'):
				#print request.form.get('datatext')
				#print encryptData(str(request.form.get('datatext')),request.form.get('key'),request.form.get('iv'))
				return encryptData(str(request.form.get('datatext')),request.form.get('key'),request.form.get('iv'))
			if request.form.get('dsubmit'):
				if request.form.get('dsubmit'):
					return decryptData(str(request.form.get('datatext')),request.form.get('key'),request.form.get('iv'))
	else:
		return render_template("index.html")

if __name__ == '__main__':
   app.run("0.0.0.0",port=54321,threaded=True)
