#ifndef PAQUETES_H_
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


#endif

