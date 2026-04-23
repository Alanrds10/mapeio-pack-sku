# Mapeio Pack - EAN & DUN-14 Converter

Ferramenta desenvolvida em Python/Streamlit para automação e validação de códigos de barras logísticos.
*Herramienta desarrollada en Python/Streamlit para la automatización y validación de códigos de barras logísticos.*

---

## 🇧🇷 Português: Documentação do Algoritmo

### Objetivo
Padronizar a conversão entre unidades de venda (EAN-13) e unidades de embarque (DUN-14/GTIN-14), gerando automaticamente todas as 9 variantes logísticas possíveis para cada SKU.

### Lógica de Cálculo (Módulo 10)
O algoritmo segue o padrão global da GS1 para cálculo de dígito verificador:
1. **Extração da Base:** O sistema extrai os 12 dígitos fundamentais do SKU (do dígito 1 ao 12 no EAN-13; do dígito 2 ao 13 no DUN-14).
2. **Adição do Prefixo:** Adiciona-se o Indicador Logístico (Variante de 1 a 9) à frente da base.
3. **Ponderação:** Da direita para a esquerda, os 13 dígitos resultantes são multiplicados alternadamente por pesos **3** e **1**.
4. **Soma e Módulo:** O resultado da soma das multiplicações é submetido ao Módulo 10.
5. **Dígito Final:** O dígito verificador é a diferença entre o resultado e o próximo múltiplo de 10.

### Tabela de Variantes
| Variante | Descrição |
| :--- | :--- |
| 1 | Caixa Padrão / Primária |
| 2 | Caixa Master / Fardo Secundário |
| 3 - 8 | Grandes Volumes e Paletes |
| 9 | Itens de Peso Variável (Obrigatório) |

---

## 🇺🇾 Español: Documentación del Algoritmo

### Objetivo
Estandarizar la conversión entre unidades de venta (EAN-13) y unidades de transporte (DUN-14/GTIN-14), generando automáticamente las 9 variantes logísticas posibles para cada SKU.

### Lógica de Cálculo (Módulo 10)
El algoritmo sigue el estándar global de GS1 para el cálculo del dígito verificador:
1. **Extracción de la Base:** El sistema extrae los 12 dígitos fundamentales del SKU (del dígito 1 al 12 en el EAN-13; del dígito 2 al 13 en el DUN-14).
2. **Adición de Prefijo:** Se añade el Indicador Logístico (Variante de 1 a 9) al inicio de la base.
3. **Ponderación:** De derecha a izquierda, los 13 dígitos resultantes se multiplican alternativamente por los pesos **3** y **1**.
4. **Suma y Módulo:** El resultado de la suma de las multiplicaciones se somete al Módulo 10.
5. **Dígito Final:** El dígito verificador es la diferencia entre el resultado y el próximo múltiplo de 10.

---

## Como executar / Cómo ejecutar
1. `pip install -r requirements.txt`
2. `streamlit run app.py`