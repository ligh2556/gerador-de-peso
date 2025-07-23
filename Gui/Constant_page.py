# Gui/Constant_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from Core.calculo import calcular_massa_alianca, get_diametro_por_tamanho, TABELA_TAMANHO_ARO_MM

class ConstantPage(QWidget):
    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)
        self.settings = settings

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Calcular e Salvar Constante de Perfil")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        main_layout.addWidget(title_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.profile_name_input = QLineEdit()
        self.profile_name_input.setPlaceholderText("Ex: Reta por fora, anatômica por dentro")
        
        self.largura_combo = QComboBox()
        self.largura_combo.addItems(["2", "3", "4", "5", "6", "7"])
        
        self.tamanho_anel_input = QComboBox()
        for tamanho in sorted(TABELA_TAMANHO_ARO_MM.keys()):
            self.tamanho_anel_input.addItem(str(tamanho))

        self.validator = QDoubleValidator()
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        
        # --- CORREÇÃO APLICADA AQUI ---
        self.espessura_input = QLineEdit()
        self.espessura_input.setValidator(self.validator)
        
        self.peso_pratico_input = QLineEdit()
        self.peso_pratico_input.setValidator(self.validator)
        self.peso_pratico_input.setPlaceholderText("Massa real medida na balança")

        self.tipo_ouro_combo = QComboBox()
        self.tipo_ouro_combo.addItems(["Ouro 18k", "Ouro 10k"])
        self.densidades = {"Ouro 18k": 15.4, "Ouro 10k": 12.2}

        form_layout.addRow(QLabel("Nome do Perfil:"), self.profile_name_input)
        form_layout.addRow(QLabel("Largura (mm):"), self.largura_combo)
        form_layout.addRow(QLabel("Tamanho do Anel:"), self.tamanho_anel_input)
        form_layout.addRow(QLabel("Espessura (mm):"), self.espessura_input)
        form_layout.addRow(QLabel("Material:"), self.tipo_ouro_combo)
        form_layout.addRow(QLabel("Peso Prático (g):"), self.peso_pratico_input)
        
        main_layout.addLayout(form_layout)

        self.save_button = QPushButton("Calcular e Salvar Constante")
        self.save_button.clicked.connect(self._calculate_and_save)
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")

        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.result_label)
        main_layout.addStretch()

    def _calculate_and_save(self):
        # (Lógica de cálculo permanece a mesma)
        try:
            profile_name = self.profile_name_input.text().strip()
            if not profile_name:
                raise ValueError("O nome do perfil não pode ser vazio.")
            largura_mm = float(self.largura_combo.currentText())
            tamanho = int(self.tamanho_anel_input.currentText())
            diametro_mm = get_diametro_por_tamanho(tamanho)
            espessura_mm = float(self.espessura_input.text().replace(',', '.'))
            peso_pratico = float(self.peso_pratico_input.text().replace(',', '.'))
            selecao_ouro = self.tipo_ouro_combo.currentText()
            densidade = self.densidades[selecao_ouro]
            peso_teorico = calcular_massa_alianca(
                diametro_interno_cm=(diametro_mm / 10),
                espessura_cm=(espessura_mm / 10),
                largura_cm=(largura_mm / 10),
                densidade=densidade
            )
            if peso_teorico == 0: raise ValueError("Peso teórico não pode ser zero.")
            constante = (peso_pratico / peso_teorico) - 1.0
            self.settings["perfis"][profile_name] = constante
            self.result_label.setStyleSheet("color: green;")
            self.result_label.setText(f"Perfil '{profile_name}' salvo com constante de {constante:+.2%}.")
        except (ValueError, TypeError) as e:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText(f"Erro: Verifique os valores. ({e})")