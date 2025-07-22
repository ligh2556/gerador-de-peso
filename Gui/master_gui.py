# Gui/master_gui.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from .barra_lateral import BarraLateral
from .main_page import MainPage
from .config_page import ConfigPage

class MasterGui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculadora de Alianças")
        self.setGeometry(100, 100, 1024, 600)

        # --- MUDANÇA 1: Criar um dicionário para compartilhar os dados ---
        # Estes valores serão alterados na página de configuração e lidos na página principal.
        self.configuracoes_app = {
            "valor_ouro_18k": 350.00,  # Valor inicial de exemplo
            "valor_ouro_10k": 220.00   # Valor inicial de exemplo
        }

        self.widget_central = QWidget()
        self.layout_principal = QHBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        self.barra_lateral = BarraLateral()
        
        self.paginas = QStackedWidget()
        # --- MUDANÇA 2: Passar o dicionário de configurações para as páginas ---
        self.main_page = MainPage(settings=self.configuracoes_app)
        self.config_page = ConfigPage(settings=self.configuracoes_app)
        
        self.paginas.addWidget(self.main_page)
        self.paginas.addWidget(self.config_page)

        self.layout_principal.addWidget(self.barra_lateral)
        self.layout_principal.addWidget(self.paginas)
        
        self.setCentralWidget(self.widget_central)
        
        self.barra_lateral.sinal_pagina_principal.connect(self.mostrar_pagina_principal)
        self.barra_lateral.sinal_configuracoes.connect(self.mostrar_pagina_configuracoes)

    def mostrar_pagina_principal(self):
        self.paginas.setCurrentWidget(self.main_page)

    def mostrar_pagina_configuracoes(self):
        self.paginas.setCurrentWidget(self.config_page)