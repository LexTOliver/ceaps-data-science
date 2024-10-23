import chardet
import pandas as pd
import os
import sys


__all__ = ["read_data_from_dir", "read_data", "detect_encoding"]


def detect_encoding(file_path: str) -> str:
    """
    Detect the encoding of a file.
    :param file_path: str
    :return: str
    """
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def read_data_from_dir(
    dir_path: str, encoding: str = "auto", separator: str = ","
) -> pd.DataFrame:
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
                enc = detect_encoding(file)
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


def read_data(
    file_path: str, encoding: str = "auto", separator: str = ","
) -> pd.DataFrame:
    """
    Read data from a file and return the dataframe.
    :param file_path: str
    :param encoding: str
    :param separator: str
    :return: DataFrame
    """
    try:
        # Check if the file exists
        assert os.path.exists(file_path), f"File {file_path} not found."

        if encoding == "auto":
            enc = detect_encoding(file_path)
            print(f"Reading file: {file_path} with encoding: {enc}")
        else:
            enc = encoding

        data = pd.read_csv(file_path, encoding=enc, sep=separator, skiprows=1)
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
