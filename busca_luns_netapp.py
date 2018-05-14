import paramiko
import base64
import os
import time

fecha=time.strftime("%y%m%d-%H%M")

string_input = raw_input('Introduce la lista separadas por espacio: ')
lista_hex = string_input.split()
lista_ascii = []

# Se convierte los NNA a ASCII y los agrega a una lista
for i in lista_hex:
	conversor = i.decode("hex").split("`\xa9\x80\x00")
	lista_ascii.append(conversor[1])

# Parametros de conexion a la cabina
cabinas = ['1.2.3.4','1.2.3.4','1.2.3.4','1.2.3.4']
diccionario = {"1.2.3.4":"FAS3270A","1.2.3.4":"FAS3270B","1.2.3.4":"FAS3270A","1.2.3.4":"FAS3270B"}

nbytes = 4096
port = 22
command = 'stats list instances lun'
username = 'your_username'
password = 'your_password'

# ----- Abre el fichero donde nos ira pintando las luns que encuentre
resultado = open("resultado_"+fecha+".txt", "a")
resultado.write("CABINA        - 	LUN    - 				SERIAL\n")
resultado.write("-----------------------------------------------------------------------\n")

# ---- Conecta a la cabina y lazan el comando
for hostname in cabinas:
	client = paramiko.Transport((hostname, port))
	client.connect(username=username, password=password)
	stdout_data = []
	stderr_data = []
	session = client.open_channel(kind='session')
	session.exec_command(command)

	while True:
		if session.recv_ready():
			stdout_data.append(session.recv(nbytes))
		if session.recv_stderr_ready():
			stderr_data.append(session.recv_stderr(nbytes))
		if session.exit_status_ready():
			break

	session.close()
	client.close()

#----- Buscamos el serial en la lista de luns que nos da la cabina.
	temporal = open("temporal.txt", "w")
	temporal.write(''.join(stdout_data))
	temporal.close()
	
#--- Guarda los resultado en el ficheros.
	for lun in open("temporal.txt"):
		for serial in lista_ascii:
			if serial in lun:
				resultado.write(diccionario.get(hostname) + lun)

# cerramos los ficheros
resultado.close()
os.system("notepad resultado_"+fecha+".txt")
			
# Eliminamos el fichero con la lista de las luns
os.system("del temporal.txt")
