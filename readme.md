# Mapeio Pack - EAN & DUN-14 Converter

Ferramenta desenvolvida em Python/Streamlit para automação, limpeza e conversão cruzada de códigos de barras logísticos (EAN ↔ DUN).
*Herramienta desarrollada en Python/Streamlit para la automatización, limpieza y conversión cruzada de códigos de barras logísticos (EAN ↔ DUN).*

---

## Português: Como o Código Funciona (Algoritmo Detalhado)

O script lê uma base de dados coluna a coluna e aplica a seguinte lógica de transformação estrutural para cada registro:

### 1. Sanitização de Dados
* Remove espaços em branco (`strip()`).
* Remove resíduos de formatação de planilhas, como `.0` gerados quando códigos numéricos longos são lidos como float (`replace(".0", "")`).
* Valida se a string resultante contém apenas números (`isdigit()`). Se contiver letras ou caracteres especiais, retorna como "Inválido".

### 2. Identificação e Extração da Base
O sistema conta o tamanho da string limpa e divide a lógica em duas ramificações:

* **Caso 1: String com 13 dígitos (Input EAN-13)**
  * A coluna de saída `EAN-13` recebe o próprio input.
  * O código extrai a raiz: os primeiros 12 dígitos da string.

* **Caso 2: String com 14 dígitos (Input DUN-14)**
  * O código ignora o Indicador Logístico (1º dígito) e o Dígito Verificador (14º dígito), extraindo o miolo central (da posição 2 à 13).
  * O sistema **recalcula** o dígito verificador dessa raiz de 12 números para descobrir qual é o código do produto unitário e popula a coluna de saída `EAN-13`.

### 3. Geração das 9 Variantes Logísticas (DUN-14)
Com a raiz de 12 dígitos isolada, o código inicia um loop (`for v in range(1, 10)`):
1. Concatena o número do loop (1 a 9) no início da raiz (formando 13 dígitos).
2. Envia essa nova string para a função `calcular_digito_gs1()`.
3. A função aplica o **Módulo 10**: lendo a string da direita para a esquerda, multiplica os números alternadamente por 3 e 1. A soma total é subtraída do próximo múltiplo de 10.
4. O dígito final é anexado à string, gerando o código DUN-14 válido nas 9 colunas de saída.

---

## Español: Cómo Funciona el Código (Algoritmo Detallado)

El script lee una base de datos columna por columna y aplica la siguiente lógica de transformación estructural para cada registro:

### 1. Saneamiento de Datos
* Elimina espacios en blanco (`strip()`).
* Elimina residuos de formato de hojas de cálculo, como `.0` generados cuando códigos numéricos largos se leen como float (`replace(".0", "")`).
* Valida si la cadena resultante contiene solo números (`isdigit()`). Si contiene letras o caracteres especiales, se devuelve como "Inválido".

### 2. Identificación y Extracción de la Base
El sistema cuenta el tamaño de la cadena limpia y divide la lógica en dos ramas:

* **Caso 1: Cadena de 13 dígitos (Input EAN-13)**
  * La columna de salida `EAN-13` recibe el input original.
  * El código extrae la raíz: los primeros 12 dígitos de la cadena.

* **Caso 2: Cadena de 14 dígitos (Input DUN-14)**
  * El código ignora el Indicador Logístico (1º dígito) y el Dígito Verificador (14º dígito), extrayendo el núcleo central (de la posición 2 a la 13).
  * El sistema **recalcula** el dígito verificador de esta raíz de 12 números para descubrir cuál es el código del producto unitario y llena la columna de salida `EAN-13`.

### 3. Generación de las 9 Variantes Logísticas (DUN-14)
Con la raíz de 12 dígitos aislada, el código inicia un bucle (`for v in range(1, 10)`):
1. Concatena el número del bucle (1 a 9) al inicio de la raíz (formando 13 dígitos).
2. Envía esta nueva cadena a la función `calcular_digito_gs1()`.
3. La función aplica el **Módulo 10**: leyendo la cadena de derecha a izquierda, multiplica los números alternativamente por 3 y 1. La suma total se resta del próximo múltiplo de 10.
4. El dígito final se anexa a la cadena, generando el código DUN-14 válido en las 9 columnas de salida.

---

## Como executar / Cómo ejecutar
1. Instale as dependências: `pip install -r requirements.txt`
2. Inicie o servidor local: `streamlit run app.py`