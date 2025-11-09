import flet as ft
from EEIP_Class import ImpactMurr67
import time
import threading

murr = ImpactMurr67("192.168.1.5")

def main(page: ft.Page):
    page.title = "Collaudo WBX"
    page.bgcolor = ft.Colors.GREY_200

    connesso = False

# FUNZIONE AGGIORNAMENTO STATO SERRATURE 
    def aggiorna_stato_serrature():

        # Funzione di aggiornamento della UI
        def esegui_aggiornamento_ui(p0, p1, p2, p3):
            try:
                for i in range(4):
                    elementi_serrature_0[i].bgcolor = ft.Colors.GREEN_500 if p0[i] else ft.Colors.RED_200
                    elementi_serrature_1[i].bgcolor = ft.Colors.GREEN_500 if p1[i] else ft.Colors.RED_200
                    elementi_serrature_2[i].bgcolor = ft.Colors.GREEN_500 if p2[i] else ft.Colors.RED_200
                    elementi_serrature_3[i].bgcolor = ft.Colors.GREEN_500 if p3[i] else ft.Colors.RED_200
                
                page.update()  
                
            except Exception as e:
                print(f"Errore durante l'aggiornamento UI: {e}")


        # Funzione di 
        while True:
            if connesso:
                try:
                    port0_in = murr.R_In_WBX(0) 
                    port1_in = murr.R_In_WBX(1)
                    port2_in = murr.R_In_WBX(2)
                    port3_in = murr.R_In_WBX(3)

                    # "page.run_thread" significa: fai eseguire questa funzione al thread UI principale,
                    # in quanto lui è l'unico che può modificare gli elementi grafici 
                    page.run_thread(esegui_aggiornamento_ui,port0_in, port1_in, port2_in, port3_in)

                except Exception as e:
                    print(f"Errore nel thread di aggiornamento: {e}")

            time.sleep(0.3)

    scan_thread = threading.Thread(target=aggiorna_stato_serrature, daemon=True)
    scan_thread.start()


    titolo_principale = ft.Text(
        value="Collaudo WBX",
        size=50,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE,
        font_family="Segoe UI"
    )

#----------------------------------------------------------------------------------------------#

    #FUNZIONE CONNESSIONE
    def connessione(e):
        nonlocal connesso
        time.sleep(1)
        try:
            if connesso == False:
                
                murr.connect()
                print("Connessione avvenuta con successo!")
                e.control.bgcolor = ft.Colors.GREEN
                e.control.content.value = "Disconnetti"
                e.control.update()
                connesso = True
            else:
                murr.deconnect()
                print("Disconnesso con successo!")
                e.control.bgcolor = ft.Colors.RED_200
                e.control.content.value = "Connetti"
                e.control.update()
                connesso = False
        except Exception as e:
            print(e)

    #FUNZIONE APERTURA SERRATURA - Comanda la classe dedicata
    def apri_serratura(e): #La "e" indica l'evento del click, e si porta dietro tutti i parametri del bottone. Si può cambiare con ciò che si vuole
        master_id = e.control.data["master"]
        lock_id = e.control.data["lock"]
        print(f"Master X{master_id} => Serratura porta X{lock_id} aperta!")

        # Comando apertura serratura
        murr.W_Locks_WBX(master_id,lock_id,1)
        time.sleep(0.2)
        murr.W_Locks_WBX(master_id,lock_id,0)
        e.control.update()

    #FUNZIONE ACCENSIONE LED
    def accendi_led(e):
        master_id = e.control.data
        if e.control.bgcolor == ft.Colors.RED:
            e.control.bgcolor = ft.Colors.GREEN_500
            e.control.content.value = "LED (ON)"
            print(f"Master X{master_id} => LED acceso!")
            murr.W_Led_WBX(master_id,1)

        else:
            e.control.bgcolor = ft.Colors.RED
            print(f"Master X{master_id} => LED spento!")
            e.control.content.value = "LED (OFF)"
            murr.W_Led_WBX(master_id,0)
        e.control.update()



#-------------------------------------------------------------------------------------------------#

    # --- MASTER 0 ---
    titolo_master_0 = ft.Container(
        content=ft.Text(
            value="Master\nX0",
            size=25,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            font_family="Segoe UI"
        ),
        bgcolor=ft.Colors.BLUE,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        alignment=ft.alignment.center,
    )

    elementi_serrature_0 = [
        ft.CupertinoButton(
            content=ft.Text("Lock X0", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 0, "lock": 0}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X1", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 0, "lock": 1}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X2", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 0, "lock": 2}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X3", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 0, "lock": 3}
        ),
    ]



    pulsante_led_0 = ft.CupertinoButton(
        content=ft.Text("LED (OFF)", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
        bgcolor=ft.Colors.RED, on_click=accendi_led, data=0
    )

    colonna_contenuto_0 = ft.Column(
        controls=elementi_serrature_0 + [pulsante_led_0],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    container_colonna_0 = ft.Container(
        content=ft.Column(
            controls=[titolo_master_0, colonna_contenuto_0],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400), # Leggermente più scuro per visibilità
        border_radius=10,
        padding=ft.padding.all(10),
        width=180,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.GREY_500, offset=ft.Offset(10,5)),
    )

    # --- MASTER 1 ---
    titolo_master_1 = ft.Container(
        content=ft.Text(
            value="Master\nX1",
            size=25,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            font_family="Segoe UI"
        ),
        bgcolor=ft.Colors.BLUE,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        alignment=ft.alignment.center,
    )

    elementi_serrature_1 = [
        ft.CupertinoButton(
            content=ft.Text("Lock X0", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 1, "lock": 0}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X1", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 1, "lock": 1}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X2", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 1, "lock": 2}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X3", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 1, "lock": 3}
        ),
    ]

    pulsante_led_1 = ft.CupertinoButton(
        content=ft.Text("LED (OFF)", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
        bgcolor=ft.Colors.RED, on_click=accendi_led, data=1
    )

    colonna_contenuto_1 = ft.Column(
        controls=elementi_serrature_1 + [pulsante_led_1],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    container_colonna_1 = ft.Container(
        content=ft.Column(
            controls=[titolo_master_1, colonna_contenuto_1],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=ft.padding.all(10),
        width=180,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.GREY_500, offset=ft.Offset(10,5)),
    )

    # --- MASTER 2 ---
    titolo_master_2 = ft.Container(
        content=ft.Text(
            value="Master\nX2",
            size=25,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            font_family="Segoe UI"
        ),
        bgcolor=ft.Colors.BLUE,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        alignment=ft.alignment.center,
    )

    elementi_serrature_2 = [
        ft.CupertinoButton(
            content=ft.Text("Lock X0", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 2, "lock": 0}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X1", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 2, "lock": 1}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X2", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 2, "lock": 2}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X3", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 2, "lock": 3}
        ),
    ]

    pulsante_led_2 = ft.CupertinoButton(
        content=ft.Text("LED (OFF)", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
        bgcolor=ft.Colors.RED, on_click=accendi_led, data=2
    )

    colonna_contenuto_2 = ft.Column(
        controls=elementi_serrature_2 + [pulsante_led_2],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    container_colonna_2 = ft.Container(
        content=ft.Column(
            controls=[titolo_master_2, colonna_contenuto_2],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=ft.padding.all(10),
        width=180,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.GREY_500, offset=ft.Offset(10,5)),
    )

    # --- MASTER 3 ---
    titolo_master_3 = ft.Container(
        content=ft.Text(
            value="Master\nX3",
            size=25,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            font_family="Segoe UI"
        ),
        bgcolor=ft.Colors.BLUE,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        alignment=ft.alignment.center,
    )

    elementi_serrature_3 = [
        ft.CupertinoButton(
            content=ft.Text("Lock X0", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 3, "lock": 0}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X1", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 3, "lock": 1}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X2", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 3, "lock": 2}
        ),
        ft.CupertinoButton(
            content=ft.Text("Lock X3", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.GREY_200, on_click=apri_serratura, data={"master": 3, "lock": 3}
        ),
    ]

    pulsante_led_3 = ft.CupertinoButton(
        content=ft.Text("LED (OFF)", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
        bgcolor=ft.Colors.RED, on_click=accendi_led, data=3
    )

    colonna_contenuto_3 = ft.Column(
        controls=elementi_serrature_3 + [pulsante_led_3],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    container_colonna_3 = ft.Container(
        content=ft.Column(
            controls=[titolo_master_3, colonna_contenuto_3],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=ft.padding.all(10),
        width=180,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.GREY_500, offset=ft.Offset(10,5)),
    )

    


    # COMPOSIZIONE ROW MASTER
    controlli_riga_master = [
        container_colonna_0, 
        container_colonna_1, 
        container_colonna_2, 
        container_colonna_3
    ]

    riga_master = ft.Row(
        controls=controlli_riga_master,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
        wrap=True, # Permette di andare a capo su schermi piccoli
        run_spacing=40, # Spaziatura verticale quando va a capo
    )


    # PULSANTE CONNETTI/DISCONNETTI
    pulsante_connetti = ft.ElevatedButton(
            content=ft.Text("Connetti", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
            bgcolor=ft.Colors.RED_200, on_click=connessione, data={"master": 0, "lock": 0},
            width=150, height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))
        )
    
    # LAYOUT PRINCIPALE CONTENTENTE IL TITOLO E LA ROW DEI MASTER
    layout_principale = ft.Column(
        controls=[
            ft.Container(content=titolo_principale, alignment=ft.alignment.center, padding=20),
            riga_master
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # AGGIUNTA LAYOUT ALLA PAGINA
    page.add(pulsante_connetti, layout_principale)
    page.update()

#   ESECUZIONE
if __name__ == "__main__":
    ft.app(main)
