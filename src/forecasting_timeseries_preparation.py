import numpy as np
import pandas as pd
import argparse
from statsmodels.tsa.stattools import adfuller
from utils.data_reading import read_data


__all__ = ["forecasting_timeseries_preparation", "is_stationary"]


def _create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Forecasting Time Series Preparation")
    parser.add_argument(
        "-i",
        "--file-path",
        default="./data/interim/data.csv",
        type=str,
        help="Input file path",
    )
    parser.add_argument(
        "-enc", "--encoding", type=str, default="utf-8", help="Encoding of the files"
    )
    parser.add_argument(
        "-sep", "--separator", type=str, default=",", help="Separator of the files"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./data/processed/forecasting_data.csv",
        type=str,
        help="Output file path",
    )
    return parser


def is_stationary(
    series: pd.Series, threshold: float = 0.05, print_results: bool = False
):
    """
    Check the stationarity of a timeseries data.
    :param series: Time Series data
    :param threshold: Threshold for comparing p-value
    :param print_results: Indicates if the results must be printed
    :return: Bool indicating if the data is stationary
    """
    stationarity: bool = False
    result = adfuller(series)

    if result[1] <= threshold and result[0] < 0 and result[4]["1%"] < [4]:
        stationarity = True

    if print_results:
        print("p-value: %f" % result[1])
        print("ADF Statistic: %f" % result[0])
        print("Critical Values:")
        for key, value in result[4].items():
            print("\t%s: %.3f" % (key, value))
        print(f"The TimeSeries is {'not ' if not stationarity else ''}stationary.")

    return stationarity


def _apply_stationarity_transformations(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply differencing and log transformation so the timeseries become stationary.
    :param data: Dataframe with the timeseries
    :return new_data: Dataframe updated
    """
    if is_stationary(data["VALOR_REEMBOLSADO"]):
        print('The original timeseries is stationary.')
        return data
    else:
        print(
            "The original data is not stationary, applying first differencing and log transformation."
        )
        # Apply differencing with the period equals to one
        data["VALOR_REEMBOLSADO_stationary"] = data["VALOR_REEMBOLSADO"].diff(periods=1)

        # Apply log transformation
        data["VALOR_REEMBOLSADO_stationary"] = np.log(data["VALOR_REEMBOLSADO"])

        if is_stationary(data["VALOR_REEMBOLSADO_stationary"]):
            print("The original timeseries needed to be transformed and it is saved in 'stationary' column.")
            return data
        else:
            print(
                "The timeseries is not stationary and transformations were not enough. A detailed analysis is required!"
            )
            return data


def forecasting_timeseries_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Group data by 'DATA' column, sum and count the values by 'VALOR_REEMBOLSADO'.
    :param data: DataFrame
    :return: DataFrame
    """
    data["DATA"] = pd.to_datetime(data["DATA"])

    # Group data by 'DATA' column, sum and count the values by 'VALOR_REEMBOLSADO'
    data = data.groupby("DATA")["VALOR_REEMBOLSADO"].agg(["sum", "count"]).reset_index()
    data.columns = ["DATA", "VALOR_REEMBOLSADO", "COUNT"]

    # Stationarity transformations
    data = _apply_stationarity_transformations(data)

    data = data.sort_values("DATA")
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


if __name__ == "__main__":
    _main()
