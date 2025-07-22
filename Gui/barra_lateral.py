# Gui/barra_lateral.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from . import icons

class BarraLateral(QWidget):
    sinal_pagina_principal = pyqtSignal()
    sinal_configuracoes = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.largura_expandida = 60
        self.esta_expandida = True
        
        self.icon_menu = icons.create_menu_icon()
        self.icon_home = icons.create_home_icon()
        self.icon_settings = icons.create_settings_icon()
        
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(5, 5, 5, 5)
        self.layout_principal.setSpacing(10)
        # MUDANÇA 1: Removido o alinhamento no topo para permitir que o layout ocupe todo o espaço vertical.
        # self.layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop) # <-- LINHA REMOVIDA

        icon_size = QSize(28, 28)

        self.btn_toggle = QPushButton()
        self.btn_toggle.setIcon(self.icon_menu)
        self.btn_toggle.setIconSize(icon_size)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setChecked(True)
        self.btn_toggle.clicked.connect(self.toggle_barra)

        self.btn_pagina_principal = QPushButton()
        self.btn_pagina_principal.setIcon(self.icon_home)
        self.btn_pagina_principal.setIconSize(icon_size)
        self.btn_pagina_principal.clicked.connect(self.sinal_pagina_principal.emit)
        
        self.btn_configuracoes = QPushButton()
        self.btn_configuracoes.setIcon(self.icon_settings)
        self.btn_configuracoes.setIconSize(icon_size)
        self.btn_configuracoes.clicked.connect(self.sinal_configuracoes.emit)
        
        self.botoes_de_navegacao = [self.btn_pagina_principal, self.btn_configuracoes]

        # --- MUDANÇA 2: Alterada a ordem de adição dos widgets ---
        self.layout_principal.addWidget(self.btn_toggle)
        self.layout_principal.addWidget(self.btn_pagina_principal)
        
        # Adiciona um espaço flexível que empurra tudo abaixo dele para o fundo
        self.layout_principal.addStretch() 
        
        self.layout_principal.addWidget(self.btn_configuracoes)
        # -------------------------------------------------------------
        
        self.setFixedWidth(self.largura_expandida)

    def toggle_barra(self):
        if self.btn_toggle.isChecked():
            self.esta_expandida = True
            for botao in self.botoes_de_navegacao:
                botao.setVisible(True)
        else:
            self.esta_expandida = False
            for botao in self.botoes_de_navegacao:
                botao.setVisible(False)