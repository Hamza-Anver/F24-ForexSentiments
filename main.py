import os
import pandas as pd
import plotly.graph_objs as go


sentiments_dir = "data/sentiments.csv"
forex_dir = "data/forex_rates.csv"


def main():
    # Check if the files exist
    if not (os.path.exists(sentiments_dir) and os.path.exists(forex_dir)):
        print("Data files do not exist.")
        return

    # Combine the data
    pd_sentiments = pd.read_csv(sentiments_dir)
    pd_forex = pd.read_csv(forex_dir)

    # Change header of forex data 'Date' to 'date'
    pd_forex.rename(columns={"Date": "date"}, inplace=True)

    # Average buy and sell to spot rate
    pd_forex["spot_lkr_usd"] = (
        pd_forex["Buy Rate (LKR)"] + pd_forex["Sell Rate (LKR)"]
    ) / 2
    # Drop the buying and selling rate columns
    pd_forex.drop(columns=["Buy Rate (LKR)", "Sell Rate (LKR)"], inplace=True)

    # Merge the data
    merged = pd.merge(pd_sentiments, pd_forex, on="date")

    # Sort by date
    merged.sort_values("date", inplace=True)

    # Save the data
    merged.to_csv("data/combined_data.csv", index=False)

    merged_smooth = merged.copy()

    # Smoothen the sentiment and spot rate data
    merged_smooth["sentiment"] = merged["sentiment"].rolling(window=7).mean()
    merged_smooth["spot_lkr_usd"] = merged["spot_lkr_usd"].rolling(window=15).mean()

    # Plot the data
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=merged_smooth["date"],
            y=merged_smooth["sentiment"],
            name="Sentiment (Smooth)",
            yaxis="y1",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged_smooth["date"],
            y=merged_smooth["spot_lkr_usd"],
            name="Spot Rate (Smooth)",
            yaxis="y2",
        )
    )

    # Hide these by default
    fig.add_trace(
        go.Scatter(
            x=merged["date"],
            y=merged["sentiment"],
            name="Sentiment",
            yaxis="y1",
            visible="legendonly",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged["date"],
            y=merged["spot_lkr_usd"],
            name="Spot Rate",
            yaxis="y2",
            visible="legendonly",
        )
    )

    fig.update_layout(
        title="Sentiment vs Spot Rate",
        xaxis_title="Date",
        yaxis_title="Sentiment",
        yaxis2=dict(title="Spot Rate", overlaying="y", side="right"),
    )

    # Save to html file
    fig.write_html("index.html")

if __name__ == "__main__":
    main()
