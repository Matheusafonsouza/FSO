#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>

int count = 0;

void handleTerm(int sig)
{
  printf("Recebi %d\n", sig);
  if (count == 2)
  {
    count++;
    puts("Senha acionada");
  }
  else
  {
    count = 0;
  }
}

void handleUsr1(int sig)
{
  printf("Recebi %d\n", sig);
  if (count == 3)
  {
    puts("Tchau");
    exit(0);
  }
  else
  {
    count = 0;
  }
}

void handleUsr2(int sig)
{
  printf("Recebi %d\n", sig);
  if (count == 1)
  {
    count++;
  }
  else
  {
    count = 0;
  }
}

void handleInt(int sig)
{
  printf("Recebi %d\n", sig);
  count = 1;
}

int main()
{
  signal(SIGTERM, handleTerm);
  signal(SIGUSR1, handleUsr1);
  signal(SIGUSR2, handleUsr2);
  signal(SIGINT, handleInt);
  while (1)
  {
    pause();
  }
}