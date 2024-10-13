# Data Dictionary

<!-- TODO: More studies about data dictionary and Data Catalog for database documentation! -->

This data dictionary provides an overview of the data contained in the `data.csv` file, based on [CEAPS](https://www12.senado.leg.br/transparencia/dados-abertos-transparencia/dados-abertos-ceaps?utm_medium=email&_hsenc=p2ANqtz-9oraJDtmhd8_VnMw6lGWYoF-FANWSpngMwRtg5ovo9-FUTm4kwZNmhdv-VODztf3mjAuiwU6VMgVCFd_3ndX_vSNKFpg&_hsmi=231298145&utm_content=231298145&utm_source=hs_automation).

## Table of Contents

1. [Overview](#overview)
2. [Data Fields](#data-fields)
3. [Data Sample](#data-sample)

## Overview <a name="overview"></a>


CEAPS (Cota para Exercício da Atividade Parlamentar dos Senadores) is a dataset that describes all the expenses declared by Brazilian senators, divided by year.

The `data.csv` file contains the aggregation of all data between 2008 and 2022, including which senator made that expense, how much it was, when it was made, the details, the type of the expense, the supplier, and some documentation of the expense.

The dataset is structured in a comma-separated values (CSV) format. It was originally encoded as `LATIN1` and then transformed to `UTF-8`. The original delimiter was a semicolon, but after the transformations, it is now separated by a comma. The dataset transformations also include removing rows where the year of the expense does not match the year of registration.

## Data Fields <a name="data-fields"></a>

The `data.csv` file includes the following fields:

| Field              | Type          | Description                                                                                   |
|--------------------|---------------|-----------------------------------------------------------------------------------------------|
| ANO                | Numeric       | Represents the year in which the expense was registered on CEAPS.                             |
| MES                | Numeric       | Represents the month in which the expense was registered on CEAPS.                            |
| SENADOR            | String        | Indicates the name of the senator who made the expense.                                       |
| TIPO_DESPESA       | String        | Specifies the type of the expense.                                                            |
| CNPJ_CPF           | String        | Denotes the identification document of the supplier.                                          |
| FORNECEDOR         | String        | States the name of the supplier company.                                                      |
| DOCUMENTO          | String        | Refers to the document that records the expense.                                              |
| DATA               | Datetime      | Indicates the date when the expense was made.                                                 |
| DETALHAMENTO       | String        | Provides details or a description of the expense.                                             |
| VALOR_REEMBOLSADO  | Numeric       | Represents the amount of the expense in the brazilian currency.                                                         |
| COD_DOCUMENTO      | String        | Represents the documentation code of the expense.                                             |


## Data Sample <a name="data-sample"></a>

Here is a sample of the data contained in the `data.csv` file:

| ANO  | MES | SENADOR                | TIPO_DESPESA                                                | CNPJ_CPF           | FORNECEDOR                            | DOCUMENTO | DATA       | DETALHAMENTO                                                     | VALOR_REEMBOLSADO | COD_DOCUMENTO |
|------|-----|------------------------|-------------------------------------------------------------|--------------------|---------------------------------------|-----------|------------|------------------------------------------------------------------|-------------------|---------------|
| 2014 | 12  | ANTONIO AURELIANO      | Locomoção, hospedagem, alimentação, combustíveis e lubrificantes | 16.978.175/0001-08 | Adria Viagens e Turismo Ltda          | 000719    | 2014-12-16 | Carro utilizado pelo senador Antônio Aureliano ao estado de Minas Gerais. | 962.49            | 987160        |
| 2014 | 1   | ANTONIO CARLOS RODRIGUES | Aluguel de imóveis para escritório político, compreendendo despesas concernentes a eles. | 07.885.958/0001-56 | CONTROLAR PRESTAÇÃO DE SERVIÇOS DE PORTARIA | 00002156  | 2014-01-02 | SERVIÇOS DE LIMPEZA DO ESCRITORIO DE APOIO PARLAMENTAR REFERENTE AO MES DE JANEIRO 2014 | 346.0             | 880818        |
| 2014 | 1   | ARMANDO MONTEIRO       | Aluguel de imóveis para escritório político, compreendendo despesas concernentes a eles. | 10.835.932/0001-08 | CELPE                                 | 2966730   | 2014-02-10 | ENERGIA ELÉTRICA DO ESCRITÓRIO POLÍTICO DO SENADOR ARMANDO MONTEIRO SALA 1002 | 361.56            | 903320        |
...

This sample provides a glimpse of the data structure and values present in the dataset.
