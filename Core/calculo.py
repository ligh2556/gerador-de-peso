# Core/calculo.py
import math

# A tabela e a função get_diametro_por_tamanho permanecem as mesmas...
TABELA_TAMANHO_ARO_MM = {
    10: 14.65, 11: 14.95, 12: 15.35, 13: 15.65, 14: 15.95, 15: 16.65,
    16: 16.95, 17: 17.35, 18: 17.65, 19: 17.95, 20: 18.35, 21: 18.65,
    22: 18.95, 23: 19.35, 24: 19.65, 25: 19.95, 26: 20.35, 27: 20.35,
    28: 20.65, 29: 20.95, 30: 21.35, 31: 21.65, 32: 21.95, 33: 22.35,
    34: 22.65, 35: 23.05
}

def get_diametro_por_tamanho(tamanho: int) -> float | None:
    return TABELA_TAMANHO_ARO_MM.get(tamanho)


# A função original não muda.
def calcular_massa_alianca(diametro_interno_cm: float, espessura_cm: float, largura_cm: float, densidade: float) -> float:
    if any(val <= 0 for val in [diametro_interno_cm, espessura_cm, largura_cm, densidade]):
        raise ValueError("Dimensões/densidade devem ser positivas.")
    raio_interno_cm = diametro_interno_cm / 2
    raio_externo_cm = raio_interno_cm + espessura_cm
    volume_cm3 = math.pi * (raio_externo_cm**2 - raio_interno_cm**2) * largura_cm
    massa_gramas = densidade * volume_cm3
    return massa_gramas


# --- MUDANÇA: Nova função para o cálculo inverso ---
def calcular_espessura_alianca(diametro_interno_cm: float, largura_cm: float, densidade: float, massa_desejada_g: float) -> float:
    """
    Calcula a espessura de uma aliança com base na massa desejada e outras dimensões.
    """
    if any(val <= 0 for val in [diametro_interno_cm, largura_cm, densidade, massa_desejada_g]):
        raise ValueError("Dimensões, densidade e massa devem ser valores positivos.")

    raio_interno_cm = diametro_interno_cm / 2

    # Reorganizando a fórmula: V = m/d  e  V = pi * (re^2 - ri^2) * L
    # m/d = pi * (re^2 - ri^2) * L
    # (m/d) / (pi * L) = re^2 - ri^2
    # re^2 = (m/d) / (pi*L) + ri^2
    # re = sqrt(...)
    # e = re - ri

    termo_volume = massa_desejada_g / (densidade * math.pi * largura_cm)
    
    # Verifica se a massa é suficiente para o diâmetro e largura dados
    if termo_volume < 0:
        raise ValueError("Massa insuficiente para as dimensões fornecidas.")

    raio_externo_ao_quadrado = termo_volume + (raio_interno_cm**2)
    raio_externo_cm = math.sqrt(raio_externo_ao_quadrado)
    
    espessura_cm = raio_externo_cm - raio_interno_cm
    
    return espessura_cm