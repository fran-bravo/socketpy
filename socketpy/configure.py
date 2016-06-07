import sqlite3, os
from socketpy.excpetions import FileError
from socketpy.filing import Filer, FileLineWrapper


class Configure:

    def __init__(self):
        self.working_directory = os.getcwd()
        self._create_directory("database")
        self._create_directory("headers")
        self.database = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database"), "types.db")
        self.headers = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headers")
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.create_db()
        self.create_headers()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS types (type_id INTEGER PRIMARY KEY,
                                                                 type_name VARCHAR(50),
                                                                 type_built_in BIT)""")
        self._load_basic_types()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def create_headers(self):
        self._create_models()
        self._create_packagesh()
        self._create_packagesc()
        return

    def _load_basic_types(self):
        types = [("int", 1), ("uint8_t", 1),
                 ("uint16_t", 1), ("uint32_t", 1),
                 ("void", 1), ("char", 1),
                 ("int*", 1), ("uint8_t*", 1),
                 ("uint16_t*", 1), ("uint32_t*", 1),
                 ("void*", 1), ("char*", 1),
                 ]
        self.cursor.executemany("INSERT INTO types VALUES(NULL, ?,?)", types)

    @staticmethod
    def _create_directory(directory):
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), directory))

    def _create_models(self):
        fd = FileLineWrapper(open(os.path.join(self.headers, "modelos.h"), "w+"))
        fd.f.writelines("""#ifndef MODELOS_H_
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



#endif"""
                        )
        fd.close()
        return

    def _create_packagesh(self):
        fd = FileLineWrapper(open(os.path.join(self.headers, "paquetes.h"), "w+"))
        fd.f.writelines("""#ifndef PAQUETES_H_
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


#endif"""
                        )
        fd.close()
        return

    def _create_packagesc(self):
        fd = FileLineWrapper(open(os.path.join(self.headers,  "paquetes.c"), "w+"))
        fd.f.writelines("""#include "paquetes.h"

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


#endif"""
                        )
        fd.close()
        return
