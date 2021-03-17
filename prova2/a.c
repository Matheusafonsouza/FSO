#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

#define MAX_VALUE 100000

sem_t mutex;
int v1[MAX_VALUE], v2[MAX_VALUE];
int sem1, sem2, mod, value, count;

void calc1(int i)
{
  if ((v1[i] % mod) == value)
  {
    sem_wait(&mutex);
    count++;
    sem_post(&mutex);
  }
}

void calc2(int i)
{
  if ((v2[i] % mod) == value)
  {
    sem_wait(&mutex);
    count++;
    sem_post(&mutex);
  }
}

void *calcula_perguntasv1(void *a)
{
  for (int i = 0; i < MAX_VALUE; i++)
    v1[i] = rand_r(&sem1);
}

void *calcula_perguntasv2(void *a)
{
  for (int i = 0; i < MAX_VALUE; i++)
    v2[i] = rand_r(&sem2);
}

void *verifica1(void *a)
{
  for (int i = 0; i < MAX_VALUE; i++)
  {
    calc1(i);
  }
}

void *verifica2(void *a)
{
  for (int i = 0; i < MAX_VALUE; i++)
  {
    calc2(i);
  }
}

int read()
{
  if (scanf(" %d %d", &mod, &value) != 2)
  {
    return -1;
  }
  return 1;
}

int main()
{
  pthread_t tid1, tid2;

  sem_init(&mutex, 0, 1);

  scanf("%d %d", &sem1, &sem2);

  //create threads
  pthread_create(&tid1, NULL, &calcula_perguntasv1, NULL);
  pthread_create(&tid2, NULL, &calcula_perguntasv2, NULL);
  //wait for threads
  pthread_join(tid1, NULL);
  pthread_join(tid2, NULL);

  while (read() != -1)
  {
    //create threads
    pthread_create(&tid1, NULL, &verifica1, NULL);
    pthread_create(&tid2, NULL, &verifica2, NULL);
    //wait for threads
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);

    printf("%d\n", count);
    count = 0;
  }

  return 0;
}