# Consulta de informações por Aeródromo

**Busque informações de cartas, tempo, TAF e METAR.**

---

# Requisitos

* Python 3
* Beautifulsoup 4

# Instalação

Clone este repositório

    git clone https://github.com/Guilehm/consulta-aisweb.git

Entre no diretório

    cd consulta-aisweb
    
Instale o Beautifulsoup 4

    pip install beautifulsoup4
    
# Utilização

**Execute o arquivo `consulta.py`:**
- Digite o código ICAO de um aeródromo:
```
SBJD
```
Será impresso:
- As cartas disponíveis.
- Os horários de nascer e pôr do sol neste dia.
- As informações de TAF e METAR disponíveis.
