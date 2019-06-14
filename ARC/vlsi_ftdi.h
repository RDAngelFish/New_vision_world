#ifndef VLSI_FTDI_H
#define VLSI_FTDI_H

#include "dev_uart.h"

#define MAX_UART_BUF_SIZE   256
#define UART_MAX_RX         100


/** \brief FTDI recieve buffer, the communication port is UART */
typedef struct uart_buf
{
  char rx_buf[256];
  int rx_index;
} UART_BUF;

/** \brief FTDI device object */
typedef struct vlsi_ftdi
{
  DEV_UART *uart;
  UART_BUF rx;
} VLSI_FTDI;

/** \brief ftdi initial
*          Register the uart device, and initial the device
*   \param baudrate: ftdi baudrate, suggest 115200
*/
int vlsi_ftdi_init(VLSI_FTDI *obj, int baudrate);

/** \brief ftdi test
*          Test function. Sent to command for test. If the ftdi not reply, try to fix.
*/
int vlsi_ftdi_test(VLSI_FTDI *obj);

/** \brief ftdi send unsigned integer
*          Send data. Data Type int -> char .
*/
int vlsi_ftdi_send_uint(VLSI_FTDI *obj, unsigned int data_u32);

/** \brief ftdi receive
*          Receive data for SVM predict. Data Type char -> int .
*/
int vlsi_ftdi_receive(VLSI_FTDI *obj, int *buf);



#endif