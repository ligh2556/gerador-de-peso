# Gui/config_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

class ConfigPage(QWidget):
    # Aceita o dicionário de configurações no construtor
    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)
        self.settings = settings  # Armazena a referência ao dicionário compartilhado

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("Configurações de Valores")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        main_layout.addWidget(title_label)

        # Formulário
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Validador para aceitar apenas números com vírgula ou ponto
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        # Campos de entrada
        self.valor_18k_input = QLineEdit()
        self.valor_18k_input.setValidator(validator)
        
        self.valor_10k_input = QLineEdit()
        self.valor_10k_input.setValidator(validator)
        
        form_layout.addRow(QLabel("Valor do Ouro 18k (por grama):"), self.valor_18k_input)
        form_layout.addRow(QLabel("Valor do Ouro 10k (por grama):"), self.valor_10k_input)

        # Botão para salvar
        self.save_button = QPushButton("Salvar Valores")
        self.save_button.clicked.connect(self._save_settings)

        # Label para confirmação
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: green;")

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addStretch()
        
        self._load_settings() # Carrega os valores atuais ao iniciar a página

    def _load_settings(self):
        """Carrega os valores do dicionário e os exibe nos campos de entrada."""
        valor_18k = self.settings.get("valor_ouro_18k", 0.0)
        valor_10k = self.settings.get("valor_ouro_10k", 0.0)
        
        self.valor_18k_input.setText(f"{valor_18k:.2f}".replace('.', ','))
        self.valor_10k_input.setText(f"{valor_10k:.2f}".replace('.', ','))

    def _save_settings(self):
        """Salva os valores dos campos de entrada no dicionário compartilhado."""
        try:
            valor_18k = float(self.valor_18k_input.text().replace(',', '.'))
            valor_10k = float(self.valor_10k_input.text().replace(',', '.'))

            # Atualiza o dicionário
            self.settings["valor_ouro_18k"] = valor_18k
            self.settings["valor_ouro_10k"] = valor_10k

            self.status_label.setText("Valores salvos com sucesso!")
        except ValueError:
            self.status_label.setText("Erro: Insira valores numéricos válidos.")
            self.status_label.setStyleSheet("color: red;")