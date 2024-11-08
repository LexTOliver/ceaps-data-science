import argparse
from datetime import datetime
from neuralprophet import NeuralProphet, set_log_level
import os
import pandas as pd
import plotly.io as pio
import pickle


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--data_path",
        type=str,
        default="./data/processed/forecasting_data.csv",
        help="Path to the CSV data.",
    )
    parser.add_argument(
        "-o",
        "--output_model",
        type=str,
        default=f"./models/neuralprophet-{datetime.now().strftime('%Y%m%d-%H%M%S')}/",
        help="Directory path to save the model.",
    )
    parser.add_argument(
        "-m",
        "--output_metrics",
        type=str,
        default="./reports/figures/",
        help="Directory path to save the metrics.",
    )
    return parser


def _save_prediction(model, metrics, output_path: str) -> None:
    """
    Save the metrics of the model.
    :param model: NeuralProphet
    :param metrics: dict
    :param output_path: str
    :return: None
    """
    print(output_path)
    if os.path.isfile(output_path):
        raise ValueError("Output path must be a directory.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(
        output_path,
        f"neuralprophet_prediction{datetime.now().strftime('%Y%m%d-%H%M%S')}.png",
    )

    # Plotting the metrics
    fig = model.plot(metrics)
    
    pio.write_image(fig, output_file)


def _save_model(model, metrics, output_path: str) -> None:
    """
    Save the model and its metrics.
    :param model: NeuralProphet
    :param metrics: Metrics DataFrame
    :param output_path: str
    :return: None
    :raises: ValueError
    """
    if os.path.isfile(output_path):
        raise ValueError("Output path must be a directory.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_model = os.path.join(output_path, "neuralprophet_model.pkl")
    output_metrics = os.path.join(output_path, "neuralprophet_metrics.csv")

    with open(output_model, "wb") as f:
        pickle.dump(model, f)

    metrics.to_csv(output_metrics, index=False)


def train_neural_prophet(
    data: pd.DataFrame, output_model: str, output_metrics: str
) -> None:
    """
    Train the Neural Prophet model.
    :param data: pd.DataFrame
    :param output_model: str
    :param output_metrics: str
    :return: None
    """
    # Train the model
    model = NeuralProphet(
        # n_changepoints=0,   # Trend changepoints
        # yearly_seasonality=True,
        # monthly_seasonality=True,
        # weekly_seasonality=False,
        # daily_seasonality=False,
    )
    model.set_plotting_backend("plotly-static")
    metrics = model.fit(data, freq="D")

    # Forecasting
    # future = model.make_future_dataframe(data, periods=365)
    # forecast = model.predict(future)

    # Saves
    _save_model(model, metrics, output_model)
    # _save_prediction(
    #     model, forecast, output_metrics
    # )         # FIXME: Not working, need to fix


def main():
    set_log_level()

    parser = create_argparser()
    args = parser.parse_args()

    data = pd.read_csv(args.data_path)
    data["X"] = pd.to_datetime(data["X"])
    data = data.rename(columns={"X": "ds"})
    data = data[["ds", "y"]]

    train_neural_prophet(data, args.output_model, args.output_metrics)


if __name__ == "__main__":
    main()
