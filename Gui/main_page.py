# Gui/main_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QComboBox, 
                             QCheckBox, QRadioButton, QGridLayout, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from Core.calculo import (calcular_massa_alianca, calcular_espessura_alianca, 
                          calcular_espessura_par, get_diametro_por_tamanho, 
                          TABELA_TAMANHO_ARO_MM)

class MainPage(QWidget):
    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)
        self.settings = settings
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Calculadora de Alianças")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        
        options_layout = QHBoxLayout()
        self.inverter_checkbox = QCheckBox("Inverter Cálculo")
        self.par_checkbox = QCheckBox("Calcular Par")
        self.avancado_checkbox = QCheckBox("Modo Avançado")
        self.modelos_diferentes_checkbox = QCheckBox("Modelos Diferentes")
        
        options_layout.addWidget(self.inverter_checkbox)
        options_layout.addWidget(self.par_checkbox)
        options_layout.addWidget(self.avancado_checkbox)
        options_layout.addWidget(self.modelos_diferentes_checkbox)
        options_layout.addStretch()

        main_layout.addWidget(title_label)
        main_layout.addLayout(options_layout)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.validator = QDoubleValidator()
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        
        # Parâmetros Anel 1 (ou único/compartilhado)
        (self.largura_layout_1, self.largura_combo_1, 
         self.largura_personalizada_input_1) = self._criar_layout_largura(self.validator)
        self.espessura_input_1 = QLineEdit()
        self.espessura_input_1.setValidator(self.validator)
        self.espessura_input_1.setPlaceholderText("mm")
        self.perfil_combo_1 = QComboBox()
        
        # Parâmetros Anel 2 (para modo "Modelos Diferentes")
        (self.largura_layout_2, self.largura_combo_2, 
         self.largura_personalizada_input_2) = self._criar_layout_largura(self.validator)
        self.espessura_input_2 = QLineEdit()
        self.espessura_input_2.setValidator(self.validator)
        self.espessura_input_2.setPlaceholderText("mm")
        self.perfil_combo_2 = QComboBox()
        
        self.tamanho_layout = QHBoxLayout()
        self.tamanho_anel_input_1 = self._criar_combo_tamanho()
        self.tamanho_anel_input_2 = self._criar_combo_tamanho()
        self.tamanho_layout.addWidget(self.tamanho_anel_input_1)
        self.tamanho_layout.addWidget(self.tamanho_anel_input_2)

        self.tipo_ouro_combo = QComboBox()
        self.tipo_ouro_combo.addItems(["Ouro 18k", "Ouro 10k"])
        self.densidades = {"Ouro 18k": 15.4, "Ouro 10k": 12.2}
        
        self.form_layout.addRow(QLabel("Material (Ouro):"), self.tipo_ouro_combo)
        self.form_layout.addRow(QLabel("Largura (mm):"), self.largura_layout_1)
        self.largura_label_2 = QLabel("Largura Anel 2 (mm):")
        self.form_layout.addRow(self.largura_label_2, self.largura_layout_2)
        self.tamanho_label = QLabel("Tamanho do Anel:")
        self.form_layout.addRow(self.tamanho_label, self.tamanho_layout)
        self.espessura_label_1 = QLabel("Espessura (mm):")
        self.form_layout.addRow(self.espessura_label_1, self.espessura_input_1)
        self.espessura_label_2 = QLabel("Espessura Anel 2 (mm):")
        self.form_layout.addRow(self.espessura_label_2, self.espessura_input_2)
        self.perfil_label_1 = QLabel("Perfil da Aliança:")
        self.form_layout.addRow(self.perfil_label_1, self.perfil_combo_1)
        self.perfil_label_2 = QLabel("Perfil Anel 2:")
        self.form_layout.addRow(self.perfil_label_2, self.perfil_combo_2)

        self.inverse_section = self._criar_secao_inversa()
        
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.inverse_section)
        
        self.calculate_button = QPushButton("Calcular")
        self.calculate_button.setStyleSheet("font-size: 14px; padding: 8px; margin-top: 10px;")
        main_layout.addWidget(self.calculate_button)

        line = QFrame(); line.setFrameShape(QFrame.Shape.HLine); line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        
        results_grid = QGridLayout()
        self.painel_1 = self._criar_painel_resultado("Peso (Massa):", "0.00 g")
        self.painel_2 = self._criar_painel_resultado("Valor Estimado:", "R$ 0,00")
        self.painel_3 = self._criar_painel_resultado("Peso Médio:", "0.00 g")
        self.painel_4 = self._criar_painel_resultado("Pesos (1/2):", "0.00 g / 0.00 g")
        results_grid.addWidget(self.painel_1, 0, 0); results_grid.addWidget(self.painel_2, 0, 1)
        results_grid.addWidget(self.painel_3, 1, 0); results_grid.addWidget(self.painel_4, 1, 1)
        main_layout.addLayout(results_grid)
        main_layout.addStretch()

        self.calculate_button.clicked.connect(self._on_calculate_click)
        for checkbox in [self.par_checkbox, self.modelos_diferentes_checkbox, self.inverter_checkbox, self.avancado_checkbox]:
            checkbox.toggled.connect(self._update_ui_visibility)

        self._update_ui_visibility()

    def _criar_layout_largura(self, validator):
        container = QWidget(); hbox = QHBoxLayout(container); hbox.setContentsMargins(0,0,0,0)
        combo = QComboBox(); combo.addItems(["2", "3", "4", "5", "6", "7", "Personalizado"])
        line_edit = QLineEdit(); line_edit.setValidator(validator); line_edit.setPlaceholderText("mm")
        line_edit.setVisible(False)
        combo.currentTextChanged.connect(lambda text, le=line_edit: le.setVisible(text == "Personalizado"))
        hbox.addWidget(combo); hbox.addWidget(line_edit)
        return container, combo, line_edit

    def _criar_combo_tamanho(self):
        combo = QComboBox(); combo.addItems(map(str, sorted(TABELA_TAMANHO_ARO_MM.keys())))
        return combo

    def _criar_secao_inversa(self):
        container = QWidget()
        self.inverse_form_layout = QFormLayout(container) # Armazena como atributo de instância
        self.inverse_form_layout.setContentsMargins(0,10,0,0); self.inverse_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        inverse_choice_container = QWidget()
        inverse_choice_layout = QHBoxLayout(inverse_choice_container); inverse_choice_layout.setContentsMargins(0,0,0,0)
        self.radio_por_peso = QRadioButton("Por Peso"); self.radio_por_valor = QRadioButton("Por Valor")
        self.radio_por_peso.setChecked(True)
        self.radio_por_peso.toggled.connect(self._update_ui_visibility)
        self.radio_por_valor.toggled.connect(self._update_ui_visibility)
        inverse_choice_layout.addWidget(self.radio_por_peso); inverse_choice_layout.addWidget(self.radio_por_valor)
        self.inverse_form_layout.addRow(QLabel("Calcular por:"), inverse_choice_container)
        
        validator = QDoubleValidator(); validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.massa_alvo_input = QLineEdit(); self.massa_alvo_input.setValidator(validator)
        self.massa_alvo_input.setPlaceholderText("Peso desejado (g)")
        self.massa_alvo_label = QLabel("Peso Desejado (g):")
        self.inverse_form_layout.addRow(self.massa_alvo_label, self.massa_alvo_input)
        
        self.valor_alvo_input = QLineEdit(); self.valor_alvo_input.setValidator(validator)
        self.valor_alvo_input.setPlaceholderText("Valor a gastar em R$")
        self.valor_alvo_label = QLabel("Valor a Gastar (R$):")
        self.inverse_form_layout.addRow(self.valor_alvo_label, self.valor_alvo_input)
        return container
        
    def _criar_painel_resultado(self, texto_label, texto_valor):
        container = QWidget()
        layout = QVBoxLayout(container)
        label = QLabel(texto_label); label.setObjectName("resultado_label")
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        valor = QLabel(texto_valor); valor.setObjectName("resultado_valor")
        valor.setStyleSheet("font-size: 22px; color: #DAA520; font-weight: bold;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(valor, alignment=Qt.AlignmentFlag.AlignCenter)
        return container

    def showEvent(self, event):
        self._populate_profiles(); super().showEvent(event)

    def _populate_profiles(self):
        for combo in [self.perfil_combo_1, self.perfil_combo_2]:
            current = combo.currentText()
            combo.clear()
            perfis = self.settings.get("perfis", {})
            combo.addItems(perfis.keys())
            index = combo.findText(current)
            if index != -1: combo.setCurrentIndex(index)

    def _update_ui_visibility(self):
        is_par = self.par_checkbox.isChecked()
        is_inverso = self.inverter_checkbox.isChecked()
        is_diferente = self.modelos_diferentes_checkbox.isChecked() and is_par and not is_inverso
        is_avancado = self.avancado_checkbox.isChecked()

        self.avancado_checkbox.setEnabled(is_par and not is_inverso)
        self.modelos_diferentes_checkbox.setEnabled(is_par and not is_inverso)
        if is_inverso or not is_par:
            if self.avancado_checkbox.isChecked(): self.avancado_checkbox.setChecked(False)
            if self.modelos_diferentes_checkbox.isChecked(): self.modelos_diferentes_checkbox.setChecked(False)

        self.tamanho_anel_input_2.setVisible(is_par)
        self.form_layout.setRowVisible(self.largura_label_2, is_diferente)
        self.form_layout.setRowVisible(self.espessura_label_2, is_diferente)
        self.form_layout.setRowVisible(self.perfil_label_2, is_diferente)
        
        self.form_layout.setRowVisible(self.espessura_label_1, not is_inverso)
        self.inverse_section.setVisible(is_inverso)
        self.espessura_input_1.setReadOnly(is_inverso)
        if is_inverso: self.espessura_input_1.setText("")
        
        is_por_peso = self.radio_por_peso.isChecked() and is_inverso
        # --- CORREÇÃO APLICADA AQUI ---
        self.inverse_form_layout.setRowVisible(self.massa_alvo_label, is_por_peso)
        self.inverse_form_layout.setRowVisible(self.valor_alvo_label, not is_por_peso)
        
        self.painel_3.setVisible(is_par and is_avancado and not is_inverso)
        self.painel_4.setVisible(is_par and is_avancado and not is_inverso)
        self.painel_2.setVisible(True)
        
        label1, label2, label3, label4 = "", "", "", ""
        if is_inverso:
            self.calculate_button.setText("Calcular Espessura")
            label1 = "Espessura (mm):"
            if is_par: 
                label2 = "Pesos (Anel 1 / 2):"
            else:
                self.painel_2.setVisible(False)
        else:
            self.calculate_button.setText("Calcular Peso e Valor")
            if is_par:
                if is_avancado:
                    label1, label2 = "Peso Total:", "Valor Total:"
                    label3, label4 = "Peso Médio:", "Pesos (1 / 2):"
                else: 
                    label1, label2 = "Peso Total:", "Valor Total:"
            else:
                label1, label2 = "Peso (Massa):", "Valor Estimado:"
        
        self.painel_1.findChild(QLabel, "resultado_label").setText(label1)
        self.painel_2.findChild(QLabel, "resultado_label").setText(label2)
        self.painel_3.findChild(QLabel, "resultado_label").setText(label3)
        self.painel_4.findChild(QLabel, "resultado_label").setText(label4)

    def _get_largura_mm(self, combo, line_edit):
        selecao = combo.currentText()
        if not selecao: raise ValueError("Largura não selecionada.")
        return float(line_edit.text().replace(',', '.')) if selecao == "Personalizado" else float(selecao)
    
    def _get_anel_params(self, num_anel):
        params = {}
        if num_anel == 1:
            params["largura_mm"] = self._get_largura_mm(self.largura_combo_1, self.largura_personalizada_input_1)
            tamanho_combo = self.tamanho_anel_input_1
            params["espessura_mm"] = float(self.espessura_input_1.text().replace(',', '.'))
            params["constante"] = self.settings["perfis"].get(self.perfil_combo_1.currentText(), 0.0)
        else:
            params["largura_mm"] = self._get_largura_mm(self.largura_combo_2, self.largura_personalizada_input_2)
            tamanho_combo = self.tamanho_anel_input_2
            params["espessura_mm"] = float(self.espessura_input_2.text().replace(',', '.'))
            params["constante"] = self.settings["perfis"].get(self.perfil_combo_2.currentText(), 0.0)
        
        tamanho = int(tamanho_combo.currentText())
        params["diametro_mm"] = get_diametro_por_tamanho(tamanho)
        if params["diametro_mm"] is None: raise ValueError(f"Tamanho do anel {num_anel} inválido.")
        return params

    def _on_calculate_click(self):
        for panel in [self.painel_1, self.painel_2, self.painel_3, self.painel_4]:
            panel.findChild(QLabel, "resultado_valor").setText("...")
            
        try:
            is_par = self.par_checkbox.isChecked()
            is_inverso = self.inverter_checkbox.isChecked()
            is_diferente = self.modelos_diferentes_checkbox.isChecked() and is_par and not is_inverso
            is_avancado = self.avancado_checkbox.isChecked()
            selecao_ouro = self.tipo_ouro_combo.currentText()
            densidade = self.densidades[selecao_ouro]
            valor_grama = self.settings.get("valor_ouro_18k" if selecao_ouro == "Ouro 18k" else "valor_ouro_10k", 0)

            if not is_inverso:
                params1 = self._get_anel_params(1)
                massa1, valor1 = self._calcular_massa_valor(params1, densidade, valor_grama)

                if is_par:
                    if is_diferente:
                        params2 = self._get_anel_params(2)
                    else:
                        params2 = params1.copy()
                        tamanho2 = int(self.tamanho_anel_input_2.currentText())
                        params2["diametro_mm"] = get_diametro_por_tamanho(tamanho2)
                    
                    massa2, valor2 = self._calcular_massa_valor(params2, densidade, valor_grama)
                    massa_total, valor_total = massa1 + massa2, valor1 + valor2
                    massa_media = massa_total / 2.0
                    
                    if is_avancado:
                        self.painel_1.findChild(QLabel, "resultado_valor").setText(f"{massa_total:.2f} g")
                        self.painel_2.findChild(QLabel, "resultado_valor").setText(self._format_currency(valor_total))
                        self.painel_3.findChild(QLabel, "resultado_valor").setText(f"{massa_media:.2f} g")
                        self.painel_4.findChild(QLabel, "resultado_valor").setText(f"{massa1:.2f}g / {massa2:.2f}g")
                    else:
                        self.painel_1.findChild(QLabel, "resultado_valor").setText(f"{massa_total:.2f} g")
                        self.painel_2.findChild(QLabel, "resultado_valor").setText(self._format_currency(valor_total))
                else:
                    self.painel_1.findChild(QLabel, "resultado_valor").setText(f"{massa1:.2f} g")
                    self.painel_2.findChild(QLabel, "resultado_valor").setText(self._format_currency(valor1))
            else:
                massa_alvo_total = 0.0
                if self.radio_por_peso.isChecked():
                    massa_alvo_total = float(self.massa_alvo_input.text().replace(',', '.'))
                else:
                    valor_alvo_total = float(self.valor_alvo_input.text().replace(',', '.'))
                    if valor_grama <= 0: raise ValueError("Valor/g deve ser > 0.")
                    massa_alvo_total = valor_alvo_total / valor_grama
                if massa_alvo_total <= 0: raise ValueError("Alvo deve ser > 0.")

                largura_mm = self._get_largura_mm(self.largura_combo_1, self.largura_personalizada_input_1)
                diametro_mm1 = get_diametro_por_tamanho(int(self.tamanho_anel_input_1.currentText()))

                if is_par:
                    diametro_mm2 = get_diametro_por_tamanho(int(self.tamanho_anel_input_2.currentText()))
                    espessura_cm = calcular_espessura_par(diametro_mm1/10, diametro_mm2/10, largura_mm/10, densidade, massa_alvo_total)
                    massa1 = calcular_massa_alianca(diametro_mm1/10, espessura_cm, largura_mm/10, densidade)
                    massa2 = calcular_massa_alianca(diametro_mm2/10, espessura_cm, largura_mm/10, densidade)
                    self.painel_1.findChild(QLabel, "resultado_valor").setText(f"{espessura_cm * 10:.2f} mm")
                    self.painel_2.findChild(QLabel, "resultado_valor").setText(f"{massa1:.2f}g / {massa2:.2f}g")
                else:
                    espessura_cm = calcular_espessura_alianca(diametro_mm1/10, largura_mm/10, densidade, massa_alvo_total)
                    self.painel_1.findChild(QLabel, "resultado_valor").setText(f"{espessura_cm * 10:.2f} mm")

        except (ValueError, TypeError) as e:
            self.painel_1.findChild(QLabel, "resultado_label").setText("Erro!")
            self.painel_1.findChild(QLabel, "resultado_valor").setText(str(e) if str(e) else "Verifique os valores.")
            for panel in [self.painel_2, self.painel_3, self.painel_4]:
                panel.findChild(QLabel, "resultado_label").setText(""); panel.findChild(QLabel, "resultado_valor").setText("")
        except Exception as e:
            self.painel_1.findChild(QLabel, "resultado_label").setText("Erro Inesperado!")
            self.painel_1.findChild(QLabel, "resultado_valor").setText(str(e))
    
    def _calcular_massa_valor(self, params, densidade, valor_grama):
        massa_teorica = calcular_massa_alianca(params["diametro_mm"]/10, params["espessura_mm"]/10, params["largura_mm"]/10, densidade)
        massa_ajustada = massa_teorica * (1 + params["constante"])
        valor = massa_ajustada * valor_grama
        return massa_ajustada, valor
    
    def _format_currency(self, value):
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")