#external modules
from tkinter import Tk
import logtools
import time
import os
from datetime import datetime
import configparser
import clr

#local modules                   
from loghandler import Log
from ulitahandler import ProgramHandler, START_BTN_POS, serial_n_input_pos
from GUI_popups import MainApplication
from hotkeys import CloseHotkeyWaiter
from grr_generator import GRR, generate_grr_savename

config = configparser.ConfigParser()
config.read('config\settings.ini')

newtonsoftjson_path = config["Paths"]["Newtonsoft.Json.Dll"]
wsconnector_path = config["Paths"]["WSConnector.Dll"]

clr.AddReference(newtonsoftjson_path)
clr.AddReference(wsconnector_path)
from WSConnector import Connector

#imported info from .ini settings file
station_name = config['Process']['StationName']
expected_part_number = config['Process']['PartNumber']

logs_path = config['Paths']['OutputLogs']
ulita_cwd = config["Paths"]['UlitaCwd']

backcheck_serial_enabled = config["Default"]["BackcheckSerial"]
validate_partnumber_enabled = config["Default"]["ValidatePartNumber"]
insertprocess_data_enabled = config["Default"]["InsertProcessData"]
only_pass_enabled = config["Default"]["OnlyInsertPass"]

test_start_time = None
test_end_time = None

def main():

    #Se define el objeto gui_app, el cual contendra las funciones para 
    #mostrar mensajes a lo largo de la prueba
    root = Tk()
    root.withdraw()
    gui_app = MainApplication(root)

    #se define la coneccion con la dll de traceabilidad, ws connector
    connector = Connector() #traceability connection
    
    #se define el objeto "ulita" el cual contiene funciones basicas para
    #manipular la aplicacion ulita del FCCA TESTER(abrir, cerrar, hacer clicks, etc)
    ulita = ProgramHandler("ULITA", ulita_cwd)
    
    #el siguiente objeto estara corriendo un hilo constantemente el cual esperara
    #al comando shift + esc, para cerrar la aplicacion junto con ulita
    close_waiter = CloseHotkeyWaiter(ulita)
    close_waiter.start()

    #si la aplicacion ulita no esta abierta hasta aqui, se abre la aplicacion
    if not ulita.opened:
        ulita.open()
        time.sleep(1)

    while ulita.opened:

        #se abre ventana que pide escanear la pieza
        askserial_window =  gui_app.ask_serial()

        #se espera hasta que el serial se guarde
        gui_app.wait_window_destroy(askserial_window)
        if gui_app.serial == None:
            continue

        #funcion que valida la cantidad de caracteres del serial y su numero de parte
        def valid_serial(serial):
            # return True
            if len(serial) != 14:
                msg_window = gui_app.message("SERIAL '{1}' NO VALIDO".format(serial), "orange")
                gui_app.wait_window_destroy(msg_window)
                return False
            else:
                if validate_partnumber_enabled == 'yes':
                    serial_partnumber = ""
                    resp, serial_partnumber = connector.CIMP_PartNumberRef(serial,1, serial_partnumber)

                    if expected_part_number != serial_partnumber:
                        msg_window = gui_app.message("NUMERO DE PARTE NO COINCIDE\nExpected: {0}\nReceived: {1}".format(expected_part_number, serial_partnumber), "orange")
                        gui_app.wait_window_destroy(msg_window)

                        #----------------------------------------------------------------------
                        #aqui puede ir mensaje al operador para retirar la pieza del fixture
                        msg_window = gui_app.message("RETIRE LA PIEZA Y\n TOME UNA NUEVA", "blue")
                        gui_app.wait_window_destroy(msg_window)
                        #----------------------------------------------------------------------
                        return False
                        
                    else:
                        return True
                else:
                    return True
            
            
        
        if not valid_serial(gui_app.serial):
            continue

        #se hace el backcheck de la pieza
        if backcheck_serial_enabled == 'yes':

            resp = connector.BackCheck_Serial(gui_app.serial, station_name)
        else:
            resp = "1|TEST FINAL FUNCTIONAL"      

        #se determina si el backcheck fue aprobatorio
        if not resp == "1|TEST FINAL FUNCTIONAL":
            msg_window = gui_app.message("FALLA EN BACKCHECK\nresponse: " + resp, "orange")
            gui_app.wait_window_destroy(msg_window)

            #----------------------------------------------------------------------
            #aqui puede ir mensaje al operador para retirar la pieza del fixture
            msg_window = gui_app.message("RETIRE LA PIEZA Y\n TOME UNA NUEVA", "blue")
            gui_app.wait_window_destroy(msg_window)
            #----------------------------------------------------------------------

            #la palabra reservada continue, descarta el ciclo actual del loop, y continua con el siguiente
            #ciclo desde el principio
            continue

        
        
        time.sleep(2)
    
        ulita.click(START_BTN_POS)

        # delay de 4 segundos, es el tiempo estimado para poder insertar el serial en 
        #la aplicacion ulita
        time.sleep(4)
        ulita.click(serial_n_input_pos)

        ulita.typewrite(gui_app.serial)
        time.sleep(2)
        #-------------------------------------------------------------------
        #aqui puede ir mensaje al operador para poner la pieza en el fixture
        msg_window = gui_app.message("INSERTE LA PIEZA EN EL FIXTURE", "blue")
        gui_app.wait_window_destroy(msg_window)
        #-------------------------------------------------------------------

        #-----------------------------------------------------------------------------
        #aqui se le puede pedir al operador bajar el fixture
        #-----------------------------------------------------------------------------

        #se obtiene la fecha del momento actual, para tomarla como referencia
        #tal referencia servira para saber si se a creado el log de la prueba actual
        ref_date = datetime.now()

        #el siguiente waile espera hasta que se cree el log de la prueba actual
        while not logtools.dut_log_exists(logs_path, ref_date):
            time.sleep(1)
            print("waiting for log")


        #a partir de aqui empieza el TEST FUNCTIONAL, se guarda la fecha con hora
        test_start_time = str(datetime.now())[:19]
        ulita.busy = True


        #se crea el objeto log, en base al archivo log recien generado, que se estara
        #escribiendo durante todo el test funcional
        log_path = logtools.get_newer_log(logs_path)
        dut_log = Log(log_path)


        counter = 0



        #este while espera a que el log se termine de escribir,
        #lo que a su vez significa, que la prueba termine
        while not dut_log.write_completed():
            if dut_log.write_stopped():
                print("test has manualy stoped")
                gui_app.message("LA PRUEBA SE DETUVO MANUALMENTE", "red")
            counter += 1
            print(str(counter) + ": tests not finished yet")
            time.sleep(1)

        #la prueba termina, se guarda la fecha de terminacion de la prueba
        test_end_time = str(datetime.now())[:19]
        ulita.busy = False


        #si se encuentran fallas en el log, se extrae el failstring del log,
        #de lo contrario, no se genera el failstring.
        #ademas se obtiene el status en este if
        if dut_log.has_fails():

            fail_string = dut_log.get_failstring()
            status = 0
            msg_window = gui_app.message("TEST FUNCTIONAL FAILED", "red", 40)
        else:
            msg_window = gui_app.message("TEST FUNCTIONAL PASSED", "green")
            fail_string = ""
            status = 1
        
        print("fail string: ", fail_string)
        
        gui_app.wait_window_destroy(msg_window)

        #se manda el resultado a traceabilidad

        def insert_process_data():
            return connector.InsertProcessDataWithFails(gui_app.serial,
                                                        station_name,
                                                        "TEST FINAL FUNCTIONAL",
                                                        test_start_time,
                                                        test_end_time,
                                                        status,
                                                        fail_string,
                                                        "employee")

        if insertprocess_data_enabled == 'yes':
            if only_pass_enabled == 'yes':
                if status == 1:
                    reply = insert_process_data()
                else:
                    reply = "OK"
            else:
                reply = insert_process_data()
        else:
            reply = "OK"


        #se determina si los datos se subieron correctamente a traceabilidad
        #dependiendo de la respusta, se mostrara un mensaje indicandolo
        if reply != "OK":
            msg_window = gui_app.message("FALLA AL SUBIR A TRACEABILIDAD: \n"+ reply, "red")
            gui_app.wait_window_destroy(msg_window)
        

        
        grr_path = generate_grr_savename()

        # se agregan los resultados al grr
        if os.path.isfile(grr_path):
            grr = GRR(grr_path, file_exists=True)
            grr.append_log(dut_log.path)
        else:
            grr = GRR(grr_path)
            grr.append_log(dut_log.path)

        
        #----------------------------------------------------------------------
        #aqui puede ir mensaje al operador para retirar la pieza del fixture
        msg_window = gui_app.message("RETIRE LA PIEZA Y\n TOME UNA NUEVA", "blue")
        gui_app.wait_window_destroy(msg_window)
        #----------------------------------------------------------------------

        
    root.destroy()
    root.mainloop()
    os._exit(1)

if __name__ == "__main__":
    main()