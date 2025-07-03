import tkinter as tk
from tkinter import ttk

# Importar todos los módulos de las pestañas
from detalles_tab_ui import DetallesTab
from documentos_tab_ui import DocumentosTab
from tareas_ui import TareasTab
from partes_ui import PartesTab
from seguimiento_ui import SeguimientoTab

class CaseDetailWindow(tk.Toplevel):
    def __init__(self, parent, app_controller, case_id):
        super().__init__(parent)
        self.app_controller = app_controller
        self.case_id = case_id
        
        self.case_data = self.app_controller.db_crm.get_case_by_id(self.case_id)
        if not self.case_data:
            self.destroy()
            return
            
        self.title(f"Detalles del Caso: {self.case_data.get('caratula', 'N/A')}")
        
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        # 1. TAMAÑO DE LA VENTANA AJUSTADO (MÁS PEQUEÑO)
        self.geometry("850x600") 
        self.minsize(650, 450)
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- Crear e instanciar cada pestaña ---
        
        # Pestaña 0: Detalles
        self.detalles_tab = DetallesTab(self.notebook, self.app_controller)
        self.notebook.add(self.detalles_tab, text="Detalles del Caso")
        self.detalles_tab.load_details(self.case_data)

        # Pestaña 1: Documentación
        self.documentos_tab = DocumentosTab(self.notebook, self.app_controller, self.case_data)
        self.notebook.add(self.documentos_tab, text="Documentación")

        # Pestaña 2: Tareas/Plazos
        self.tareas_tab = TareasTab(self.notebook, self.app_controller)
        self.notebook.add(self.tareas_tab, text="Tareas/Plazos")
        self.tareas_tab.load_tareas(self.case_id)
        self.tareas_tab.set_add_button_state()

        # Pestaña 3: Partes
        self.partes_tab = PartesTab(self.notebook, self.app_controller)
        self.notebook.add(self.partes_tab, text="Partes")
        self.partes_tab.load_partes(self.case_id)
        self.partes_tab.set_add_button_state(None)

        # Pestaña 4: Seguimiento
        self.seguimiento_tab = SeguimientoTab(self.notebook, self.app_controller)
        self.notebook.add(self.seguimiento_tab, text="Seguimiento")
        self.seguimiento_tab.load_actividades(self.case_id)
        self.seguimiento_tab.set_add_button_state(None)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    # 2. NUEVO MÉTODO PARA SELECCIONAR UNA PESTAÑA
    def select_tab(self, tab_index):
        """Selecciona una pestaña del notebook por su índice."""
        try:
            self.notebook.select(tab_index)
        except tk.TclError:
            print(f"Error: No se pudo seleccionar la pestaña con índice {tab_index}")
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    def on_close(self):
        self.app_controller.on_case_window_close(self.case_id)
        self.destroy()