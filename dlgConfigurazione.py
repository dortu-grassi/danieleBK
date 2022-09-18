## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import gi
import ast

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Msg(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Messaggio", transient_for=parent, flags=0)
        # self.add_buttons(
        #    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        # )

        self.set_default_size(150, 100)
        self.__msg = ""
        self.label = Gtk.Label(label=self.__msg, margin=30)

        box = self.get_content_area()
        box.add(self.label)
        self.set_modal(True)
        # self.show_all()

    def set_msg(self, msg):
        self.label.set_text(msg)
        self.show_all()
    # self.run()


class DlgNuovo(Gtk.Window):
    def __init__(self, fconf):
        super().__init__(title="Nuovo backups")
        self.fconf = fconf
        with open(self.fconf, "r") as data:
            self.bks = ast.literal_eval(data.read())
            data.close()

        # print(self.bks)
        self.set_default_size(400, 300)
        # self.set_border_width(10)
        grid = Gtk.Grid()

        lbl = Gtk.Label(label="Inserisci codice")
        lbl.set_property("margin", 10)
        self.txtCodice = Gtk.Entry()
        self.txtCodice.set_property("width-request", 100)
        self.txtCodice.set_property("margin", 10)
        # self.txtCodice.set_property("height-request",200)
        grid.attach(lbl, 0, 0, 1, 1)
        grid.attach(self.txtCodice, 1, 0, 1, 1)

        lbl = Gtk.Label(label="Inserisci Titolo")
        lbl.set_property("margin", 10)
        self.txtTitolo = Gtk.Entry()
        self.txtTitolo.set_property("width-request", 200)
        self.txtTitolo.set_property("margin", 10)
        grid.attach(lbl, 0, 1, 1, 1)
        grid.attach(self.txtTitolo, 1, 1, 1, 1)

        # *************** pulsantiera
        hbox = Gtk.Box(margin=10, spacing=6)
        # hbox.set_property("height-request", 200)

        button = Gtk.Button.new_with_mnemonic("Annulla")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_annulla_clicked)
        hbox.add(button)

        button = Gtk.Button.new_with_mnemonic("Salva")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_salva_clicked)
        hbox.add(button)
        grid.attach(hbox, 1, 2, 1, 1)

        self.add(grid)

    def pulisci(self, s):
        s = s.replace("à", "a")
        s = s.replace("è", "e")
        s = s.replace("é", "e")
        s = s.replace("ì", "i")
        s = s.replace("ò", "o")
        s = s.replace("ù", "u")
        s = s.replace("À", "a")
        s = s.replace("È", "e")
        s = s.replace("É", "e")
        s = s.replace("Ì", "i")
        s = s.replace("Ò", "o")
        s = s.replace("Ù", "o")
        return s

    def __esisteCodice(self, s):
        # print("esisteCodice")
        return s in self.bks

    def __salvaNuovo(self, ch, titolo):
        # print("salvaNuovo")
        self.bks[ch] = {'titolo': titolo}
        with open(self.fconf, "w") as data:
            data.write(str(self.bks))
            data.close()

    def on_annulla_clicked(self, bt):
        # print("annulla")
        self.destroy()

    def on_salva_clicked(self, bt):
        # print("Salva")
        self.msg = Msg(self)
        if self.txtCodice.get_text().isalpha():
            ch = self.pulisci(self.txtCodice.get_text())
            if self.__esisteCodice(ch):
                self.msg.set_msg("Codice esistente")
            else:
                titolo = self.txtTitolo.get_text()
                if len(titolo) == 0:
                    self.msg.set_msg("Inserisci il titolo")
                else:
                    self.__salvaNuovo(ch, titolo)
                    self.destroy()
        else:
            self.msg.set_msg("NON puoi inserire nel codice caratteri diversi da quelli dell'alfabeto")


class DlgConf(Gtk.Window):
    def __init__(self,fconf, chDiz):
        super().__init__(title="Configurazione backups")
        print(chDiz)
        with open(fconf, "r") as data:
            self.bk = ast.literal_eval(data.read())['bks'][chDiz]
            data.close()
        #self.bk = diz
        print(self.bk)
        self.set_default_size(800, 300)
        self.set_border_width(10)
        box = Gtk.Grid()
        self.nb = Gtk.Notebook()
        self.nb.set_property("width-request", 780)
        self.nb.set_property("height-request", 260)
        # self.add(self.nb)
        box.attach(self.nb, 0, 0, 1, 1)

        self.__prima_pagina()
        self.__seconda_pagina()
        self.__terzaPagina()
        # self.add(self.__attachButton())
        box.attach(self.__attach_button(), 0, 1, 1, 1)
        # label = Gtk.Label(label="This is a dialog to display additional information")

        # box = self.get_content_area()
        # box.add(label)
        self.add(box)
        self.show_all()

    # ************************** DESTINAZIONE ********************************
    def __terzaPagina(self):
        # seconda pagina
        pg2 = Gtk.Grid()
        pg2.set_border_width(5)
        pg2.set_property("width-request", 300)
        # pg2.set_property("height-request",150)
        larg1 = 90

        h = Gtk.Box(spacing=10)
        rdLocaleTO = Gtk.RadioButton.new_with_label_from_widget(None, "Locale")
        rdLocaleTO.set_property("width-request", larg1)
        rdLocaleTO.connect("toggled", self.on_rd_toggled_to, "loc")
        h.add(rdLocaleTO)

        self.txtLocPathTO = Gtk.Entry(text="", editable=False)
        self.txtLocPathTO.set_property("max-width-chars", 80)
        h.add(self.txtLocPathTO)

        self.btLocPathTO = Gtk.Button.new_with_mnemonic("----")
        self.btLocPathTO.set_property("width-request", 25)
        self.btLocPathTO.set_property("height-request", 15)
        self.btLocPathTO.connect("clicked", self.on_folder_clicked)
        h.add(self.btLocPathTO)
        pg2.attach(h, 0, 0, 1, 1)

        l = Gtk.HSeparator()
        l.set_property("height-request", 10)
        l.set_property("margin", 10)
        pg2.attach(l, 0, 1, 4, 1)

        h = Gtk.Box(spacing=10)
        self.rdRemotoTO = Gtk.RadioButton.new_with_label_from_widget(rdLocaleTO, "Remoto")
        self.rdRemotoTO.set_property("width-request", larg1)
        # rdRemoto.connect("toggled", self.on_rd_toggled, "2")
        h.add(self.rdRemotoTO)
        h.add(Gtk.Label(label="Host", width_request=50, xalign=1))
        self.txtHostTO = Gtk.Entry(text="")
        # pg2.attach(self.utente,2,1,1,1)
        h.add(self.txtHostTO)
        pg2.attach(h, 0, 2, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Utente", width_request=50, xalign=1))
        self.txtUtenteTO = Gtk.Entry(text="")
        h.add(self.txtUtenteTO)
        pg2.attach(h, 0, 3, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Path", width_request=50, xalign=1))
        self.txtRemPathTO = Gtk.Entry(text="", max_width_chars=80)
        h.add(self.txtRemPathTO)
        pg2.attach(h, 0, 4, 1, 1)

        self.nb.append_page(pg2, Gtk.Label(label="DESTINAZIONE"))

        self.__init_origine_to()

    def __init_origine_to(self):
        if self.bk['dirTO']['remotoTO'] :
            self.rdRemotoTO.set_active(True)
            i = self.bk['dirTO']['to'].find("@")
            if i != -1:
                self.txtUtenteTO.set_text(self.bk['dirTO']['to'][:i])
                ii = self.bk['dirTO']['to'].find(":")
                if ii != -1:
                    self.txtHostTO.set_text(self.bk['dirTO']['to'][i + 1:ii])
                    self.txtRemPathTO.set_text(self.bk['dirTO']['to'][ii + 1:])

    def on_rd_toggled_to(self, rd, name):
        if rd.get_active():
            self.btLocPathTO.set_sensitive(True)
            self.txtHostTO.set_editable(False)
            self.txtUtenteTO.set_editable(False)
            self.txtRemPathTO.set_editable(False)
        else:
            self.txtHostTO.set_editable(True)
            self.txtUtenteTO.set_editable(True)
            self.txtRemPathTO.set_editable(True)
            self.btLocPathTO.set_sensitive(False)

    # ************************** ORIGINE ********************************
    def __seconda_pagina(self):
        # seconda pagina
        pg2 = Gtk.Grid()
        pg2.set_border_width(5)
        pg2.set_property("width-request", 300)
        # pg2.set_property("height-request",150)
        larg1 = 90

        h = Gtk.Box(spacing=10)
        rdLocale = Gtk.RadioButton.new_with_label_from_widget(None, "Locale")
        rdLocale.set_property("width-request", larg1)
        rdLocale.connect("toggled", self.on_rd_toggled, "loc")
        h.pack_start(rdLocale, True, True, 0)
        # h.add(rdLocale)
        # pg2.attach(rdLocale,0,0,1,1)

        self.txtLocPath = Gtk.Entry(text="", editable=False)
        self.txtLocPath.set_property("max-width-chars", 80)
        h.pack_start(self.txtLocPath, True, True, 0)
        # h.add(locPath)
        # pg2.attach(locPath,1,0,2,1)
        self.btLocPath = Gtk.Button.new_with_mnemonic("---")
        self.btLocPath.set_property("width-request", 25)
        self.btLocPath.set_property("height-request", 15)
        self.btLocPath.connect("clicked", self.on_folder_clicked)
        h.pack_start(self.btLocPath, False, True, 0)
        # h.add(button)
        # pg2.attach(button,3,0,1,1)
        pg2.attach(h, 0, 0, 1, 1)

        l = Gtk.HSeparator()
        l.set_property("height-request", 10)
        l.set_property("margin", 10)
        pg2.attach(l, 0, 1, 4, 1)

        h = Gtk.Box(spacing=10)
        self.rdRemoto = Gtk.RadioButton.new_with_label_from_widget(rdLocale, "Remoto")
        self.rdRemoto.set_property("width-request", larg1)
        # rdRemoto.connect("toggled", self.on_rd_toggled, "2")
        h.add(self.rdRemoto)
        h.add(Gtk.Label(label="Host", width_request=50, xalign=1))
        self.txtHost = Gtk.Entry(text="")
        # pg2.attach(self.utente,2,1,1,1)
        h.add(self.txtHost)
        pg2.attach(h, 0, 2, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Utente", width_request=50, xalign=1))
        self.txtUtente = Gtk.Entry(text="")
        h.add(self.txtUtente)
        pg2.attach(h, 0, 3, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Path", width_request=50, xalign=1))
        self.txtRemPath = Gtk.Entry(text="", max_width_chars=80)
        # self.txtRemPath.set_property("max-width-chars", 35)
        h.add(self.txtRemPath)
        pg2.attach(h, 0, 4, 1, 1)

        self.nb.append_page(pg2, Gtk.Label(label="ORIGINE"))

        self.__init_origine()

    def __init_origine(self):
        if self.bk['dirDA']['remoto'] :
            self.rdRemoto.set_active(True)
            i = self.bk['dirDA']['da'].find("@")
            if i != -1:
                self.txtUtente.set_text(self.bk['dirDA']['da'][:i])
                ii = self.bk['dirDA']['da'].find(":")
                if ii != -1:
                    self.txtHost.set_text(self.bk['dirDA']['da'][i + 1:ii])
                    self.txtRemPath.set_text(self.bk['dirDA']['da'][ii + 1:])

    def on_rd_toggled(self, rd, name):
        if rd.get_active():
            self.btLocPath.set_sensitive(True)
            self.txtHost.set_editable(False)
            self.txtUtente.set_editable(False)
            self.txtRemPath.set_editable(False)
        else:
            self.btLocPath.set_sensitive(False)
            self.txtHost.set_editable(True)
            self.txtUtente.set_editable(True)
            self.txtRemPath.set_editable(True)

    # *************************** GENERALE *****************************
    def __prima_pagina(self):
        # prima pagina
        self.generale = Gtk.Grid()
        self.generale.set_border_width(10)
        self.generale.attach(Gtk.Label(label=self.bk['titolo']), 0, 0, 1, 1)
        self.nb.append_page(self.generale, Gtk.Label(label="GENERALE"))

    # ******************************************************************

    def __attach_button(self):
        hbox2 = Gtk.Box(spacing=6)
        button = Gtk.Button.new_with_mnemonic("Annulla")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_annulla_clicked)
        hbox2.add(button)

        button = Gtk.Button.new_with_mnemonic("Salva")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_salva_clicked)
        hbox2.add(button)
        return hbox2

    def on_folder_clicked(self, widget):
        #print(widget.get_label())
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(300, 200)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if widget.get_label()=="---":
                #print("Select clicked")
                #print("Folder selected: " + dialog.get_filename())
                self.txtLocPath.set_text(dialog.get_filename())
            elif widget.get_label()=="----":
                self.txtLocPathTO.set_text(dialog.get_filename())
        #elif response == Gtk.ResponseType.CANCEL:
        #    print("Cancel clicked")

        dialog.destroy()

    def on_annulla_clicked(self):
        printf("Annulla")

    def on_salva_clicked(self):
        print("salva")


def getImpostazioni(f):
    with open(f, "r") as data:
        d = ast.literal_eval(data.read())
        data.close()
        return d


#win = DlgConf(getImpostazioni("./danieleBK.conf")['chDef'])
#win = DlgConf("./danieleBK.conf","chDef")
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()
