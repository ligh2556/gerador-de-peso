# main.py
import sys
from PyQt6.QtWidgets import QApplication
from Gui.master_gui import MasterGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # --- Carregar a folha de estilo ---
    # Lembre-se que agora o main.py está um nível acima da pasta Gui
    try:
        with open("Gui/estilo.qss", "r", encoding="utf-8") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Aviso: Arquivo 'Gui/estilo.qss' não encontrado. Usando estilo padrão.")
        
    # --- Instanciar e mostrar a janela principal ---
    janela_principal = MasterGui()
    janela_principal.show()
    
    sys.exit(app.exec())