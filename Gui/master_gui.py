# Gui/master_gui.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from .barra_lateral import BarraLateral
from .main_page import MainPage
from .config_page import ConfigPage
from .Constant_page import ConstantPage # <-- MUDANÇA: Importar a nova página

class MasterGui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculadora de Alianças")
        self.setGeometry(100, 100, 1024, 600)

        # MUDANÇA: Adicionado "perfis" ao dicionário de configurações
        self.configuracoes_app = {
            "valor_ouro_18k": 350.00,
            "valor_ouro_10k": 220.00,
            "perfis": {
                "Padrão (Teórico)": 0.0, # Perfil padrão com 0% de diferença
            }
        }

        self.widget_central = QWidget()
        self.layout_principal = QHBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        self.barra_lateral = BarraLateral()
        
        self.paginas = QStackedWidget()
        self.main_page = MainPage(settings=self.configuracoes_app)
        self.config_page = ConfigPage(settings=self.configuracoes_app)
        self.constant_page = ConstantPage(settings=self.configuracoes_app) # <-- MUDANÇA: Instanciar a nova página
        
        self.paginas.addWidget(self.main_page)
        self.paginas.addWidget(self.config_page)
        self.paginas.addWidget(self.constant_page) # <-- MUDANÇA: Adicionar a página ao Stack

        self.layout_principal.addWidget(self.barra_lateral)
        self.layout_principal.addWidget(self.paginas)
        
        self.setCentralWidget(self.widget_central)
        
        # Conexões dos sinais
        self.barra_lateral.sinal_pagina_principal.connect(self.mostrar_pagina_principal)
        self.barra_lateral.sinal_configuracoes.connect(self.mostrar_pagina_configuracoes)
        self.barra_lateral.sinal_constantes.connect(self.mostrar_pagina_constantes) # <-- MUDANÇA: Conectar o novo sinal

    def mostrar_pagina_principal(self):
        self.paginas.setCurrentWidget(self.main_page)

    def mostrar_pagina_configuracoes(self):
        self.paginas.setCurrentWidget(self.config_page)

    # <-- MUDANÇA: Nova função para mostrar a página de constantes
    def mostrar_pagina_constantes(self):
        self.paginas.setCurrentWidget(self.constant_page)