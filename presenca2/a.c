#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

int N;

int cmpfunc(const void *a, const void *b)
{
  return (*(int *)a - *(int *)b);
}

void *order(void *a)
{
  qsort(a, N, sizeof(int), cmpfunc);
}

int equals(int *v1, int *v2)
{
  for (int i = 0; i < N; i++)
  {
    if (v1[i] != v2[i])
    {
      return -1;
    }
  }

  return 1;
}

int main(void)
{
  pthread_t tid;
  scanf(" %d", &N);

  int v1[N], v2[N];

  for (int i = 0; i < N; i++)
  {
    scanf(" %d", &v1[i]);
  }
  for (int i = 0; i < N; i++)
  {
    scanf(" %d", &v2[i]);
  }

  pthread_create(&tid, NULL, &order, (void *)&v1);
  qsort(v2, N, sizeof(int), cmpfunc);

  pthread_join(tid, NULL);

  if (equals(v1, v2) != -1)
  {
    puts("Mesmos elementos");
  }
  else
  {
    puts("Diferentes");
  }
  return 0;
}