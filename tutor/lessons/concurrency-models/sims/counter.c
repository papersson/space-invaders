// Two threads each add 1 to a shared counter ten million times, with no lock (OSTEP ch. 26),
// and then the same with a mutex around the increment.
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define N 10000000
static volatile long counter = 0;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static int use_lock;

static void *worker(void *arg) {
    for (long i = 0; i < N; i++) {
        if (use_lock) pthread_mutex_lock(&m);
        counter = counter + 1;
        if (use_lock) pthread_mutex_unlock(&m);
    }
    return NULL;
}

int main(int argc, char **argv) {
    use_lock = argc > 1 && atoi(argv[1]);
    pthread_t a, b;
    pthread_create(&a, NULL, worker, NULL);
    pthread_create(&b, NULL, worker, NULL);
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    printf("%ld\n", counter);
    return 0;
}
