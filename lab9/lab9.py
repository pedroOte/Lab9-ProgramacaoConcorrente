import concurrent.futures
import multiprocessing
import time
import math

N = 1000000 #tamanho sequencia

def ehPrimo(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.ceil(math.sqrt(n) + 1), 2):
        if n % i == 0:
            return False
    return True

#tarefa executada pelo pool de threads
def task(inicio, fim):
    qtdPrimosProcesso = 0
    for i in range(inicio, fim):
        qtdPrimosProcesso += ehPrimo(i)
    return qtdPrimosProcesso

if __name__ == '__main__':
    start = time.time()

    qtdPrimos = 0

    nThreads = multiprocessing.cpu_count()

    futures = [] #array com os resultados das tasks

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(0, N, N // nThreads):
            if (i + N // nThreads < N):
                futures.append(executor.submit(task, i, i + N // nThreads))
            else: 
                futures.append(executor.submit(task, i, N))

        for future in concurrent.futures.as_completed(futures):
            qtdPrimos += future.result()

    end = time.time()

    print('work took {} seconds'.format(end - start))
    print('quantidade de números primos:', qtdPrimos)