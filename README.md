# Maturitní data CERMAT
This repository is relevant only to Czech nationals. Hence the documentation is maintained in Czech language.

**Neoficiální** kompilace dat z webu [https://vysledky.cermat.cz/data](https://vysledky.cermat.cz/data/Default.aspx). CERMAT nenabízí možnost stažení všech dat najednou. Manuální stažení všech dat je možné, ale pracné. Naštěstí to může python udělat za nás.

Prosím všechny aby k datům přistupovali zodpovědně a případné závěry si pečlivě rozmysleli.

## Stáhnout data
TODO

## Jak pustit python script na stažení dat
1. Nainstalujte si python >= 3.7.x
2. Nainstalujte závislosti:   
    ```pip install beautifulsoup4 requests pandas openpyxl```
3. Spusťte skript:   
    ```python download.py```
4. Skript vytvoří soubor `maturita_dd-mm-YYYY.xlsx`

## Jsem z CERMATu a vadí mi, že jsou naše data volně přístupná
Napište mi na `sivakfil@gmail.com`.
