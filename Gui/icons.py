# Gui/icons.py
from PyQt6.QtCore import QSize, Qt, QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtSvg import QSvgRenderer 

def create_settings_icon() -> QIcon:
    """Renderiza o SVG da engrenagem e retorna como QIcon."""
    # --- SVG SUPER SIMPLIFICADO E CONFIÁVEL PARA A ENGRENAGEM ---
    svg_data = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <path fill="#DAA520" d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 l-3.84,0c-0.24,0-0.44,0.17-0.48,0.41L9.22,5.25C8.63,5.5,8.1,5.82,7.6,6.2L5.21,5.24C5,5.17,4.75,5.24,4.63,5.46L2.71,8.78 c-0.12,0.21-0.07,0.47,0.12,0.61l2.03,1.58C4.82,11.36,4.8,11.68,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.38,2.44 c0.04,0.24,0.24,0.41,0.48,0.41l3.84,0c0.24,0,0.44-0.17,0.48-0.41l0.38-2.44c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0.01,0.59-0.22l1.92-3.32c0.12-0.2,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
    </svg>
    """
    svg_bytes = QByteArray(svg_data.encode('utf-8'))
    renderer = QSvgRenderer(svg_bytes)
    
    # Criando a tela de desenho com tamanho fixo e uniforme
    pixmap = QPixmap(QSize(32, 32))
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)


def create_home_icon() -> QIcon:
    """Renderiza o SVG da casa e retorna como QIcon."""
    svg_data = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path fill="#DAA520" d="M10,20v-6h4v6h5v-8h3L12,3L2,12h3v8H10z"/>
    </svg>
    """
    svg_bytes = QByteArray(svg_data.encode('utf-8'))
    renderer = QSvgRenderer(svg_bytes)

    # Criando a tela de desenho com tamanho fixo e uniforme
    pixmap = QPixmap(QSize(32, 32))
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)


def create_menu_icon() -> QIcon:
    """Renderiza o SVG do menu e retorna como QIcon."""
    svg_data = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path fill="#DAA520" d="M3,6h18v2H3V6z M3,11h18v2H3V11z M3,16h18v2H3V16z"/>
    </svg>
    """
    svg_bytes = QByteArray(svg_data.encode('utf-8'))
    renderer = QSvgRenderer(svg_bytes)

    # Criando a tela de desenho com tamanho fixo e uniforme
    pixmap = QPixmap(QSize(32, 32))
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)