#ifndef MODELOS_H_
#define MODELOS_H_

#include  <commons/collections/list.h>

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



#endif

