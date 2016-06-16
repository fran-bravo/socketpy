import sqlite3, os, re, sys
from socketpy.filing import FileLineWrapper
from socketpy.db import Database


class Configure:

    def __init__(self):
        self.working_directory = os.getcwd()
        self.headers = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headers")
        self.database = Database()

    # Public Interface #

    def initialize_directories(self):
        self._create_directory("database")
        self._create_directory("headers")

    def create_db(self):
        self.database.create_types_table()
        self._load_basic_types()

    def close_connection(self):
        self.database.close_connection()

    def create_headers(self):
        self._create_models()
        self._create_packagesh()
        self._create_packagesc()
        return

    def gather_types(self):
        directories = list(os.walk(self.working_directory))
        for direc in directories:
            root, subdirs, files = direc
            for fd in files:
                if fd.endswith(".c") or fd.endswith(".h"):
                    self._analyze_file(root, fd)
                    print("\tNo hay más tipos de dato en el archivo\n")

    # Private Methods #

    def _analyze_file(self, root, source):
        print("Raiz ", root)
        file = os.path.join(root, source)
        print("Procesando archivo: ", source)
        struct_body = False
        fd = FileLineWrapper(open(file))
        for line in fd.f:
            if line.startswith("#include"):
                self._inspect_include(line)
            if line.startswith("typedef") and line.endswith("{"):
                struct_body = not struct_body
            if line.startswith("typedef") and line.endswith(";\n"):
                linea = line.split(" ")
                linea.remove("typedef")
                tipo = linea[-1]
                tipo = re.sub('[;\n]', '', tipo)
                print(tipo)
                self.database.insert_type(tipo, source)
            if line.startswith("}"):
                struct_body = not struct_body
                tipo = re.sub('[;}\ \n]', '', line)
                if tipo.startswith("__"):
                    tipo = tipo.split("))")[1]
                if tipo != "":
                    self.database.insert_type(tipo, source)

    def _inspect_include(self, line):
        print("Inspecting include ", line)
        if "<" in line:
            file = line.split("<")[-1]
            file = re.sub('[>\n]', '', file)
        if "\"" in line:
            file = line.split("\"")[-2]
        for root in self.database.get_routes():
            for dir, subdirs, files in os.walk(root):
                if file in files:
                    self._analyze_file(dir, file)
                    print("\tNo hay más tipos de dato en el archivo\n")
                    break

    def _load_basic_types(self):
        types = [("int", "builtin"), ("uint8_t", "builtin"),
                 ("uint16_t", "builtin"), ("uint32_t", "builtin"),
                 ("void", "builtin"), ("char", "builtin"),
                 ("int*", "builtin"), ("uint8_t*", "builtin"),
                 ("uint16_t*", "builtin"), ("uint32_t*", "builtin"),
                 ("void*", "builtin"), ("char*", "builtin"),
                 ]
        self.database.insert_types(types)

    @staticmethod
    def _create_directory(directory):
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), directory))

    #   Templates Creation  #

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
