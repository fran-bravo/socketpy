#ifndef SOCKET_H_
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
#include "paquetes.h"

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

//FUNCIONES DE STRINGS

char**  string_split(char * text, char * separator);
char** _string_split(char* text, char* separator, int(*condition)(char*, int));
void 	string_append(char ** original, char * string_to_add);
char*   string_from_format(const char* format, ...);
char*	string_duplicate(char* original);

#endif /* SOCKET_H_ */