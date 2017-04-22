MODEL = """#ifndef MODELOS_H_
#define MODELOS_H_

typedef struct {
    int length;
    char *data;
} t_stream;

// Header de stream
typedef struct {
    uint8_t tipoEstructura;
    uint16_t length;
} __attribute__ ((__packed__)) t_header;

// Modelos



#endif"""
PACKC = """#include "paquetes.h"

// Paquetizacion

t_stream * paquetizar(int tipoEstructura, void * estructuraOrigen){
    t_stream * buffer;

    switch(tipoEstructura){
    } //Fin del switch

    return buffer;
}

// Despaquetizacion

void * despaquetizar(uint8_t tipoEstructura, char * dataPaquete, uint16_t length){
    void * buffer;

    switch(tipoEstructura){
    } //Fin del switch

    return buffer;
}

// Headers


char * crearDataConHeader(uint8_t tipoEstructura, int length){
    char * data = malloc(length);

    uint16_t lengthDatos = length - sizeof(t_header);

    t_header header = crearHeader(tipoEstructura, lengthDatos); //creo el header

    int tamanoTotal = 0, tamanoDato = 0;

    memcpy(data, &header.tipoEstructura, tamanoDato = sizeof(uint8_t)); //copio el tipoEstructura del header a data
    tamanoTotal = tamanoDato;
    memcpy(data + tamanoTotal, &header.length, tamanoDato = sizeof(uint16_t)); //copio el length del header a data

    return data;
}

t_header crearHeader(uint8_t tipoEstructura, uint16_t lengthDatos){
    t_header header;
    header.tipoEstructura = tipoEstructura;
    header.length = lengthDatos;
    return header;
}

t_header despaquetizarHeader(char * header){
    t_header estructuraHeader;

    int tamanoTotal = 0, tamanoDato = 0;
    memcpy(&estructuraHeader.tipoEstructura, header + tamanoTotal, tamanoDato = sizeof(uint8_t));
    tamanoTotal = tamanoDato;
    memcpy(&estructuraHeader.length, header + tamanoTotal, tamanoDato = sizeof(uint16_t));

    return estructuraHeader;
}

// Auxiliar

// Auxiliar

// End"""
PACKH = """#ifndef PAQUETES_H_
#define PAQUETES_H_

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include "string.h"
#include "modelos.h"

// Paquetizacion

t_stream * paquetizar(int tipoEstructura, void * estructuraOrigen);

// Despaquetizacion

void * despaquetizar(uint8_t tipoEstructura, char * dataPaquete, uint16_t length);

// Headers

char * crearDataConHeader(uint8_t tipoEstructura, int length);
t_header crearHeader(uint8_t tipoEstructura, uint16_t lengthDatos);

t_header despaquetizarHeader(char * header);

// Auxiliar

#endif"""

SOCKC = """#include "socket.h"

/*
 * Nombre: socket_crearCliente/0
 * Argumentos:
 * 		- NINGUNO
 *
 * Devuelve:
 * 		int (Descriptor al socket creado), en caso de error, devuelve -1.
 *
 *
 * Funcion: Crea el socket para un cliente.
 */
int socket_crearCliente(void){

	int sockfd;

	if((sockfd = socket(AF_INET,SOCK_STREAM,0)) == -1){
		perror("Error al crear socket");//Crear log para este error.
		return -1;
	}

	return sockfd;

}

/*Nombre: socket_conectarCliente/3
 * Argumentos:
 * 		- sockfd (int), (descriptor del socket cliente).
 * 		- serverIp (char*),(IP del server a conectar)
 * 		- serverPort (int), (puerto del server a conectar)
 *
 * Devuelve:
 * 		int (Descriptor al socket que se va a conectar, devuelve -1 si hay error).
 *
 * Funcion: Conectarme a un server con su IP y puerto.
 *
 */
int socket_conectarCliente(int sockfd,char *serverIp, int serverPort){

        struct sockaddr_in socketInfo;

        //INICIALIZACION DE SOCKETINFO
        socketInfo.sin_family = AF_INET;
        socketInfo.sin_port = htons(serverPort); //host to network short
        socketInfo.sin_addr.s_addr = inet_addr(serverIp);
        memset(&(socketInfo.sin_zero),\'\0\',8); // PONGO A 0 EL RESTO DE LA ESTRUCTURA
        // ME CONECTO CON LA DIRECCIÓN DE SOCKETINFO
        //SIEMPRE VERIFICANDO QUE NO DEN -1 LAS FUNCIONES O 0 EN CASO DE RECV() -- SOLO PARA SERVER IGUAL :)

        if(connect(sockfd , (struct sockaddr *)&socketInfo , sizeof(socketInfo)) == -1){
            perror("Falló la conexión"); // Cambiar esto por un log.
            return -1;
        }

		return sockfd;
}

/*Nombre: socket_crearYConectarCliente/2
 * Argumentos:
 * 		- serverIp (char*),(IP del server a conectar)
 * 		- serverPort (int), (puerto del server a conectar)
 *
 * Devuelve:
 * 		int (Descriptor al socket que se va a conectar).
 *
 * Funcion: Crear y conectar un nuevo cliente a un server con su IP y puerto.
 *
 */
int socket_crearYConectarCliente(char *serverIp, int serverPort){
	int sockfd;
	sockfd = socket_crearCliente();
	if (sockfd < 0)
		return -1;

	sockfd = socket_conectarCliente( sockfd,(char*)serverIp, serverPort);

	return sockfd;
}

/*Nombre: socket_crearServidor/2
 * Argumentos:
 * 		- serverIp (char*),(IP del server)
 * 		- serverPort (int), (puerto del server)
 *
 * Devuelve:
 * 		int (Descriptor al socket del server).
 *
 * Funcion: Crear un nuevo servidor.
 *
 */
int socket_crearServidor(char *ip, int port){
	int socketEscucha;
	struct sockaddr_in miSocket;//ESTE ES EL SOCKET CON LA DRECCION IP

	if((socketEscucha = socket(AF_INET,SOCK_STREAM,0)) == -1){
		perror("Error al crear socket");
		return -1;
	}

	miSocket.sin_family = AF_INET;
	miSocket.sin_port = htons(port);
	miSocket.sin_addr.s_addr = inet_addr(ip);
	memset(&(miSocket.sin_zero),'\0',8); //NI LE PRESTEN ATENCION A ESTO

	int yes = 1;
	if (setsockopt(socketEscucha, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
		perror("setsockopt");
		exit(1);
	}

	if(bind(socketEscucha,(struct sockaddr*)&miSocket, sizeof(miSocket)) == -1){
		perror ("Error al bindear el socket escucha");
		return -1;
	}

	if (listen(socketEscucha, MAX_CONNECTION_SERVER) == -1){
		perror("Error en la puesta de escucha");
		return -1;
	}

	return socketEscucha;

}

/*Nombre: socket_crearServidor/2
 * Argumentos:
 * 		- serverIp (char*),(IP del server)
 * 		- serverPort (int), (puerto del server)
 *
 * Devuelve:
 * 		int (Descriptor al socket del server).
 *
 * Funcion: Crear un nuevo servidor.
 *
 */
int socket_crearServidorIpLocal(int port){
	int socketEscucha;
	struct sockaddr_in miSocket;//ESTE ES EL SOCKET CON LA DRECCION IP

	if((socketEscucha = socket(AF_INET,SOCK_STREAM,0)) == -1){
		perror("Error al crear socket");
		return -1;
	}

	miSocket.sin_family = AF_INET;
	miSocket.sin_port = htons(port);
	miSocket.sin_addr.s_addr = INADDR_ANY;
	memset(&(miSocket.sin_zero),'\0',8); //NI LE PRESTEN ATENCION A ESTO

	int yes = 1;
	if (setsockopt(socketEscucha, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
		perror("setsockopt");
		exit(1);
	}

	if(bind(socketEscucha,(struct sockaddr*)&miSocket, sizeof(miSocket)) == -1){
		perror ("Error al bindear el socket escucha");
		return -1;
	}

	if (listen(socketEscucha, MAX_CONNECTION_SERVER) == -1){
		perror("Error en la puesta de escucha");
		return -1;
	}

	return socketEscucha;

}




int socket_crearServidorPuertoRandom(char *ip, int * port){
	int socketEscucha;
	struct sockaddr_in miSocket;//ESTE ES EL SOCKET CON LA DRECCION IP

	if((socketEscucha = socket(AF_INET,SOCK_STREAM,0)) == -1){
		perror("Error al crear socket");
		return -1;
	}

	miSocket.sin_family = AF_INET;
	miSocket.sin_port = htons(0);
	miSocket.sin_addr.s_addr = inet_addr(ip);
	memset(&(miSocket.sin_zero),'\0',8); //NI LE PRESTEN ATENCION A ESTO

	int yes = 1;
	if (setsockopt(socketEscucha, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
		perror("setsockopt");
		exit(1);
	}

	if(bind(socketEscucha,(struct sockaddr*)&miSocket, sizeof(miSocket)) == -1){
		perror ("Error al bindear el socket escucha");
		return -1;
	}

	if (listen(socketEscucha, MAX_CONNECTION_SERVER) == -1){
		perror("Error en la puesta de escucha");
		return -1;
	}

	struct sockaddr_in sin;
	socklen_t len = sizeof(sin);
	if (getsockname(socketEscucha, (struct sockaddr *)&sin, &len) == -1){
		perror("getsockname");
		return -1;
	}

	*port = ntohs(sin.sin_port);

	return socketEscucha;
}

/*Nombre: socket_aceptarCliente/1
 * Argumentos:
 * 		- socketEscucha (int),(descriptor del socket del server para escuchar conexiones)
 *
 * Devuelve:
 * 		int (Descriptor al socket de la nueva conexión).
 *
 * Funcion: Aceptar un cliente que está siendo previamente escuchado.
 *
 */
int socket_aceptarCliente(int socketEscucha){
	int socketNuevaConexion;
	unsigned int size_sockAddrIn;

	struct sockaddr_in suSocket;

	size_sockAddrIn = sizeof(struct sockaddr_in);
	socketNuevaConexion = accept(socketEscucha, (struct sockaddr *)&suSocket, &size_sockAddrIn);

	if(socketNuevaConexion < 0) {

		perror("Error al aceptar conexion entrante");
		return -1;

	}

	return socketNuevaConexion;

}

/*
 * Nombre: socket_enviar/3
 * Argumentos:
 * 		- socketReceptor
 * 		- tipo: (unsigned char) tipo de socket
 * 		- estructura (void *) (lo que quiero enviar)
 * 		- tipoEstructura (int que define qué estructura quiero enviar)
 *
 * Devuelve:
 * 		int (1->si se envio o false->error al envio).
 * 		--> convierte la estructura a un buffer transferible, y lo envia.
 *
 * Funcion: paquetiza y envia la estructura, convierte la estructura a un buffer transferible y la envia
 */
int socket_enviar(int socketReceptor, t_tipoEstructura tipoEstructura, void* estructura){
	int cantBytesEnviados;

	t_stream * paquete = paquetizar(tipoEstructura, estructura);

	cantBytesEnviados = send(socketReceptor, paquete->data, paquete->length, 0);
	free(paquete->data);
	free(paquete);
	if( cantBytesEnviados == -1){
		perror("Server no encontrado");
		return 0;
	}
	else {
		return 1;
	}
}

/*
 * Nombre: socket_recibir/3
 * SINTAXIS CORRECTA: socket_recibir(soquetEmisor, &tipoRecibido, &PunteroAEstructuraRecibida)
 * NOTA: El segudno y tercer parametro son por referencia. Los modifica en la funcion.
 * Admite que se mande NULL en cualquiera de los dos, si no interesa uno de los datos.
 * Argumentos:
 * 		- socketEmisor
 * 		- tipoEstructura: (t_tipoEstructura *) puntero a la variable tipo del paquete
 * 		- estructura (void **) puntero a una variable tipo void*
 *
 * Devuelve:
 * 		int (1-> se recibio ok, 0-> si hubo problemas).
 *
 * Funcion: recibir y despaquetizar, convierte el paquete recibido a la estructura que corresponda.
 */
int socket_recibir(int socketEmisor, t_tipoEstructura * tipoEstructura, void** estructura){
	int cantBytesRecibidos;
	t_header header;
	char* buffer;
	char* bufferHeader;

	bufferHeader = malloc(sizeof(t_header));

	cantBytesRecibidos = recv(socketEmisor, bufferHeader, sizeof(t_header), MSG_WAITALL);	//Recivo por partes, primero el header.
	if(cantBytesRecibidos == -1){
		free(bufferHeader);
		perror("Error al recibir datos");
		return 0;
	}


	header = despaquetizarHeader(bufferHeader);
	free(bufferHeader);

	if (tipoEstructura != NULL) {
		*tipoEstructura = header.tipoEstructura;
	}

	if(header.length == 0){	// Que pasa si recivo mensaje con length 0? retorno 1 y *estructura NULL.
		if (estructura != NULL) {
			*estructura = NULL;
		}
		return 1;
	}

	buffer = malloc(header.length);
	cantBytesRecibidos = recv(socketEmisor, buffer, header.length, MSG_WAITALL);	//Recivo el resto del mensaje con el tamaño justo de buffer.
	if(cantBytesRecibidos == -1){
		free(buffer);
		perror("Error al recibir datos");
		return 0;
	}

	if(estructura != NULL) {
		*estructura = despaquetizar(header.tipoEstructura, buffer, header.length);
	}

	free(buffer);

	if (cantBytesRecibidos == 0){
			*tipoEstructura = 0;
	}

	return 1;
}




char* socket_ip(char* direccionCompleta){
	char * dir = string_duplicate(direccionCompleta);
	string_append(&dir,"basura"); // Le agrego al final cualquier cosa, cuestion de que si me mandan "127.0.0.1:", pueda dividirlo correctamente...
	char * resultado = ( string_split(dir, ":") )[0]; //Divido en el ":", en un array de char* y digo que me de la primera parte.
	free(dir);
	return resultado;
}

int socket_puerto(char* direccionCompleta){
	char * dir = string_duplicate("basura");
	string_append(&dir,direccionCompleta); // Le agrego al principio cualquier cosa, cuestion de que si me mandan ":2532", pueda dividirlo correctamente...
	int resultado = atoi(( string_split(dir, ":") )[1]);	//Divido en el ":", en un array de char* y digo que me de la segunda parte en forma de int.
	free(dir);
	return resultado;
}

char* socket_unirDireccion(char* ip, int puerto){
	return string_from_format("%s:%d", ip, puerto);
}

/*
 * Nombre: socket_cerrarConexion/3
 *
 * Argumentos:
 * 		- socket
 *
 * Devuelve:
 * 		int (-1-> si se cerro ok, 0-> si hubo problemas).
 *
 * Funcion: recibir y despaquetizar, convierte el paquete recibido a la estructura que corresponda.
 */
int socket_cerrarConexion(int socket){
	return close(socket);
}"""

SOCKH = """#ifndef SOCKET_H_
#define SOCKET_H_

#include <stdlib.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/epoll.h>
#include <errno.h>
#include <sys/ioctl.h>
#include "package.h"
#include <commons/string.h>

#define MAX_EVENTS_EPOLL 60
#define MAX_CONNECTION_SERVER 60 //VAMOS A ATENDER DE A 10 CONEXIONES COMO MAXIMO A LA VEZ

// Estructura para paquetizar datos a enviar/recibir
typedef struct {
	uint8_t tipo;
	uint16_t length;
} t_socketHeader;

typedef uint8_t t_tipoEstructura;

//FUNCIONES PARA EL CLIENTE
int socket_crearCliente(void);
int socket_conectarCliente(int sockfd,char *serverIp, int serverPort);
int socket_crearYConectarCliente(char *serverIp, int serverPort);

//FUNCIONES PARA EL SERVIDOR
int socket_crearServidor(char *ip, int port);
int socket_crearServidorPuertoRandom(char *ip, int * port);
int socket_aceptarCliente(int socketEscucha);
int socket_crearServidorIpLocal(int port);

//FUNCIONES COMUNES
int socket_enviar(int socketReceptor, t_tipoEstructura tipoEstructura, void* estructura);
int socket_recibir(int socketEmisor, t_tipoEstructura * tipoEstructura, void** estructura);

int socket_cerrarConexion(int socket);

//FUNCIONES DE MANIPULACION DE DIRECCIONES IP y PUERTO
char* socket_ip(char* direccionCompleta);
int socket_puerto(char* direccionCompleta);

char* socket_unirDireccion(char* ip, int puerto);


#endif /* SOCKET_H_ */"""