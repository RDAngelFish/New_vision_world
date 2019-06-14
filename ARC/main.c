#include "embARC.h"
#include "board.h"
#include "dev_uart.h"
#include "dev_pinmux.h"

#include "vlsi_ftdi.h"
#include "vlsi_svm.h"

#include <stdio.h>
#include <stdlib.h>
#include "embARC_debug.h"

struct vlsi_ftdi *vlsi_ftdi_obj;

int main(void)
{
    //io_pmod_config(PMOD_C, PMOD_UART, IO_PINMUX_ENABLE);    //PMOD_C = UART1    mux.c   line 281
    io_arduino_config_uart(IO_PINMUX_ENABLE);               //ARDUINO = UART2   mux.c   line 255

    vlsi_ftdi_obj = (VLSI_FTDI*)malloc(sizeof(VLSI_FTDI));
    
    vlsi_ftdi_init(vlsi_ftdi_obj, 115200);
    
    
    int f = 0;
    f = vlsi_ftdi_test(vlsi_ftdi_obj);
    EMBARC_PRINTF("test %d \r\n", f);
    board_delay_ms(1000, 1);

    //0 float X_test_T_0[20] = { 1.11, 1.36, 1.66, 1.64, 1.8, 1.69, 1.84, 1.69, 2.18, 1.57, 0.63, 1.42, 0.42, 1.71, 0.22, 1.77, 0.02, 1.76, -0.22, 1.58 };
    //1 float X_test_T_1[20] = { 0.24, 1.32, 0.22, 1.32, 0.23, 1.24, 0.22, 1.22, 0.31, 1.28, -0.24, 0.86, -0.18, 0.91, -0.25, 0.84, -0.25, 0.84, -0.23, 0.84 };
    //2 float X_test_T_2[20] = { 1.03, -1.39, 1.02, -1.41, 1.06, -1.2, 1.06, -1.16, 1.06, -1.11, 1.04, -0.78, 1.01, -0.23, 1.01, -0.22, 1.0, -0.24, 0.98, -0.31 };
        
    int real_data[22];
    
    float predict_data[20];
    
    while(1)
    {
        //Receive data from OpenPose
        vlsi_ftdi_receive(vlsi_ftdi_obj, real_data);
        
        //Pre-Process
        for (int i = 0; i < 10; i++)
        {
            predict_data[2 * i] = ((float)real_data[2 * i + 2] - (float)real_data[0]) / 100;
            predict_data[2 * i + 1] = ((float)real_data[2 * i + 3] - (float)real_data[1]) / 100;
        }  
            
        //SVM Predict
        int final_anw = 0;
        final_anw = vlsi_svm_predict(predict_data);

        //Sound
        unsigned int voice_info;    //0~27  left~right  28 reserved : 29 cymbals : 30 drum : 31 piano
        int piano_index;
        
        voice_info = 0;
        
        //Piano
        if(final_anw == 0)
        {
            voice_info |= 0x1 << 31;
            for (int i = 0; i < 10; i++)
            {
                if(real_data[2*i + 3] > 400)    //y
                {
                    //bound
                    if(real_data[2*i + 2] < 54)                     //left bound 320 - 14 * 19
                    {
                        real_data[2*i + 2] = 54;
                    }
                    else if (real_data[2*i + 2] > 586)              //right bound 320 + 14 * 19
                    {
                        real_data[2*i + 2] = 586;
                    }
                                    
                    piano_index = (real_data[2*i + 2] - 54) / 19;   //left offset
                    voice_info |= 0x1 << piano_index;
                }
            } 
        }
        //Drum
        else if(final_anw == 1)
        {
            voice_info |= 0x1 << 30;
            if(real_data[3] > 355)          //y
            {
                if(real_data[2] < 370)      //x
                {
                    voice_info |= 0x1 << 1;
                }
                else if(real_data[2] < 420) //x
                {
                    voice_info |= 0x1 << 0;
                }
            }
            if(real_data[13] > 355)          //y
            {
                if(real_data[12] > 270)      //x
                {
                    voice_info |= 0x1 << 2;
                }
                else if(real_data[2] > 220) //x
                {
                    voice_info |= 0x1 << 3;
                }
            }
        }
        //Cymbals
        else
        {
            voice_info |= 0x1 << 29;
            if(abs(real_data[2] - real_data[12]) < 30)      //x
            {
                if(abs(real_data[3] - real_data[13]) < 5)   //y
                {
                    voice_info |= 0x1 << 0;
                }
                else                                        //y
                {
                    voice_info |= 0x1 << 1;
                }
            }
            
        }
        vlsi_ftdi_send_uint(vlsi_ftdi_obj, voice_info);
        
        EMBARC_PRINTF("voice information : %d %d\r\n", final_anw, voice_info);
    }
    
    return E_OK;
}

