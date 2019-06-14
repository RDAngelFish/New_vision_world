#include "embARC.h"
#include "embARC_debug.h"
#include "stdlib.h"
#include "embARC_error.h"
#include "board.h"
#include "dev_uart.h"

#include "vlsi_ftdi.h"

char rx_buf[256] = {0};
int rx_flag = 0;

static void rx_cb(void* ptr)
{
    DEV_UART * uart_obj = (DEV_UART*)ptr;
    int rd_avail = 0;
    int cnt = 0;
    
    uart_obj->uart_control(UART_CMD_GET_RXAVAIL, (void*)(&rd_avail));
    
    while (rd_avail > 0) 
    {
        cnt = (rd_avail < UART_MAX_RX)? rd_avail:(UART_MAX_RX-1);
        uart_obj->uart_read((void*)(rx_buf + rx_flag), cnt);
        rx_flag += cnt;
        uart_obj->uart_control(UART_CMD_GET_RXAVAIL, (void*)(&rd_avail));
    }
}

int vlsi_ftdi_init(VLSI_FTDI *obj, int baudrate)
{
    obj->uart = uart_get_dev(2);                  //UART2 in ARDUINO
    int32_t ercd = obj->uart->uart_open(baudrate);
    if (ercd != E_OK && ercd != E_OPNED) 
    {
        EMBARC_PRINTF("FTDI INIT ERROR\r\n");
        return -1;
    }
    
    EMBARC_PRINTF("FTDI INIT OK\r\n");
    
    obj->uart->uart_control(UART_CMD_SET_RXCB, (void*)rx_cb);
    obj->uart->uart_control(UART_CMD_SET_RXINT, 1);
    
    for (int i = 0; i < 256; ++i) 
    {
        obj->rx.rx_buf[i] = 0;
    }
    
    obj->rx.rx_index = 0;
    
    DEV_UART_INFO_SET_EXTRA_OBJECT(&(obj->uart->uart_info), &(obj->rx));
    
    return 0;
}

int vlsi_ftdi_test(VLSI_FTDI *obj)
{
    int f = -2;
    
    while (f == -2)
    {
        obj->uart->uart_write("vlsi", 4);
        
        for (int i = 0; i < 20; i++) 
        {
            board_delay_ms(5,1);
            
            if (strstr(rx_buf, "vlsi") != NULL)
            {
                EMBARC_PRINTF("break\r\n");
                
                EMBARC_PRINTF("--------------------------\r\n");
                EMBARC_PRINTF("reply rxbuf: %s\r\n", rx_buf);
                EMBARC_PRINTF("--------------------------\r\n");
            
                f = 0;
            
                for (int j = 0; j < 256; ++j)
                {
                    rx_buf[j] = 0;
                }
                
                rx_flag = 0;
                return f;
            }
        }
        EMBARC_PRINTF("time out\r\n");
    }
    
    return f;
}

int vlsi_ftdi_send_uint(VLSI_FTDI *obj, unsigned int data_u32)
{
    obj->uart->uart_write("vlsi", 4);
        
    unsigned char data_u8[4];
    data_u8[3] = (unsigned char)(data_u32 % 256);               // 0 ~  7
    data_u8[2] = (unsigned char)((data_u32 / 256) % 256);       // 8 ~ 15
    data_u8[1] = (unsigned char)((data_u32 / 65536) % 256);     //16 ~ 23
    data_u8[0] = (unsigned char)((data_u32 / 16777216) % 256);  //24 ~ 31
                
    obj->uart->uart_write(data_u8, 4); 
    
    obj->uart->uart_write("OK", 2); 
        
    return 0;
}

int vlsi_ftdi_receive(VLSI_FTDI *obj, int *buf)
{
    while((rx_buf[48] != 'O') || (rx_buf[49] != 'K'))       //Need time out
    {
        board_delay_ms(5,1);
    }
        
    //Combine High 8-bit and Low 8-bit
    for (int i = 0; i < 22; i++)
    {
        buf[i] = ((unsigned int)rx_buf[2 * i + 4]) * 256 + (unsigned int)rx_buf[2*i + 5];
    }   
    
    for (int j = 0; j < 256; ++j)
    {
        rx_buf[j] = 0;
    }
    
    rx_flag = 0;
    
    return 0;
}

