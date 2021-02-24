#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdlib.h>

char name[100];

void readName()
{
  int scanfReturn;

  scanfReturn = scanf(" %s", name);
  if (scanfReturn == EOF)
  {
    exit(0);
  }
}

void handleTerm()
{
  readName();
  if (strcmp(name, "Con2") == 0)
  {
    puts("Certo");
  }
  else
  {
    puts("Erro");
  }
}

void handleUsr1()
{
  readName();
  if (strcmp(name, "Igor3k") == 0)
  {
    puts("Certo");
  }
  else
  {
    puts("Erro");
  }
}

void handleUsr2()
{
  readName();
  if (strcmp(name, "Monark") == 0)
  {
    puts("Certo");
  }
  else
  {
    puts("Erro");
  }
}

void handleAlrm()
{
  readName();
  if (strcmp(name, "Silencio") == 0)
  {
    puts("Certo");
  }
  else
  {
    puts("Erro");
  }
}

void handleInt()
{
  readName();
  if (strcmp(name, "Con1") == 0)
  {
    puts("Certo");
  }
  else
  {
    puts("Erro");
  }
}

int main()
{
  signal(SIGTERM, handleTerm);
  signal(SIGUSR1, handleUsr1);
  signal(SIGUSR2, handleUsr2);
  signal(SIGINT, handleInt);
  signal(SIGALRM, handleAlrm);
  while (1)
  {
    pause();
  }
}