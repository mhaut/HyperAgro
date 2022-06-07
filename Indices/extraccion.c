#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mongoc/mongoc.h>



void desempaquetarCubo (char* nombreFichero, int tamanoFichero)
{
    /* 1. Se prepara el buffer para almacenar el contenido del cubo
          espectral leido de MongoDB y se carga
    */
    unsigned short *buffer = (unsigned short *) malloc (tamanoFichero); 
    void *ptr_buffer = (void*) buffer;   
    FILE *fichero = fopen(nombreFichero,"rb");   
    fread(buffer,sizeof(unsigned short), tamanoFichero/sizeof(unsigned short),fichero);
    fclose(fichero);
    printf("\nCubo cargado en memoria:"
           "\n\ttamano buffer    -> %i Bytes"
           "\n\tnumero elementos -> %li"
           "\n\ttamano elemento  -> %li Bytes\n\n",
            tamanoFichero,tamanoFichero/sizeof(unsigned short), sizeof(unsigned short));
    /* 2. Se prepara el buffer de destino para almacenar el contenido del cubo
          espectral desempaquetado   
    */   
    int tamanoFinal = tamanoFichero * 4 / 3.0; 
    unsigned short *bufferDestino =(unsigned short *) malloc(tamanoFinal);
    void *ptr_bufferDestino = (void*) bufferDestino;
    unsigned short valorAnterior;
    /* 3. Se realiza el desempaquetamiento de 12bits a 16bits almacenando el 
          resultado en bufferDestino   
    */ 
    for(int i = 0; i < tamanoFichero / sizeof(*buffer); i++) {
        switch (i%3){
            case 0:
                *bufferDestino = (*buffer & 0x0FFF);
                valorAnterior = *buffer;
                break;
            case 1:
                *bufferDestino = ((valorAnterior & (0xF000)) >> 12) | ((*buffer & (0x00FF)) << 4);
                valorAnterior = *buffer;
                break;
            case 2:
                *bufferDestino = ((valorAnterior & (0xFF00)) >> 8) | ((*buffer & (0x000F)) << 8);
                bufferDestino++;
                *bufferDestino = ((*buffer & 0xFFF0) >> 4);
                break;
        }
        buffer++;
        bufferDestino++;
    }    
    printf("\nCubo desempaquetado:"
           "\n\ttamano buffer    -> %i Bytes"
           "\n\tnumero elementos -> %li"
           "\n\ttamano elemento  -> %li Bytes\n\n",
            tamanoFinal,tamanoFinal/sizeof(unsigned short), sizeof(unsigned short));  
    /* 4. Se guarda en un fichero el cubo desempaquetado*/ 
    fichero = fopen(nombreFichero,"wb");
    fwrite(ptr_bufferDestino,sizeof(unsigned short), tamanoFinal/sizeof(unsigned short), fichero);
    fclose(fichero);       
    /* 5. Se libera la memoria reservada ppor los buffers*/
    free(ptr_buffer);
    free(ptr_bufferDestino);
}

int main (int argc, char *argv[])
{
    /* 0. Se inicializa la libreria de mongoc */
    mongoc_init ();
    char *ficheroDestino = argv[1];
    /* 1. Se crea el cliente contra la instancia de MongoDB*/
    mongoc_client_t *client = mongoc_client_new ("mongodb://localhost:27017");

    /* 2. Se selecciona la bd que se quiere usar de las que hay en la instancia*/
    mongoc_database_t *db = mongoc_client_get_database (client, "test");

    /* 3. Se crea el bucket de GridFS */
    bson_t prefijoBucket;
    bson_init(&prefijoBucket); 
    BSON_APPEND_UTF8(&prefijoBucket, "bucketName", "gridfstest");
    bson_error_t error;
    mongoc_gridfs_bucket_t *bucket = mongoc_gridfs_bucket_new (db, &prefijoBucket, NULL, &error);
    if (!bucket) {
       printf ("Error al crear el gridfs bucket: %s\n", error.message);
       return EXIT_FAILURE;
    }
    printf ("Conexion establecida contra la base de datos\n");


   /* 4. Se accede a los metadatos del fichero mas nuevo */
    bson_t *filtroLista = BCON_NEW ("filename", BCON_REGEX("raw_.*.bin", "i"));
    bson_t preferenciasLectura;
    bson_init(&preferenciasLectura);

    mongoc_cursor_t *cursor = mongoc_gridfs_bucket_find (bucket, filtroLista, &preferenciasLectura);
    const bson_t *documento;


    bson_iter_t iter;
    const bson_oid_t *oid;
    char oidstr[25];
    const bson_value_t *tamanoDocumento;
    while(mongoc_cursor_next (cursor, &documento)) {
        bson_iter_init_find(&iter, documento, "_id");
        oid = bson_iter_oid (&iter);
        bson_oid_to_string (oid, oidstr);
        bson_iter_init_find(&iter, documento, "length");
        tamanoDocumento = bson_iter_value(&iter);
    }
 

    printf ("Datos del documento a procesar\n"
            "\tOID    -> %s\n"
            "\ttamano -> %i\n", oidstr, tamanoDocumento->value.v_int32);

    bson_value_t *idDocumento = malloc(sizeof(bson_value_t));
    idDocumento->value.v_oid = *oid;
    idDocumento->value_type = BSON_TYPE_OID;

    /* 5. Se obtiene el documento con el OID recuperado y se escribe en ficheroDestino*/

    mongoc_stream_t *streamDescarga = mongoc_stream_file_new_for_path (ficheroDestino, O_CREAT | O_RDWR, 0);

    if(!mongoc_gridfs_bucket_download_to_stream(bucket, idDocumento, streamDescarga, &error)) {
        printf("Que ha pachao?");
        return EXIT_FAILURE;
    }
    printf("Se ha podido almacenar correctamente el documento en el fichero \"%s\"\n", ficheroDestino);
    /* 6. Se lee el ficheroDestino y se desempaqueta*/
    
    clock_t tiempo = clock();
    desempaquetarCubo(ficheroDestino, tamanoDocumento->value.v_int32);    
    tiempo = clock() - tiempo;

    printf("Tiempo empleado en el desempaquetamiento -> %f\n",(double)tiempo/CLOCKS_PER_SEC);
    /* 6. Cleanup. */
    mongoc_stream_close(streamDescarga);
    mongoc_stream_destroy (streamDescarga);
    mongoc_cursor_destroy (cursor);
    bson_destroy (&prefijoBucket);
    mongoc_gridfs_bucket_destroy (bucket);
    mongoc_database_destroy (db);
    mongoc_client_destroy (client);
    mongoc_cleanup ();

   return EXIT_SUCCESS; 
}
