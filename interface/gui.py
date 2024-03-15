import customtkinter
from typing import Union, Callable, Any
import threading
from kabum import Kabum
from interface import function

class PopFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = customtkinter.CTkLabel(self)
        self.grid_columnconfigure(0, weight=1)

    def mensage(self, text):
        self.label.configure(text=text)
        self.label.grid(row=0, column=0)
        self.grid(row=1, column=0, padx=8, pady=8,
                  sticky="ewn", ipadx=8, ipady=8)

class SearchFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sig = True

        self.popframe = PopFrame(master=self.master)

        self.label = customtkinter.CTkLabel(self, text='Link')
        self.label.grid(row=0, column=0)
        self.label.grid_columnconfigure(0, weight=1)

        self.input_link = customtkinter.CTkEntry(self)
        self.input_link.grid(row=0, column=1, padx=8, pady=8, sticky="nesw")

        self.grid_columnconfigure(1, weight=1)
        self.grid_configure(row=0, column=0,)

        self.btn_adicionar = self.buttons(
            text='Adicionar', bg_color='#3ab42f', hover_color='#49E13B', command=self.action_adicionar)
        self.btn_adicionar.grid(row=1, column=0, padx=8, stick='nesw')

        self.btn_monitorar = self.buttons(
            text='Monitorar', bg_color='#22619c', hover_color='#2B7AC3', command=self.action_monitorar)
        self.btn_monitorar.grid(row=1, column=1, padx=8, stick='nesw')

    def buttons(self, text='', bg_color='blue', hover_color='blue', size=16, command: Union[Callable[[], Any], None] = None):
        my_font = customtkinter.CTkFont(size=size, weight='bold')
        button = customtkinter.CTkButton(
            self, text=text, fg_color=bg_color, hover_color=hover_color,  font=my_font, command=command)
        return button

    def action_adicionar(self):
        self.popframe.grid_remove()
        if function.verify_link(self.input_link.get()):
            try:
                link = threading.Thread(target=Kabum, args=(
                    self.input_link.get(),)).start()
                self.popframe.grid_remove()
            except:
                pass
        else:
            self.popframe.mensage("Verifique se o link é do site Kabum.")

        self.input_link.delete(0, len(self.input_link.get()))

    def cancel_monitor(self):
        if not self.sig:
            self.btn_monitorar = self.buttons(
                text='Monitorar', bg_color='#22619c', hover_color='#2B7AC3', command=self.action_monitorar)
            self.btn_monitorar.grid(row=1, column=1, padx=8, stick='nesw')
            self.sig = True
            return True

    def monitor(self):
        self.popframe.grid_remove()
        try:
            lines = function.get_links_sheets_file()
            self.btn_stop_monitorar = self.buttons(
                text='Para Monitoramento', bg_color='#F12C2C', hover_color='#EE3C3C', command=self.stop_monitorar)
            self.btn_stop_monitorar.grid(row=1, column=1, padx=8, stick='nesw')
            while True:
                threads = list()
                for i in lines:
                    threads.append(threading.Thread(target=Kabum, args=(i,)))

                i = 0
                if len(threads) > 3:  # VERIFICA SE EXISTE MIAS DE 3 PRODUTOS PARA ANALIZAR E ABRE APENAS 3 THREADS POR VEZ PARA NAO TRAVAR A MAQUINA
                    for index, thread in enumerate(threads):
                        thread.start()
                        i += 1
                        if i >= 3:
                            thread.join()
                            i = 0
                else:
                    for thread in threads:
                        thread.start()

                    for thread in threads:
                        thread.join()

                if self.cancel_monitor():
                    break
        except:
            self.popframe.mensage(
                "Ainda não existe nenhum produto para monitorar")

    def stop_monitorar(self):
        self.sig = False
        self.btn_stop_monitorar.configure(
            text='Finalizando...', state="disabled")

    def action_monitorar(self):
        threading.Thread(target=self.monitor).start()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame = SearchFrame(master=self)
        self.top_frame.grid(row=0, column=0, padx=8, pady=8,
                            sticky="ewns", ipadx=8, ipady=8)

        self.pop_frame = PopFrame(master=self)
        self.pop_frame.grid_remove()

        self.title("Monitor de Preço")
        self.geometry("500x500+1500+100")
        # self.minsize(400, 165)
        # self.maxsize(400, 165)
        self.mainloop()
