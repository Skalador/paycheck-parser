# Paycheck Parser

In this repostiory a `python` parser for paychecks is built. This parser reads the paychecks in PDF format, which are generated from [Sage DPW](https://www.sagedpw.at/), and extracts the ["Betriebsratsumlage"](https://noe.arbeiterkammer.at/service/betriebsrat/Betriebsratsumlage.html) into `xlsx`/`excel` format. [This item of the paycheck in Austria can be used to reduce the taxes paid in a fiscal year.](https://noe.arbeiterkammer.at/service/betriebsrat/Betriebsratsumlage___Steuern.html) This reduction has to be placed in the ["Werbungskosten"](https://noe.arbeiterkammer.at/beratung/steuerundeinkommen/steuertipps/Werbungskosten.html) field of the Austrian tax report. 

All files will be parsed for the following regexp patterns:
- `'für den Zeitraum (\w+) (\d{4})'`, e.g. `'für den Zeitraum Jänner 2023'`
- `'BRU 0,5 % (\d+,\d+)'`, e.g. `'9331BRU 0,5% 12,34-'`

to extract the fiscal year, month as well as the "Betriebsratsumlage" in the corresponding month. Follow the instructions [here](#execute-the-code) to execute the code and put the data into `Werbungskosten.xlsx`.

Note: It is assumed, that the `BRU` is `0.5%`.

The `Werbungskosten.xlsx` will look like:
| Jahr |    Monat |      Beschreibung|   Wert|
|------|----------|------------------|-------|
| 2023 |   Jänner |Betriebsratsumlage|  10.00|
| 2023 |  Februar |Betriebsratsumlage|  10.00|
| 2023 |     März |Betriebsratsumlage|  10.00|
| 2023 |    April |Betriebsratsumlage|  10.00|
| 2023 |      Mai |Betriebsratsumlage|  10.00|
| 2023 |     Juni |Betriebsratsumlage|  10.00|
| 2023 |     Juli |Betriebsratsumlage|  10.00|
| 2023 |   August |Betriebsratsumlage|  10.00|
| 2023 |September |Betriebsratsumlage|  10.00|
| 2023 |  Oktober |Betriebsratsumlage|  10.00|
| 2023 | November |Betriebsratsumlage|  10.00|
| 2023 | Dezember |Betriebsratsumlage|  10.00|
|      |          |             Summe| 120.00|

The default log level is `INFO`, which can be changed to `DEBUG` if necessary.

## Prerequisites

### Install from requirements.txt

Installing dependencies:
```
pip install --no-cache-dir -r requirements.txt
```

### Generate requirements.txt

```
# install
pip install pipreqs

# Run in current directory
python -m  pipreqs.pipreqs .
```

## Execute the code

Place all `*.pdf` files into the same folder as `main.py`. All paychecks have to be named in the format `YYYY_MM.pdf`, e.g. `2023_03.pdf`.

Run the code:
```
python main.py
```
