# Gui/main_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QComboBox, 
                             QCheckBox, QRadioButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from Core.calculo import (calcular_massa_alianca, calcular_espessura_alianca, 
                          get_diametro_por_tamanho, TABELA_TAMANHO_ARO_MM)

class MainPage(QWidget):
    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)
        self.settings = settings
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Calculadora de Alianças")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        
        self.inverter_checkbox = QCheckBox("Inverter Cálculo (descobrir a espessura)")
        self.inverter_checkbox.toggled.connect(self._update_ui_mode)

        main_layout.addWidget(title_label)
        main_layout.addWidget(self.inverter_checkbox)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.validator = QDoubleValidator()
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        largura_layout = QHBoxLayout()
        self.largura_combo = QComboBox()
        self.largura_combo.addItems(["2", "3", "4", "5", "6", "7", "Personalizado"])
        self.largura_combo.currentTextChanged.connect(self._on_largura_changed)
        self.largura_personalizada_input = QLineEdit()
        self.largura_personalizada_input.setPlaceholderText("Largura (mm)")
        self.largura_personalizada_input.setValidator(self.validator)
        self.largura_personalizada_input.setVisible(False)
        largura_layout.addWidget(self.largura_combo)
        largura_layout.addWidget(self.largura_personalizada_input)

        self.tamanho_anel_input = QComboBox()
        for tamanho in sorted(TABELA_TAMANHO_ARO_MM.keys()):
            self.tamanho_anel_input.addItem(str(tamanho))

        self.espessura_input = QLineEdit()
        self.espessura_input.setPlaceholderText("Grossura da parede (mm)")
        self.espessura_input.setValidator(self.validator)
        
        self.tipo_ouro_combo = QComboBox()
        self.tipo_ouro_combo.addItems(["Ouro 18k", "Ouro 10k"])
        self.densidades = {"Ouro 18k": 15.4, "Ouro 10k": 12.2}
        
        self.perfil_combo = QComboBox()

        self.form_layout.addRow(QLabel("Largura (mm):"), largura_layout)
        self.form_layout.addRow(QLabel("Tamanho do Anel:"), self.tamanho_anel_input)
        self.espessura_label = QLabel("Espessura (mm):")
        self.form_layout.addRow(self.espessura_label, self.espessura_input)
        self.form_layout.addRow(QLabel("Material:"), self.tipo_ouro_combo)
        self.form_layout.addRow(QLabel("Perfil da Aliança:"), self.perfil_combo)

        self.inverse_choice_container = QWidget()
        inverse_choice_layout = QHBoxLayout(self.inverse_choice_container)
        inverse_choice_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_por_peso = QRadioButton("Por Peso")
        self.radio_por_valor = QRadioButton("Por Valor")
        self.radio_por_peso.setChecked(True)
        self.radio_por_peso.toggled.connect(self._update_inverse_input_mode)
        inverse_choice_layout.addWidget(self.radio_por_peso)
        inverse_choice_layout.addWidget(self.radio_por_valor)
        self.inverse_choice_label = QLabel("Calcular por:")
        self.form_layout.addRow(self.inverse_choice_label, self.inverse_choice_container)
        
        # --- CORREÇÃO APLICADA AQUI ---
        self.massa_alvo_input = QLineEdit()
        self.massa_alvo_input.setValidator(self.validator)
        self.massa_alvo_input.setPlaceholderText("Peso desejado em gramas")
        self.massa_alvo_label = QLabel("Peso Desejado (g):")
        self.form_layout.addRow(self.massa_alvo_label, self.massa_alvo_input)
        
        self.valor_alvo_input = QLineEdit()
        self.valor_alvo_input.setValidator(self.validator)
        self.valor_alvo_input.setPlaceholderText("Valor a gastar em R$")
        self.valor_alvo_label = QLabel("Valor a Gastar (R$):")
        self.form_layout.addRow(self.valor_alvo_label, self.valor_alvo_input)
        
        main_layout.addLayout(self.form_layout)

        self.calculate_button = QPushButton("Calcular Peso e Valor")
        self.calculate_button.setStyleSheet("font-size: 14px; padding: 8px; margin-top: 10px;")
        self.calculate_button.clicked.connect(self._on_calculate_click)
        main_layout.addWidget(self.calculate_button)

        line = QFrame(); line.setFrameShape(QFrame.Shape.HLine); line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        results_layout = QHBoxLayout()
        massa_layout = QVBoxLayout()
        self.resultado_massa_label = QLabel("Peso (Massa):")
        self.resultado_massa_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.resultado_massa_valor = QLabel("0.00 gramas")
        self.resultado_massa_valor.setStyleSheet("font-size: 22px; color: #DAA520; font-weight: bold;")
        massa_layout.addWidget(self.resultado_massa_label, alignment=Qt.AlignmentFlag.AlignCenter)
        massa_layout.addWidget(self.resultado_massa_valor, alignment=Qt.AlignmentFlag.AlignCenter)
        valor_layout = QVBoxLayout()
        self.resultado_valor_label = QLabel("Valor Estimado:")
        self.resultado_valor_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.resultado_valor_valor = QLabel("R$ 0,00")
        self.resultado_valor_valor.setStyleSheet("font-size: 22px; color: #DAA520; font-weight: bold;")
        valor_layout.addWidget(self.resultado_valor_label, alignment=Qt.AlignmentFlag.AlignCenter)
        valor_layout.addWidget(self.resultado_valor_valor, alignment=Qt.AlignmentFlag.AlignCenter)
        results_layout.addLayout(massa_layout)
        results_layout.addLayout(valor_layout)
        main_layout.addLayout(results_layout)
        main_layout.addStretch()

        self._update_ui_mode()

    def showEvent(self, event):
        self._populate_profiles()
        super().showEvent(event)

    def _populate_profiles(self):
        current_selection = self.perfil_combo.currentText()
        self.perfil_combo.clear()
        perfis = self.settings.get("perfis", {"Padrão (Teórico)": 0.0})
        for profile_name in perfis.keys():
            self.perfil_combo.addItem(profile_name)
        index = self.perfil_combo.findText(current_selection)
        if index != -1: self.perfil_combo.setCurrentIndex(index)

    def _on_largura_changed(self, texto_selecionado: str):
        self.largura_personalizada_input.setVisible(texto_selecionado == "Personalizado")

    def _update_ui_mode(self):
        is_inverso = self.inverter_checkbox.isChecked()
        self.espessura_label.setVisible(not is_inverso)
        self.espessura_input.setVisible(not is_inverso)
        self.inverse_choice_label.setVisible(is_inverso)
        self.inverse_choice_container.setVisible(is_inverso)
        if is_inverso:
            self.calculate_button.setText("Calcular Espessura Necessária")
            self._update_inverse_input_mode()
        else:
            self.calculate_button.setText("Calcular Peso e Valor")
            self.massa_alvo_label.setVisible(False); self.massa_alvo_input.setVisible(False)
            self.valor_alvo_label.setVisible(False); self.valor_alvo_input.setVisible(False)
    
    def _update_inverse_input_mode(self):
        is_por_peso = self.radio_por_peso.isChecked()
        self.massa_alvo_label.setVisible(is_por_peso)
        self.massa_alvo_input.setVisible(is_por_peso)
        self.valor_alvo_label.setVisible(not is_por_peso)
        self.valor_alvo_input.setVisible(not is_por_peso)

    def _on_calculate_click(self):
        # (Lógica de cálculo permanece a mesma)
        try:
            selecao_largura = self.largura_combo.currentText()
            largura_mm = float(self.largura_personalizada_input.text().replace(',', '.')) if selecao_largura == "Personalizado" else float(selecao_largura)
            tamanho_selecionado = int(self.tamanho_anel_input.currentText())
            diametro_mm = get_diametro_por_tamanho(tamanho_selecionado)
            if diametro_mm is None: raise ValueError("Tamanho inválido.")
            selecao_ouro = self.tipo_ouro_combo.currentText()
            densidade = self.densidades[selecao_ouro]
            valor_grama = self.settings.get("valor_ouro_18k", 0) if selecao_ouro == "Ouro 18k" else self.settings.get("valor_ouro_10k", 0)
            if self.inverter_checkbox.isChecked():
                massa_desejada = 0.0
                if self.radio_por_peso.isChecked():
                    massa_desejada = float(self.massa_alvo_input.text().replace(',', '.'))
                elif self.radio_por_valor.isChecked():
                    valor_alvo = float(self.valor_alvo_input.text().replace(',', '.'))
                    if valor_grama <= 0: raise ValueError("Valor por grama (R$) deve ser > 0. Defina nas Configurações.")
                    massa_desejada = valor_alvo / valor_grama
                if massa_desejada <= 0: raise ValueError("Peso/Valor alvo deve ser > 0.")
                espessura_calculada_cm = calcular_espessura_alianca(
                    diametro_interno_cm=(diametro_mm / 10), largura_cm=(largura_mm / 10),
                    densidade=densidade, massa_desejada_g=massa_desejada
                )
                self.espessura_input.setText(f"{espessura_calculada_cm * 10:.2f}")
                valor_final = massa_desejada * valor_grama
                self.resultado_massa_valor.setText(f"{massa_desejada:.2f} gramas")
                self.resultado_valor_valor.setText(f"R$ {valor_final:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            else:
                espessura_mm = float(self.espessura_input.text().replace(',', '.'))
                massa_teorica = calcular_massa_alianca(
                    diametro_interno_cm=(diametro_mm / 10), espessura_cm=(espessura_mm / 10),
                    largura_cm=(largura_mm / 10), densidade=densidade
                )
                profile_name = self.perfil_combo.currentText()
                constante = self.settings["perfis"].get(profile_name, 0.0)
                massa_final_ajustada = massa_teorica * (1 + constante)
                valor_total = massa_final_ajustada * valor_grama
                self.resultado_massa_valor.setText(f"{massa_final_ajustada:.2f} gramas")
                self.resultado_valor_valor.setText(f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        except (ValueError, TypeError):
            self.resultado_massa_valor.setText("Erro!")
            self.resultado_valor_valor.setText("Verifique os valores.")
        except Exception as e:
            self.resultado_massa_valor.setText("Erro!")
            self.resultado_valor_valor.setText(f"{e}")