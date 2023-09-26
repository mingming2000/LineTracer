#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include "M.hpp"
#include <wiringPi.h>
#include <iostream>
#include <string.h>

using namespace std;	// MCP3008 example
#define SI 0
int main(){
	
	int pin = 2;
	char value;

	wiringPiSetupGpio();			// Setup the library
	pinMode(SI, OUTPUT);

	printf("MCP3008 Example\n");
	spi s;
	spi_open(&s, "/dev/spidev0.0");
	int ret, ch = 0;
	while (true){
		digitalWrite(SI, HIGH);

		for(ch = 1; ch <= 128; ++ch){
			
			if(ch == 1){
				// printf("-------------------------\n");
				// printf("One Cycle Start\n");
				digitalWrite(SI, LOW);
			}

			if(ch == 127){
				ch = 0;
				sleep(1);
				// printf("One Cycle Finish\n");
				// printf("-------------------------\n");
			}
			ret = spi_getadc(&s, 0);
			printf(">> %d___\r", ret);
			// printf(">> %d/1023\r", ret);
		}
	}
	spi_close(&s);
	return 0;
}