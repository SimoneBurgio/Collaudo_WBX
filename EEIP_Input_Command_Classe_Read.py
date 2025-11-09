from EEIP_Class import ImpactMurr67
import time
murr = ImpactMurr67("192.168.1.5")
murr.connect()
RUN = True

try:
    while RUN:
            in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, in14, in15, in16 = murr.R_X0()
            x1in1, x1in2, x1in3, x1in4, x1in5, x1in6, x1in7, x1in8, x1in9, x1in10, x1in11, x1in12, x1in13, x1in14, x1in15, x1in16 = murr.R_X1()
            print(in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, in14, in15, in16)
            print(x1in1, x1in2, x1in3, x1in4, x1in5, x1in6, x1in7, x1in8, x1in9, x1in10, x1in11, x1in12, x1in13, x1in14, x1in15, x1in16)
            print("------------------------------------------------------------------")
            time.sleep(2) 
                    
except Exception as e:
    print(f"Errore: {e}")


