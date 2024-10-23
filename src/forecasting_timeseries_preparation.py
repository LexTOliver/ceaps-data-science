import pandas as pd
import argparse
from utils.data_reading import read_data


__all__ = ["forecasting_timeseries_preparation"]


def _create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Forecasting Time Series Preparation')
    parser.add_argument(
        '-i',
        '--file-path',
        default='./data/interim/data.csv',
        type=str,
        help='Input file path'
    )
    parser.add_argument(
        '-enc',
        '--encoding',
        type=str,
        default='utf-8',
        help='Encoding of the files'
    )
    parser.add_argument(
        '-sep',
        '--separator',
        type=str,
        default=',',
        help='Separator of the files'
    )
    parser.add_argument(
        '-o',
        '--output',
        default='./data/processed/forecasting_data.csv',
        type=str,
        help='Output file path'
        )
    return parser


def forecasting_timeseries_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Group data by 'DATA' column, sum and count the values by 'VALOR_REEMBOLSADO'.
    :param data: DataFrame
    :return: DataFrame
    """
    data['DATA'] = pd.to_datetime(data['DATA'])

    # Group data by 'DATA' column, sum and count the values by 'VALOR_REEMBOLSADO'
    data = data.groupby('DATA')['VALOR_REEMBOLSADO'].agg(['sum', 'count']).reset_index()
    data.columns = ['DATA', 'VALOR_REEMBOLSADO', 'COUNT']

    data = data.sort_values('DATA')
    return data


def _main():
    # Parse arguments
    parser = _create_argparse()
    args = parser.parse_args()

    # Read data
    print(f"Reading data from file {args.file_path}...")
    print(f"Encoding: {args.encoding}")
    print(f"Separator: {args.separator}")
    data = read_data(args.file_path, args.encoding, args.separator)

    # Data preparation
    print("Preparing data...")
    data = forecasting_timeseries_preparation(data)

    # Save data
    print(f"Saving data to {args.output}...")
    data.to_csv(args.output, index=False)

if __name__ == '__main__':
    _main()
