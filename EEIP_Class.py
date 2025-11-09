from eeip import *

class ImpactMurr67:
    def __init__(self, ip):
        self.client = EEIPClient()
        self.ip = ip

    def connect(self):
        self.client.register_session(self.ip)
        # Originator -> Target (Output)
        self.client.o_t_instance_id = 111
        self.client.o_t_length = 260
        self.client.o_t_requested_packet_rate = 50000 
        self.client.o_t_realtime_format = RealTimeFormat.HEADER32BIT
        self.client.o_t_connection_type = ConnectionType.POINT_TO_POINT

        # Target -> Originator (Input)
        self.client.t_o_instance_id = 101
        self.client.t_o_length = 394
        self.client.t_o_requested_packet_rate = 50000
        self.client.t_o_realtime_format = RealTimeFormat.MODELESS
        self.client.t_o_connection_type = ConnectionType.MULTICAST

        # Ridimensiona le liste dati IO
        self.client.o_t_iodata = [0] * self.client.o_t_length
        self.client.t_o_iodata = [0] * self.client.t_o_length

        # Apre connessione implicita
        self.client.forward_open()

    def deconnect(self):
        self.client.forward_close()
        self.client.unregister_session()



# -------- SCRITTURA USCITE CON BYTE E PIN

    """Scrive il valore specificato (val) su un'uscita digitale specifica (out) 
    all'interno di un byte specifico (byte) dei dati di output del client EEIP."""

    def w(self, byte, out, val):
        try:
            if 0 <= out <= 7:
                bit_position = out
                mask = 1<<bit_position
                if val == 1:
                    self.client.o_t_iodata[byte] |= mask   

                elif val == 0:
                    self.client.o_t_iodata[byte] &= ~mask 
            else:
                print("Inserire un bit tra 0 e 8")
        except ValueError:
            print("Input non valido")




#-------- LETTURA INGRESSI MODULI IO (16 bit per modulo)

    def read_port_data(self, port_number):
        """
        Legge i dati di input da una specifica porta IO-Link (da X0 a X7).
        Estrae 32 byte di dati, ma ne analizza solo i primi 2 (16 bit)
        come ingressi digitali.
        """
        
        input_data = self.client.t_o_iodata
        start_byte = 0
        end_byte = 0


        if port_number == 0:
            start_byte, end_byte = 10, 41
        elif port_number == 1:
            start_byte, end_byte = 50, 81
        elif port_number == 2:
            start_byte, end_byte = 90, 121
        elif port_number == 3:
            start_byte, end_byte = 130, 161
        elif port_number == 4:
            start_byte, end_byte = 170, 201
        elif port_number == 5:
            start_byte, end_byte = 210, 241
        elif port_number == 6:
            start_byte, end_byte = 250, 281
        elif port_number == 7:
            start_byte, end_byte = 290, 321
        else:
            print(f"Errore: Porta {port_number} non valida.")

        # Estrai i byte specifici per la porta
        port_data_bytes = input_data[start_byte:end_byte]

        # Assicurati che ci siano dati prima di provare a convertirli
        if not port_data_bytes:
            print(f"Attenzione: Dati non disponibili per la porta {port_number}.")
            return (False,) * 16

        # Per leggere solo i primi 16 bit, usiamo solo i primi 2 byte.
        inputs_int = int.from_bytes(port_data_bytes[:2], 'little')

        # Estrai i singoli bit
        in1  = (inputs_int & 1)     != 0
        in2  = (inputs_int & 2)     != 0
        in3  = (inputs_int & 4)     != 0
        in4  = (inputs_int & 8)     != 0
        in5  = (inputs_int & 16)    != 0
        in6  = (inputs_int & 32)    != 0
        in7  = (inputs_int & 64)    != 0
        in8  = (inputs_int & 128)   != 0
        in9  = (inputs_int & 256)   != 0
        in10 = (inputs_int & 512)   != 0
        in11 = (inputs_int & 1024)  != 0
        in12 = (inputs_int & 2048)  != 0
        in13 = (inputs_int & 4096)  != 0
        in14 = (inputs_int & 8192)  != 0
        in15 = (inputs_int & 16384) != 0
        in16 = (inputs_int & 32768) != 0

        return (in1, in2, in3, in4, in5, in6, in7, in8, 
                in9, in10, in11, in12, in13, in14, in15, in16)



#----- SCRITTURA USCITE MODULI IO (Serratura + ritorno per connettore)
    def W_Locks_WBX(self, master, porta, valore):
        if master == 0:
            byte = 2
        elif master == 1:
            byte = 34
        elif master == 2:
            byte = 66
        elif master == 3:
            byte = 98   
        elif master == 4:
            byte = 130
        elif master == 5:
            byte = 162
        elif master == 6:
            byte = 194
        elif master == 7:
            byte = 226
        else:
            print("Master non valido")
            return

        if porta == 0:
            out = 1
        elif porta == 1:
            out = 3
        elif porta == 2:
            out = 5
        elif porta == 3:
            out = 7
        elif porta == 4:
            out = 9
        elif porta == 5:
            out = 11
        elif porta == 6:
            out = 13
        elif porta == 7:
            out = 15
        else:
            print("Porta non valida")
            return
             
        try:
            if 0 <= out <= 7:
                bit_position = out
                mask = 1<<bit_position
                if valore == 1:
                    self.client.o_t_iodata[byte] |= mask   

                elif valore == 0:
                    self.client.o_t_iodata[byte] &= ~mask 
        except ValueError:
            print("Input non valido")


#----- SCRITTURA USCITE LED SU MODULO WBX
    def W_Led_WBX(self, master_id, valore):
        if master_id == 0:
            byte = 3
        elif master_id == 1:
            byte = 35
        elif master_id == 2:
            byte = 67
        elif master_id == 3:
            byte = 99
        
        try:
            bit_position = 7
            mask = 1<<bit_position
            if valore == 1:
                self.client.o_t_iodata[byte] |= mask   

            elif valore == 0:
                self.client.o_t_iodata[byte] &= ~mask 
                
        except ValueError:
            print("Input non valido")


# ------ LETTURA INGRESSI SU MODULO WBX
    def R_In_WBX(self, master_id):
        input_data = self.client.t_o_iodata
        start_byte = 0
        end_byte = 0


        if master_id == 0:
            start_byte, end_byte = 10, 41
        elif master_id == 1:
            start_byte, end_byte = 50, 81
        elif master_id == 2:
            start_byte, end_byte = 90, 121
        elif master_id == 3:
            start_byte, end_byte = 130, 161
        elif master_id == 4:
            start_byte, end_byte = 170, 201
        elif master_id == 5:
            start_byte, end_byte = 210, 241
        elif master_id == 6:
            start_byte, end_byte = 250, 281
        elif master_id == 7:
            start_byte, end_byte = 290, 321
        else:
            return f"Errore: Porta {master_id} non valida."

        # Estrai i byte specifici per la porta
        port_data_bytes = input_data[start_byte:end_byte]

        # Assicurati che ci siano dati prima di provare a convertirli
        if not port_data_bytes:
            print(f"Attenzione: Dati non disponibili per la porta {master_id}.")
            return (False,) * 16

        # Per leggere solo i primi 16 bit, usiamo solo i primi 2 byte.
        inputs_int = int.from_bytes(port_data_bytes[:2], 'little')

        # Estrai i singoli bit
        ix0  = (inputs_int & 1)       != 0
        ix1  = (inputs_int & 4)       != 0
        ix2  = (inputs_int & 16)      != 0
        ix3  = (inputs_int & 64)      != 0
        ix4  = (inputs_int & 512)     != 0
        ix5  = (inputs_int & 2048)    != 0
        ix6  = (inputs_int & 8192)    != 0
        ix7  = (inputs_int & 32768)   != 0

        return (ix0, ix1, ix2, ix3, ix4, ix5, ix6, ix7)


    






        


