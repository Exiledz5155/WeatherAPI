from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

stations = pd.read_csv("data/stations.txt", skiprows = 17)
stations = stations[["STAID", "STANAME                                 "]]
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>") # arrows allow for value to be placed
def about(station, date):
    # Creating the filename
    filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    # Reading the csv, skipping metadata and converting the Date string data to data time type data
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20) # Keep the date as basic data (int or string)
    df["    DATE"] = df["    DATE"].astype(str) # Convert all to string
    # Convert year to string, assigning the correct yearly data, and formatting the data
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result



if __name__ == "__main__":
    app.run(debug=True, port=5000) # change port if running multiple apps
