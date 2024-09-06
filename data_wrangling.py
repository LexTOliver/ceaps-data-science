import pandas as pd
import os, sys


def read_data(dir_path, encoding: str ='latin1', separator: str = ';') -> pd.DataFrame:
    """
    Read data from a directory and return the dataframe.
    :param dir_path: str
    :return: DataFrame
    """
    assert os.path.exists(dir_path), f"Directory {dir_path} not found."
    try:
        file_list = os.listdir(dir_path)
        data = pd.DataFrame()
        for file in file_list:
            if file.endswith('.csv'):
                data = pd.concat([data, pd.read_csv(os.path.join(dir_path, file), encoding=encoding, sep=separator, skiprows=1)])
    except UnicodeDecodeError as e:
        print(f"Could not decode csv file. Try to pass 'utf-8' or 'latin1'. Also, check the encoding of the files.")
        print(e)
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"Could not parse csv file. Check the separator.")
        print(e)
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
    # Format columns data types
    data['ANO'] = pd.to_numeric(data['ANO'], errors='coerce')
    data['MES'] = pd.to_numeric(data['MES'], errors='coerce')
    data['SENADOR'] = data['SENADOR'].astype(str)
    data['TIPO_DESPESA'] = data['TIPO_DESPESA'].astype(str)
    data['CNPJ_CPF'] = data['CNPJ_CPF'].astype(str)
    data['FORNECEDOR'] = data['FORNECEDOR'].astype(str)
    data['DOCUMENTO'] = data['DOCUMENTO'].astype(str)
    data['DATA'] = pd.to_datetime(data['DATA'], format='%d/%m/%Y', errors='coerce')
    data['DETALHAMENTO'] = data['DETALHAMENTO'].astype(str)
    data['VALOR_REEMBOLSADO'] = pd.to_numeric(data['VALOR_REEMBOLSADO'].str.replace(',', '.'), errors='coerce')
    data['COD_DOCUMENTO'] = data['COD_DOCUMENTO'].astype(str)

    # Drop duplicates
    print(f"Found {data.duplicated().sum()} duplicates.")
    data.drop_duplicates(inplace=True)

    # Drop rows if DATA doesn't match ANO
    wrong_date = data[data['DATA'].dt.year != data['ANO']]
    print(f"Found {wrong_date.shape[0]} rows where year doesn't match.")
    data.drop(wrong_date.index, inplace=True)

    return data

def main():
    data = read_data('./data/raw', encoding='latin1', separator=';')
    data = format_data(data)
    print(data.info())

    # print(data[['ANO', 'MES', 'DATA']].sort_values(by='DATA', ascending=False).head(10))


if __name__ == '__main__':
    main()