#include "paquetes.h"
// Paquetizacion
t_stream * paquetizar(int tipoEstructura, void * estructuraOrigen){
	t_stream * buffer;
    switch(tipoEstructura){
    
		case D_PERSONA:
			//TODO: definir funcion
			break;
		} //Fin del switch
	return buffer;
}
// Despaquetizacion
void * despaquetizar(uint8_t tipoEstructura, char * dataPaquete, uint16_t length){
    void * buffer;
    switch(tipoEstructura){
    
		case D_PERSONA:
			//TODO: definir funcion
			break;
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
#endif
