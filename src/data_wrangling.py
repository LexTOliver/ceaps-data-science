import chardet
import pandas as pd
import os
import sys
import re
import argparse


__all__ = ["ceaps_data_wrangling", "read_data", "format_data"]


def _create_parser() -> argparse.ArgumentParser:
    """
    Parse the arguments.
    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Data Wrangling")
    parser.add_argument(
        "-dir",
        "--dir_path",
        default="./data/raw",
        type=str,
        help="Path to the directory with the raw data.",
    )
    parser.add_argument(
        "-enc",
        "--encoding",
        type=str,
        default="Windows-1258",
        help="Encoding of the files.",
    )
    parser.add_argument(
        "-sep", "--separator", type=str, default=";", help="Separator of the files."
    )
    parser.add_argument(
        "-out",
        "--output",
        type=str,
        default="./data/interim/data.csv",
        help="Output file.",
    )
    return parser


def _detect_encoding(file_path: str) -> str:
    """
    Detect the encoding of a file.
    :param file_path: str
    :return: str
    """
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def read_data(dir_path: str, encoding: str = "auto", separator: str = ";") -> pd.DataFrame:
    """
    Read data from a directory and return the dataframe.
    :param dir_path: str
    :param encoding: str
    :param separator: str
    :return: DataFrame
    """
    # TODO: Add support for reading from a URL link
    try:
        # Check if the directory exists and if there are csv files
        assert os.path.exists(dir_path), f"Directory {dir_path} not found."

        # Check if there are csv files in the directory and list them
        file_list = os.listdir(dir_path)
        file_list = [
            os.path.join(dir_path, file) for file in file_list if file.endswith(".csv")
        ]
        assert len(file_list) > 0, f"No csv files found in {dir_path}."

        # Read the csv files
        data = pd.DataFrame()
        for file in file_list:
            if encoding == "auto":
                enc = _detect_encoding(file)
                print(f"Reading file: {file} with encoding: {enc}")
            else:
                enc = encoding

            data = pd.concat(
                [
                    data,
                    pd.read_csv(
                        file,
                        encoding=enc,
                        sep=separator,
                        skiprows=1,
                    ),
                ]
            )
    except UnicodeDecodeError as e:
        print(
            "ERROR: Could not decode csv file.\nCheck the encoding of the files or set the argument to 'auto'."
        )
        print("Exception:", e)
        sys.exit(1)
    except pd.errors.ParserError as e:
        print("ERROR: Could not parse csv file.\nCheck the separator.")
        print("Exception:", e)
        sys.exit(1)
    except AssertionError as e:
        print("ERROR:", e)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred!\nException: {e}")
        sys.exit(1)

    return data


def format_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Format the data.
    :param data: DataFrame
    :return: DataFrame
    """
    # Drop duplicates
    data.drop_duplicates(inplace=True)

    # Drop rows if DATA doesn't match ANO
    # wrong_date = data[data['DATA'].dt.year != data['ANO']]
    # print(f"Found {wrong_date.shape[0]} rows where year doesn't match.")
    # data.drop(wrong_date.index, inplace=True)

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

    # Replace missing values with "Não Identificado" in columns: 'CNPJ_CPF', 'FORNECEDOR', 'DOCUMENTO'
    data = data.fillna(
        {
            "CNPJ_CPF": "Não Identificado",
            "FORNECEDOR": "Não Identificado",
            "DOCUMENTO": "Não identificado",
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

    return data


def _main():
    # Parse arguments
    parser = _create_parser()
    args = parser.parse_args()

    # Read and format data
    print(f"Reading data from directory {args.dir_path}...")
    print(f"Encoding: {args.encoding}")
    print(f"Separator: {args.separator}")
    data = read_data(args.dir_path, encoding=args.encoding, separator=args.separator)

    # Perform data wrangling
    print("Performing data wrangling...")
    data = ceaps_data_wrangling(data)

    # Save data
    print(f"Saving data to {args.output}...")
    data.to_csv(args.output, index=False, encoding="utf-8")


if __name__ == "__main__":
    _main()
