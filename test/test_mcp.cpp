#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include "M.hpp"

// MCP3008 example

int main(){
	printf("MCP3008 Example\n");
	spi s;
	spi_open(&s, "/dev/spidev0.0");
	int ret, ch = 0;
	while (true){
		
		ret = spi_getadc(&s, 0);
		printf("channel: got: %d/1023\n",ret);
		++ch;
		
	}
	spi_close(&s);
	return 0;
}