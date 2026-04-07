from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.config import ONE_WEEK_DATA_FILE, EDSS_COLUMN, MSSS_COLUMN


PLOT_OUTPUT_COLUMNS = [
    "Pyramidal",
    "Cerebellar",
    "Thronchioencephalic",
    "Sensitive",
    "Sphincteric",
    "Visual",
    "Mental",
    "Deambulation",
    "PM10",
    "PM25",
    "N02",
    "CO",
    "O3",
    "SO2",
    "PP",
    "QQ",
    "RR",
    "TG",
    "TN",
    "TX",
    "HU",
    "FG",
    "Age",
    "Relapse_number",
    "Sex",
]


LABELS = {
    "PM10": "Particulate Matter ≤ 10 microns (PM10)",
    "PM25": "Particulate Matter ≤ 2.5 microns (PM2.5)",
    "N02": "Nitrogen Dioxide (NO2)",
    "CO": "Carbon Monoxide (CO)",
    "O3": "Ozone (O3)",
    "SO2": "Sulfur Dioxide (SO2)",
    "PP": "Sea Level Pressure",
    "QQ": "Global Radiation",
    "RR": "Precipitation Sum",
    "TG": "Mean Temperature",
    "TN": "Minimum Temperature",
    "TX": "Maximum Temperature",
    "HU": "Humidity",
    "FG": "Wind Speed",
    "Age": "Age at visit",
    "Relapse_number": "Relapse number before visit",
}


def load_data(file_path: Path) -> pd.DataFrame:
    """Load dataset from CSV."""
    return pd.read_csv(file_path)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataset for visualization."""
    df = df.copy()

    df = df.rename(columns={EDSS_COLUMN: "EDSS"})
    df["State"] = df["EDSS"].apply(lambda x: 1 if x <= 1 else (2 if x <= 2.5 else 3))

    return df


def create_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str = MSSS_COLUMN,
    color_column: str = "Sex",
    size_column: str = MSSS_COLUMN,
) -> None:
    """Create and show a scatter plot."""
    figure = px.scatter(
        data_frame=df,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        trendline="ols",
        labels={x_column: LABELS.get(x_column, x_column), y_column: y_column},
        title=f"Relationship Between {x_column} and {y_column}",
    )
    figure.show()


def create_example_plots(df: pd.DataFrame) -> None:
    """Create a few key plots."""
    create_scatter_plot(df, "Sex")
    create_scatter_plot(df, "Relapse_number")
    create_scatter_plot(df, "Age")
    create_scatter_plot(df, "PM10")
    create_scatter_plot(df, "PM25")
    create_scatter_plot(df, "N02")
    create_scatter_plot(df, "CO")
    create_scatter_plot(df, "O3")
    create_scatter_plot(df, "SO2")


def create_3d_plot(df: pd.DataFrame) -> None:
    """Create and show a 3D scatter plot."""
    fig = px.scatter_3d(
        data_frame=df,
        x="N02",
        y="EDSS",
        z="Week",
        color="EDSS",
        title="Nitrogen Dioxide (NO2)",
    )
    fig.show()


def create_subplot_figure(df: pd.DataFrame) -> None:
    """Create a multi-panel subplot figure."""
    fig = make_subplots(
        rows=4,
        cols=2,
        column_widths=[0.6, 0.4],
        row_heights=[0.25, 0.25, 0.25, 0.25],
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "scatter"}],
        ],
        subplot_titles=[
            "PP",
            "Cerebellar",
            "Thronchioencephalic",
            "Sensitive",
            "Sphincteric",
            "Visual",
            "Mental",
            "Deambulation",
        ],
    )

    columns_and_positions = [
        ("PP", 1, 1),
        ("Cerebellar", 1, 2),
        ("Thronchioencephalic", 2, 1),
        ("Sensitive", 2, 2),
        ("Sphincteric", 3, 1),
        ("Visual", 3, 2),
        ("Mental", 4, 1),
        ("Deambulation", 4, 2),
    ]

    for column, row, col in columns_and_positions:
        fig.add_trace(
            go.Scatter(
                x=df[column],
                y=df[MSSS_COLUMN],
                mode="markers",
                marker=dict(
                    size=df[MSSS_COLUMN],
                    color=df["Sex"],
                    showscale=True,
                ),
            ),
            row=row,
            col=col,
        )

    fig.update_layout(
        height=800,
        width=800,
        title_text="Multiple Subplots with MSSS",
        showlegend=False,
    )

    fig.show()


def main() -> None:
    data = load_data(ONE_WEEK_DATA_FILE)
    data = prepare_data(data)

    print("Shape:", data.shape)
    print("\nMissing values:")
    print(data.isnull().sum())

    create_example_plots(data)
    create_3d_plot(data)
    create_subplot_figure(data)


if __name__ == "__main__":
    main()