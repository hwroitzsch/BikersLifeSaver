/*
From the command-line:

  gpio -x mcp3004:200:0 aread 200

That should read the first channel on the 3008 - the 3004 is the same chip with just 4 channels. Assumes it's on SPI bus 0. (the trailing :0)

In code:
*/

#include <stdio.h>
#include <wiringPi.h

#define BASE 200
#define SPI_BUS 0

main ()
{
	wiringPiSetup();
	mcp3004Setup(BASE, SPI_BUS);
	printf("Bus SPI_BUS is: %d\n", analogRead(BASE));
}
