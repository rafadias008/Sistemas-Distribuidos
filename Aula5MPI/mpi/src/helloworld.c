#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char** argv) {
    int rank, size; // rank = ranking da maquina | size = quantos processos existem
    int *array_local, *array;
    int soma_local, soma;
    int tamanho = 8; // tamanho total do array
    int tamanho_local; // pedaço que cada processo vai pegar

    MPI_Init(&argc, &argv); // liga o MPI
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // pega meu ID
    MPI_Comm_size(MPI_COMM_WORLD, &size); // pega total de processos

    tamanho_local = tamanho / size; // divide o trabalho
    array_local = (int*)malloc(tamanho_local * sizeof(int)); // espaço pra receber os dados

    if (rank == 0) { // só o processo 0 cria o array completo
        array = (int*)malloc(tamanho * sizeof(int));
        printf("Array: ");
        for (int i = 0; i < tamanho; i++) {
            array[i] = i + 1; // preenche de 1 até 8
            printf("%d ", array[i]);
        }
        printf("\n");
    }

    // distribui o array entre os processos
    MPI_Scatter(array, tamanho_local, MPI_INT,
                array_local, tamanho_local, MPI_INT,
                0, MPI_COMM_WORLD);

    soma_local = 0;
    printf("Array recebido pelo rank %2d: ", rank);

    // cada processo soma sua parte
    for (int i = 0; i < tamanho_local; i++) {
        printf("%3d ", array_local[i]);
        soma_local += array_local[i];
    }
    printf("-- soma local: %4d\n", soma_local);

    // junta todas as somas no processo 0
    MPI_Reduce(&soma_local, &soma, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        sleep(1); // print da saída
        printf("Soma do array: %d\n", soma);
        printf("Valor esperado: %d\n", tamanho * (tamanho + 1) / 2);
        free(array);
    }

    free(array_local); // libera memória
    MPI_Finalize(); // encerra MPI
}