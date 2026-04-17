import streamlit as st
import pandas as pd
import io

# ==========================================
# 1. FUNÇÕES DE LÓGICA E CÁLCULO
# ==========================================

def calcular_digito_gs1(payload: str) -> str:
    """
    Calcula o dígito verificador Módulo 10 da GS1 usando a regra universal:
    Da direita para a esquerda, multiplica alternadamente por 3 e 1.
    """
    total_soma = 0
    multiplicador = 3
    
    # Inverte a string para iterar da direita para a esquerda
    for digito in reversed(payload):
        total_soma += int(digito) * multiplicador
        # Alterna o multiplicador entre 3 e 1
        multiplicador = 1 if multiplicador == 3 else 3
        
    resto = total_soma % 10
    digito_verificador = 0 if resto == 0 else 10 - resto
    return str(digito_verificador)

def processar_sku(sku) -> pd.Series:
    """
    Recebe um SKU sujo, identifica o tipo e retorna todos os códigos padronizados.
    """
    # Sanitização do dado
    sku_str = str(sku).strip().replace(".0", "")
    
    # Dicionário padrão de saída
    resultado = {
        "SKU Original": sku_str,
        "Tipo Identificado": "Inválido",
        "EAN-13": "N/A",
        "DUN-14 (Var 1)": "N/A",
        "DUN-14 (Var 2)": "N/A"
    }
    
    if not sku_str.isdigit():
        return pd.Series(resultado)

    tamanho = len(sku_str)

    if tamanho == 13:
        # É um EAN-13
        resultado["Tipo Identificado"] = "EAN-13"
        resultado["EAN-13"] = sku_str
        base_12 = sku_str[:12]
        
    elif tamanho == 14:
        # É um DUN-14
        resultado["Tipo Identificado"] = "DUN-14"
        base_12 = sku_str[1:13] # Extrai os 12 dígitos que formam o EAN
        # Gera o EAN completo reconstruindo o dígito verificador
        resultado["EAN-13"] = base_12 + calcular_digito_gs1(base_12)
        
    else:
        return pd.Series(resultado)

    # Gera os DUNs correspondentes (Variantes 1 e 2)
    base_dun1 = "1" + base_12
    resultado["DUN-14 (Var 1)"] = base_dun1 + calcular_digito_gs1(base_dun1)
    
    base_dun2 = "2" + base_12
    resultado["DUN-14 (Var 2)"] = base_dun2 + calcular_digito_gs1(base_dun2)
    
    return pd.Series(resultado)


# ==========================================
# 2. INTERFACE STREAMLIT
# ==========================================

st.set_page_config(page_title="Conversor EAN/DUN", layout="wide")

st.title("📦 Conversor de SKUs (EAN ↔ DUN)")
st.markdown("Faça o upload de uma planilha contendo os SKUs na **primeira coluna**. O sistema identificará automaticamente se é EAN ou DUN e completará as informações.")

arquivo_upload = st.file_uploader("Arraste seu arquivo Excel ou CSV", type=["xlsx", "xls", "csv"])

if arquivo_upload is not None:
    try:
        # Tenta ler como CSV ou Excel dependendo do nome do arquivo
        if arquivo_upload.name.endswith('.csv'):
            df_input = pd.read_csv(arquivo_upload)
        else:
            df_input = pd.read_excel(arquivo_upload)
            
        # Pega o nome da primeira coluna para usá-la como referência
        nome_coluna_alvo = df_input.columns[0]
        
        st.info(f"Processando a coluna: **{nome_coluna_alvo}** com {len(df_input)} registros...")
        
        # Aplica a função de conversão linha a linha
        df_resultado = df_input[nome_coluna_alvo].apply(processar_sku)
        
        st.success("Processamento concluído!")
        st.dataframe(df_resultado, use_container_width=True)
        
        # Preparar o arquivo para download em Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_resultado.to_excel(writer, index=False, sheet_name='SKUs Convertidos')
        processed_data = output.getvalue()
        
        st.download_button(
            label="⬇️ Baixar Planilha Convertida",
            data=processed_data,
            file_name="skus_convertidos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")