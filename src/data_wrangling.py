import pandas as pd
import os
import sys
import re
import argparse


def create_parser() -> argparse.ArgumentParser:
    """
    Parse the arguments.
    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Data Wrangling")
    parser.add_argument(
        "dir_path", type=str, help="Path to the directory with the data."
    )
    parser.add_argument(
        "-enc", "--encoding", type=str, default="latin1", help="Encoding of the files."
    )
    parser.add_argument(
        "-sep", "--separator", type=str, default=";", help="Separator of the files."
    )
    parser.add_argument(
        "-out", "--output", type=str, default="./data/data.csv", help="Output file."
    )
    return parser


def read_data(dir_path, encoding: str = "latin1", separator: str = ";") -> pd.DataFrame:
    """
    Read data from a directory and return the dataframe.
    :param dir_path: str
    :return: DataFrame
    """
    try:
        # Check if the directory exists and if there are csv files
        assert os.path.exists(dir_path), f"Directory {dir_path} not found."

        # Check if there are csv files in the directory and list them
        file_list = os.listdir(dir_path)
        file_list = [file for file in file_list if file.endswith(".csv")]
        assert len(file_list) > 0, f"No csv files found in {dir_path}."

        # Read the csv files
        data = pd.DataFrame()
        for file in file_list:
            data = pd.concat(
                [
                    data,
                    pd.read_csv(
                        os.path.join(dir_path, file),
                        encoding=encoding,
                        sep=separator,
                        skiprows=1,
                    ),
                ]
            )
    except UnicodeDecodeError as e:
        print(
            "Error:Could not decode csv file.\nTry to pass 'utf-8' or 'latin1'. Also, check the encoding of the files."
        )
        print(e)
        sys.exit(1)
    except pd.errors.ParserError as e:
        print("Error: Could not parse csv file.\nCheck the separator.")
        print(e)
        sys.exit(1)
    except AssertionError as e:
        print("Error: ", e)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    return data


def format_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Format the data.
    :param data: DataFrame
    :return: DataFrame
    """
    # Drop duplicates
    print(f"Found {data.duplicated().sum()} duplicates.")
    data.drop_duplicates(inplace=True)

    # Drop rows if DATA doesn't match ANO
    # wrong_date = data[data['DATA'].dt.year != data['ANO']]
    # print(f"Found {wrong_date.shape[0]} rows where year doesn't match.")
    # data.drop(wrong_date.index, inplace=True)

    # Replace missing values with "Não Identificado" in columns: 'CNPJ_CPF', 'FORNECEDOR', 'DOCUMENTO'
    data = data.fillna(
        {
            "CNPJ_CPF": "Não Identificado",
            "FORNECEDOR": "Não Identificado",
            "DOCUMENTO": "Não identificado",
        }
    )

    # Change column type to string for columns: 'SENADOR', 'TIPO_DESPESA' and 5 other columns
    data = data.astype(
        {
            "SENADOR": "string",
            "TIPO_DESPESA": "string",
            "CNPJ_CPF": "string",
            "FORNECEDOR": "string",
            "DOCUMENTO": "string",
            "DETALHAMENTO": "string",
            "COD_DOCUMENTO": "string",
        }
    )

    # Replace missing values with "Sem detalhamento" in column: 'DETALHAMENTO'
    data = data.fillna({"DETALHAMENTO": "Sem detalhamento"})

    # Change column type to float64 for column: 'VALOR_REEMBOLSADO'
    data["VALOR_REEMBOLSADO"] = data["VALOR_REEMBOLSADO"].str.replace(
        ",", ".", case=False, regex=False
    )
    data["VALOR_REEMBOLSADO"] = data["VALOR_REEMBOLSADO"].str.replace(
        "[^0-9.]", "", case=False, regex=True
    )
    data = data.astype({"VALOR_REEMBOLSADO": "float64"})

    # Filter rows based on column: 'DATA'
    # Define the regex pattern for the date format "dd/mm/YYYY"
    pattern = r"\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}\b"
    data["DATA"] = data["DATA"].apply(
        lambda x: x if re.match(pattern, str(x)) else None
    )
    data["DATA"] = pd.to_datetime(
        data["DATA"], format="%d/%m/%Y", dayfirst=True, errors="coerce"
    )

    return data


def ceaps_data_wrangling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform data wrangling on the CEAPS dataset.
    :param df: DataFrame
    :return: DataFrame
    """
    data = format_data(df)
    print(data.info())
    # print(data[['ANO', 'MES', 'DATA']].sort_values(by='DATA', ascending=False).head(10))

    return data


def main():
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Read and format data
    data = read_data(args.dir_path, encoding=args.encoding, separator=args.separator)

    # Perform data wrangling
    data = ceaps_data_wrangling(data)

    # Save data
    data.to_csv(args.output, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
