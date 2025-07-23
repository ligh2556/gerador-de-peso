# Gui/barra_lateral.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from . import icons

class BarraLateral(QWidget):
    # Sinais para cada botão de navegação
    sinal_pagina_principal = pyqtSignal()
    sinal_constantes = pyqtSignal()
    sinal_configuracoes = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.largura_expandida = 60
        self.esta_expandida = True
        
        # --- Carrega todos os ícones necessários ---
        self.icon_menu = icons.create_menu_icon()
        self.icon_home = icons.create_home_icon()
        self.icon_constant = icons.create_settings_icon() # Reutilizando o ícone de engrenagem
        self.icon_settings = icons.create_settings_icon()
        
        # --- Layout Principal ---
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(5, 5, 5, 5)
        self.layout_principal.setSpacing(10)

        # Tamanho padrão para todos os ícones para manter a consistência
        icon_size = QSize(28, 28)

        # --- Botão de Toggle ---
        self.btn_toggle = QPushButton()
        self.btn_toggle.setIcon(self.icon_menu)
        self.btn_toggle.setIconSize(icon_size)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setChecked(True)
        self.btn_toggle.clicked.connect(self.toggle_barra)

        # --- Botões de Navegação ---
        self.btn_pagina_principal = QPushButton()
        self.btn_pagina_principal.setIcon(self.icon_home)
        self.btn_pagina_principal.setIconSize(icon_size)
        self.btn_pagina_principal.clicked.connect(self.sinal_pagina_principal.emit)
        
        self.btn_constantes = QPushButton()
        self.btn_constantes.setIcon(self.icon_constant)
        self.btn_constantes.setIconSize(icon_size)
        self.btn_constantes.clicked.connect(self.sinal_constantes.emit)
        
        self.btn_configuracoes = QPushButton()
        self.btn_configuracoes.setIcon(self.icon_settings)
        self.btn_configuracoes.setIconSize(icon_size)
        self.btn_configuracoes.clicked.connect(self.sinal_configuracoes.emit)
        
        # Lista de botões que serão ocultados/mostrados
        self.botoes_de_navegacao = [self.btn_pagina_principal, self.btn_constantes, self.btn_configuracoes]

        # --- Adiciona os widgets ao layout na ordem desejada ---
        self.layout_principal.addWidget(self.btn_toggle)
        self.layout_principal.addWidget(self.btn_pagina_principal)
        self.layout_principal.addWidget(self.btn_constantes)
        
        self.layout_principal.addStretch() # Espaço flexível que empurra o próximo widget para baixo
        
        self.layout_principal.addWidget(self.btn_configuracoes)
        
        # Define a largura fixa da barra lateral
        self.setFixedWidth(self.largura_expandida)

    def toggle_barra(self):
        """Mostra ou oculta os botões de navegação."""
        # Apenas os botões de navegação são afetados. O botão de Configurações
        # que está no final, também deve ser ocultado.
        should_be_visible = self.btn_toggle.isChecked()
        
        self.btn_pagina_principal.setVisible(should_be_visible)
        self.btn_constantes.setVisible(should_be_visible)
        self.btn_configuracoes.setVisible(should_be_visible)