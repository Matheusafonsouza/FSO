#include <stdio.h>
#include <stdlib.h>

int main()
{
  int read, count = 0;

  while (scanf(" %d", &read) != EOF)
  {
    count++;
  }

  printf("%d\n", count);

  return 0;
}