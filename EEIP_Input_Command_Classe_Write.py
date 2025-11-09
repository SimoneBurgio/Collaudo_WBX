from EEIP_Class import ImpactMurr67
murr = ImpactMurr67("192.168.1.5")
murr.connect()
RUN = True

try:
    while RUN:
            out = input("seleziona l'out")
            val = input("seleziona il valore")
            if out == "e":
                 RUN = False
                 murr.deconnect()
            else:
                murr.w(2,int(out), int(val))    
                    
except Exception as e:
    print(f"Errore: {e}")

