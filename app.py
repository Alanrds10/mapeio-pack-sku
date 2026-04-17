import streamlit as st
import pandas as pd
import io

# ==========================================
# 1. FUNÇÕES DE LÓGICA E CÁLCULO
# ==========================================

def calcular_digito_gs1(payload: str) -> str:
    """
    Calcula o dígito verificador Módulo 10 da GS1 usando a regra universal.
    """
    total_soma = 0
    multiplicador = 3
    
    for digito in reversed(payload):
        total_soma += int(digito) * multiplicador
        multiplicador = 1 if multiplicador == 3 else 3
        
    resto = total_soma % 10
    digito_verificador = 0 if resto == 0 else 10 - resto
    return str(digito_verificador)

def processar_sku(sku) -> pd.Series:
    """
    Identifica o tipo de SKU e gera todas as 9 variantes logísticas (DUN-14).
    """
    sku_str = str(sku).strip().replace(".0", "")
    
    resultado = {
        "SKU Original": sku_str,
        "Tipo Identificado": "Inválido",
        "EAN-13": "N/A"
    }
    
    for v in range(1, 10):
        resultado[f"DUN-14 (Var {v})"] = "N/A"
    
    if not sku_str.isdigit():
        return pd.Series(resultado)

    tamanho = len(sku_str)

    if tamanho == 13:
        resultado["Tipo Identificado"] = "EAN-13"
        resultado["EAN-13"] = sku_str
        base_12 = sku_str[:12]
        
    elif tamanho == 14:
        resultado["Tipo Identificado"] = "DUN-14"
        base_12 = sku_str[1:13] 
        resultado["EAN-13"] = base_12 + calcular_digito_gs1(base_12)
        
    else:
        return pd.Series(resultado)

    for v in range(1, 10):
        prefixo = str(v)
        base_dun = prefixo + base_12
        resultado[f"DUN-14 (Var {v})"] = base_dun + calcular_digito_gs1(base_dun)
    
    return pd.Series(resultado)


# ==========================================
# 2. INTERFACE STREAMLIT
# ==========================================

st.set_page_config(page_title="Mapeio Pack", layout="wide")

st.title("Mapeio Pack - EAN e Variantes Logísticas")

# Texto atualizado sem os bullet points
st.markdown("""
O que são Variantes Logísticas? As **Variantes Logísticas** (ou Indicadores Logísticos) são o primeiro dígito de um código DUN-14 (GTIN-14). Eles são utilizados para identificar diferentes níveis de acondicionamento de um mesmo produto:

| Variante | Nível de Embalagem e Categorias Comuns no Varejo |
| :--- | :--- |
| **1** | **Caixa Padrão / Primária:** Nível inicial de agrupamento. Muito comum no recebimento de Mercearia, Cosméticos e Farmácia. |
| **2** | **Caixa Master / Fardo Secundário:** Agrupamento de caixas menores. Frequente no setor de Bebidas (fardos), Limpeza e Higiene Pessoal. |
| **3 a 8** | **Grandes Volumes e Paletes:** Utilizados para níveis crescentes de empacotamento. Dominante em Atacarejos (Cash & Carry), Materiais de Construção e recebimento de Eletrodomésticos. |
| **9** | **Itens de Peso Variável:** Uso exclusivo e obrigatório para produtos cujo preço ou quantidade varia por embalagem. Essencial para Açougue, Hortifrúti (FLV), Frios e Laticínios. |
""")

st.divider()

arquivo_upload = st.file_uploader("Arraste seu arquivo Excel ou CSV (SKUs na Coluna A)", type=["xlsx", "xls", "csv"])

if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df_input = pd.read_csv(arquivo_upload)
        else:
            df_input = pd.read_excel(arquivo_upload)
            
        nome_coluna_alvo = df_input.columns[0]
        
        st.info(f"Processando registros da coluna: **{nome_coluna_alvo}**")
        
        df_resultado = df_input[nome_coluna_alvo].apply(processar_sku)
        
        st.success("Cálculos concluídos!")
        st.dataframe(df_resultado, use_container_width=True)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_resultado.to_excel(writer, index=False, sheet_name='Mapeio de SKUs')
        processed_data = output.getvalue()
        
        st.download_button(
            label="⬇️ Baixar Relatório Completo",
            data=processed_data,
            file_name="mapeio_pack_logistica.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")