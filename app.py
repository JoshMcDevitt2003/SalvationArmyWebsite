from flask import Flask, request, redirect, url_for, render_template, flash
import pandas as pd
import io
from datetime import datetime


app = Flask(__name__)

app.secret_key = 'HelloWorld'

def getStayRowArray(df,min, max):
    numrows, numcolumns = df.shape
    rowArray = []
    for row in range(numrows):
        if lengthOfStay(df.iat[row, 2], df.iat[row, 1]) >= min and lengthOfStay(df.iat[row, 2], df.iat[row, 1]) <= max:
            rowArray.append(row)
    return rowArray
def lengthOfStay(enrollmentDate, exitDate, dateFormat = "%m/%d/%Y"):
    date1 = datetime.strptime(enrollmentDate, dateFormat)
    date2 = datetime.strptime(exitDate, dateFormat)
    lengthOfStay = date1 - date2
    return lengthOfStay.days
def age(exitdate, birthdate, dateFormat = "%m/%d/%Y"):
    date1 = datetime.strptime(birthdate, dateFormat)
    date2 = datetime.strptime(exitdate, dateFormat)
    lengthOfStay = date2 - date1
    return lengthOfStay.days
def getAgeRowArray(df,min, max):
    numrows, numcolumns = df.shape
    rowArray = []
    for row in range(numrows):
        if age(df.iat[row, 2], df.iat[row, 7])/360 >= min and age(df.iat[row, 2], df.iat[row, 7])/360 <= max:
            rowArray.append(row)
    return rowArray
def getRecidRowArray(df, column_name):
    value_counts = df[column_name].value_counts()
    repeated_entries = value_counts[value_counts >= 2].index
    indices = [df[df[column_name] == entry].index[0] for entry in repeated_entries]
    return indices
def uniqueClients(df):
    return df["Unique ID"].nunique()
def generate_date_range(start_date_str, end_date_str):
    dates = pd.date_range(start=start_date_str, end=end_date_str, freq='D')
    return dates
def getDayArray(start, end):
    array = []
    for date in generate_date_range(start, end):
        array.append(date.strftime("%m/%d/%Y"))
    return array
def getEntryMetrics(df, start, end):
    numrows, numcolumns = df.shape
    array = []
    man= 0
    woman = 0

    for row in range(numrows):
        if df.at[row, "Enrollment Start Date"] in getDayArray(start, end):
            array.append(row)
    for index in array:
        if df.at[index, "Gender"] == "Man":
            man += 1
        if df.at[index, "Gender"] == "Woman":
            woman += 1
    report =  (
        f"The number of women that entered the shelter between the start and end dates: {woman}\n" 
        f"The number of men that entered the shelter between the start and end dates {man}\n"
    )
    return report
def getExitMetrics(df, start, end):
    numrows, numcolumns = df.shape
    array = []
    man= 0
    woman = 0

    for row in range(numrows):
        if df.at[row, "Enrollment Exit Date"] in getDayArray(start, end):
            array.append(row)
    for index in array:
        if df.at[index, "Gender"] == "Man":
            man += 1
        if df.at[index, "Gender"] == "Woman":
            woman += 1
    report =  (
        f"The number of women that exited the shelter between the start and end dates: {woman}\n" 
        f"The number of men that exited the shelter between the start and end dates {man}\n"
    )
    return report
df = None
graphJSON = {
    "data": [
        {
            "type": "pie",
            "labels": [],
            "values": []
        }
    ],
    "layout": {
        "title": {"text": "Graphed Data will Appear Here"}
    }
}

@app.route('/')
def index():
    report = "Data Metrics Will Appear Here!"
    return render_template('index.html', report=report, graphJSON=graphJSON)
@app.route('/page2')
def page2():
    report = "Data Metrics Will Appear Here!"
    return render_template('page2.html', report=report, graphJSON=graphJSON)

@app.route('/page3')
def page3():
    report = "Data Metrics Will Appear Here!"
    return render_template('page3.html', report=report, graphJSON=graphJSON)

@app.route('/page4')
def page4():
    report = "Data Metrics Will Appear Here!"
    return render_template('page4.html', report=report, graphJSON=graphJSON)

@app.route('/page5')
def page5():
    report ="Data Metrics Will Appear Here!"
    return render_template('page5.html', report=report, graphJSON=graphJSON)

@app.route('/page6')
def page6():
    return render_template('page6.html')


@app.route('/lengthOfStay', methods=['POST'])
def getStayExitMetrics():
    global df
    if not (df is None):
        min = int(request.form['min'])
        max = int(request.form['max'])
        NoInterview = 0
        Other = 0
        OnGoing = 0
        NotOnGoing = 0
        Place = 0
        Emergency = 0
        Deceased = 0
        Jail = 0
        Substance = 0
        Transitional = 0
        know = 0
        DataNotCollected = 0
        longTerm = 0
        staying = 0
        psych = 0
        hotel = 0
        hospital = 0
        owned = 0
        noAnswer = 0
        counter = 0
        rows = getStayRowArray(df, min, max)
        for row in rows:
            counter += 1
            if df.iat[row, 13] == "No exit interview completed":
                NoInterview += 1
            elif df.iat[row, 13] == "Other":
                Other += 1
            elif df.iat[row, 13] == "Rental by client, with ongoing housing subsidy":
                OnGoing += 1
            elif df.iat[row, 13] == "Rental by client, no ongoing housing subsidy":
                NotOnGoing += 1
            elif "Place" in df.iat[row, 13]:
                Place += 1
            elif "Emergency" in df.iat[row, 13]:
                Emergency += 1
            elif df.iat[row, 13] == "Deceased":
                Deceased += 1
            elif df.iat[row, 13] == "Jail, prison, or juvenile detention facility":
                Jail += 1
            elif df.iat[row, 13] == "Substance abuse treatment facility or detox center":
                Substance += 1
            elif df.iat[row, 13] == "Transitional housing for homeless persons (including homeless youth)":
                Transitional += 1
            elif df.iat[row, 13] =="Data not collected":
                DataNotCollected += 1
            elif df.iat[row,13] == "Client doesn't know":
                know += 1
            elif df.iat[row,13] == "Long-term care facility or nursing home":
                longTerm += 1
            elif "Staying" in df.iat[row,13]:
                staying += 1
            elif "Psychiatric" in df.iat[row,13]:
                psych += 1
            elif "Hotel" in df.iat[row,13]:
                hotel += 1
            elif "Hospital" in df.iat[row,13]:
                hospital += 1
            elif "Owned" in df.iat[row, 13]:
                owned += 1
            else:
                noAnswer += 1
        total = Place + hospital + psych + Substance + Deceased + staying + OnGoing + NotOnGoing + Emergency + hotel + Transitional + longTerm + owned + Jail
        if total != 0:
            report = (
                f"Length of stay range entered: {min} days to {max} days\n"
                f"The number of people that we do not have data on: {NoInterview + Other + know + DataNotCollected + noAnswer}\n"
                f"The number of people that we do have data on: {total}\n"
                f"The number (percentage) of people that are in place not meant for habitation: {Place} ({Place/total:.1%})\n"
                f"The number (percentage) of people in hospital, psychiatric facility, substance abuse facility: {hospital + psych + Substance} ({(hospital + psych + Substance)/total:.1%})\n"
                f"The number (percentage) of people deceased: {Deceased} ({Deceased/total:.1%})\n"
                f"The number (percentage) staying with friends or family: {staying} ({staying/total:.1%})\n"
                f"The number (percentage) of people in rental with and without ongoing subsidy: {OnGoing + NotOnGoing} ({(OnGoing + NotOnGoing)/total:.1%})\n"
                f"The number (percentage) of people that went to jail: {Jail} ({Jail/total:.1%})\n"
                f"The number (percentage) of people in Emergency shelter, transition housing, hotel, or long-term nursing home: {Emergency + hotel + Transitional + longTerm} ({(Emergency + hotel + Transitional + longTerm)/total: .1%})\n"
                f"The number (percentage) owned by client: {owned} ({owned/total:.1%})\n"
                f"**Note percentages calculated excluding those we do not have data on**"
            )

            localGraphJSON = {
            "data": [
                {
                    "type": "pie",
                    "labels": ['Place not meant for habitation','hospital,psychiatric facility, substance abuse facility', 'deceased','staying with friends/family', 'In rental', 'jail', 'emergency shelter, transition housing, hotel, or nursing home', 'owned by client'],
                    "values": [Place, hospital + psych + Substance, Deceased, staying, OnGoing + NotOnGoing, Jail, Emergency + hotel + Transitional + longTerm, owned]
                }
            ],
            "layout": {
                "title": {"text": "Length Of Stay Exit Metrics"}
            }
        }

            return render_template('page2.html',report=report, graphJSON=localGraphJSON)
        else:
            return render_template('page2.html', report = 'No data for clients within specified range', graphJSON=graphJSON)
    return render_template('page2.html', report='Please Upload File First', graphJSON=graphJSON)

@app.route('/upload', methods=['POST'])
def upload_file():
    global df
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.endswith('.csv'):
        # Read the CSV file into a DataFrame
        file_content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(file_content))
        
        message = 'Upload successful!'
        return render_template('page6.html', message=message)
    
    flash('Invalid file format')
    return redirect(url_for('Page 6'))

@app.route('/age', methods=['POST'])
def getAgeExitMetrics():
    global df
    if not (df is None):
        min = int(request.form['min'])
        max = int(request.form['max'])
        NoInterview = 0
        Other = 0
        OnGoing = 0
        NotOnGoing = 0
        Place = 0
        Emergency = 0
        Deceased = 0
        Jail = 0
        Substance = 0
        Transitional = 0
        know = 0
        DataNotCollected = 0
        longTerm = 0
        staying = 0
        psych = 0
        hotel = 0
        hospital = 0
        owned = 0
        noAnswer = 0
        counter = 0
        rows = getAgeRowArray(df, min, max)
        for row in rows:
            counter += 1
            if df.iat[row, 13] == "No exit interview completed":
                NoInterview += 1
            elif df.iat[row, 13] == "Other":
                Other += 1
            elif df.iat[row, 13] == "Rental by client, with ongoing housing subsidy":
                OnGoing += 1
            elif df.iat[row, 13] == "Rental by client, no ongoing housing subsidy":
                NotOnGoing += 1
            elif "Place" in df.iat[row, 13]:
                Place += 1
            elif "Emergency" in df.iat[row, 13]:
                Emergency += 1
            elif df.iat[row, 13] == "Deceased":
                Deceased += 1
            elif df.iat[row, 13] == "Jail, prison, or juvenile detention facility":
                Jail += 1
            elif df.iat[row, 13] == "Substance abuse treatment facility or detox center":
                Substance += 1
            elif df.iat[row, 13] == "Transitional housing for homeless persons (including homeless youth)":
                Transitional += 1
            elif df.iat[row, 13] =="Data not collected":
                DataNotCollected += 1
            elif df.iat[row,13] == "Client doesn't know":
                know += 1
            elif df.iat[row,13] == "Long-term care facility or nursing home":
                longTerm += 1
            elif "Staying" in df.iat[row,13]:
                staying += 1
            elif "Psychiatric" in df.iat[row,13]:
                psych += 1
            elif "Hotel" in df.iat[row,13]:
                hotel += 1
            elif "Hospital" in df.iat[row,13]:
                hospital += 1
            elif "Owned" in df.iat[row, 13]:
                owned += 1
            else:
                noAnswer += 1
        total = Place + hospital + psych + Substance + Deceased + staying + OnGoing + NotOnGoing + Emergency + hotel + Transitional + longTerm + owned + Jail
        if total != 0:
            report = (
                f"Age range entered:{min} years to {max} years\n"
                f"The number of people that we do not have data on: {NoInterview + Other + know + DataNotCollected + noAnswer}\n"
                f"The number of people that we do have data on: {total}\n"
                f"The number (percentage) of people that are in place not meant for habitation: {Place} ({Place/total:.1%})\n"
                f"The number (percentage) of people in hospital, psychiatric facility, substance abuse facility: {hospital + psych + Substance} ({(hospital + psych + Substance)/total:.1%})\n"
                f"The number (percentage) of people deceased: {Deceased} ({Deceased/total:.1%})\n"
                f"The number (percentage) staying with friends or family: {staying} ({staying/total:.1%})\n"
                f"The number (percentage) of people in rental with and without ongoing subsidy: {OnGoing + NotOnGoing} ({(OnGoing + NotOnGoing)/total:.1%})\n"
                f"The number (percentage) of people that went to jail: {Jail} ({Jail/total:.1%})\n"
                f"The number (percentage) of people in Emergency shelter, transition housing, hotel, or long-term nursing home: {Emergency + hotel + Transitional + longTerm} ({(Emergency + hotel + Transitional + longTerm)/total: .1%})\n"
                f"The number (percentage) owned by client: {owned} ({owned/total:.1%})\n"
                f"**Note percentages calculated excluding those we do not have data on**"
            )

            localGraphJSON = {
            "data": [
                {
                    "type": "pie",
                    "labels": ['Place not meant for habitation','hospital,psychiatric facility, substance abuse facility', 'deceased','staying with friends/family', 'In rental', 'jail', 'emergency shelter, transition housing, hotel, or nursing home', 'owned by client'],
                    "values": [Place, hospital + psych + Substance, Deceased, staying, OnGoing + NotOnGoing, Jail, Emergency + hotel + Transitional + longTerm, owned]
                }
            ],
            "layout": {
                "title": {"text": "Length Of Stay Exit Metrics"}
            }
        }

            return render_template('page3.html',report=report, graphJSON=localGraphJSON)
        else:
            return render_template('page3.html', report = 'No data for clients within specified range', graphJSON=graphJSON)
    return render_template('page3.html', report="Please Upload File First", graphJSON=graphJSON)

@app.route('/housing', methods=['POST'])
def getPeopleNotEnteringHousing():
    global df
    if not df is None:
        housing = 0
        noData = 0
        numrows, numcolumns = df.shape
        for row in range(numrows):
            if "interview" in df.at[row, "Destination"]:
                noData += 1
            if "housing" in df.at[row, "Destination"]:
                housing += 1
        noHousing = numrows - noData - housing
        percentage = round((housing/(numrows-noData))*100, 2)
        report = (
            f"The number of people we do not have data on: {noData}\n"
            f"The number of people we have data on: {housing + noHousing}\n"
            f"The number of people entering Housing : {housing}\n"
            f"The number of people not entering housing : {noHousing}\n"
            f"The percentage on people entering housing : {percentage} %\n"
            f"**Note percentage calculated excluding those we do not have data on"
        )

        localgraphJSON = {
        "data": [
            {
                "type": "pie",
                "labels": ["Entering Housing", "Not Entering Housing"],
                "values": [housing, noHousing]
            }
        ],
        "layout": {
            "title": {"text": "Housing Data Metrics"}
        }
    }
        return render_template('page4.html', report=report, graphJSON=localgraphJSON)
    return render_template('page4.html', report="Please Upload File First", graphJSON=graphJSON)

@app.route('/recid', methods=['POST'])
def getRecidMetrics():
    global df
    if not df is None:
        mentalHealth = 0
        substanceUse = 0
        week = 0
        weekToMonth = 0
        monthToYear = 0
        overYear = 0
        for row in getRecidRowArray(df, "Unique ID"):
            if df.iat[row,27] != "No":
                mentalHealth += 1
            if df.iat[row, 29] != "No":
                substanceUse += 1
            if lengthOfStay(df.iat[row, 2], df.iat[row, 1]) <= 7:
                week += 1
            if lengthOfStay(df.iat[row, 2], df.iat[row, 1]) <= 30 and lengthOfStay(df.iat[row, 2], df.iat[row, 1]) > 7:
                weekToMonth += 1
            if lengthOfStay(df.iat[row, 2], df.iat[row, 1]) <= 360 and lengthOfStay(df.iat[row, 2], df.iat[row, 1]) > 30:
                monthToYear += 1
            if lengthOfStay(df.iat[row, 2], df.iat[row, 1]) > 360:
                overYear += 1
        total = week + weekToMonth + monthToYear + overYear
        if total != 0:
            report = (
                f"The number of unique clients within data set: {uniqueClients(df)}\n"
                f"The total number of recidivists in data set: {total}\n"
                f"The number (percentage) of recidivists with mentalHealth problems: {mentalHealth} ({mentalHealth/total:.1%})\n"
                f"The number (percentage) of recidivists with SubstanceAbuse problems: {substanceUse} ({substanceUse/total:.1%})\n"
                f"The number (percentage) of recidivists that had a length of stay less than or equal to one week: {week} ({week/total:.1%})\n"
                f"The number (percentage) of recidivists that had a length of stay greater than one week but less than one year: {weekToMonth} ({weekToMonth/total:.1%})\n"
                f"The number (percentage) of recidivists that had a length of stay greater than one month but less than one year: {monthToYear} ({monthToYear/total:.1%})\n"
                f"The number (percentage) of recidivists that had a length of stay greater than one year: {overYear} ({overYear/total:.1%})\n"
                f"Percentage of clients that become recidivits: {(len(getRecidRowArray(df, 'Unique ID'))/uniqueClients(df)):.1%}\n"
            )

            localGraphJSON = {
            "data": [
                {
                    "type": "pie",
                    "labels": ['recidivists that had a length of stay less than or equal to one week', 'recidivists that had a length of stay greater than one week but less than one year', 'recidivists that had a length of stay greater than one month but less than one year', 'recidivists that had a length of stay greater than one year'],
                    "values": [week, weekToMonth, monthToYear,overYear]
                }
            ],
            "layout": {
                "title": {"text": "Recidivist Metrics"}
            }
        }
            return render_template('page5.html', report=report, graphJSON=localGraphJSON)
        else: 
            return render_template('page5.html', report = 'No data for people within specified range', graphJSON=graphJSON)
    return render_template('page5.html', report="Please Upload File First", graphJSON=graphJSON)

@app.route('/averageEntries', methods=['POST'])
def getAverageEnteriesPerDay():
    global df
    if not (df is None):
        start = request.form.get('min')
        end = request.form.get('max')
        clientsperdate = df['Enrollment Start Date'].value_counts()
        counts_array = [clientsperdate.get(date, 0) for date in getDayArray(start, end)]
        clientsperdateExit = df['Enrollment Exit Date'].value_counts()
        counts_array2 = [clientsperdateExit.get(date, 0) for date in getDayArray(start, end)]
        exits = round(sum(counts_array2)/len(counts_array2),2)
        numrows, numcolumns = df.shape
        twenty = 0
        thirty = 0
        fourty = 0
        fifty = 0
        sixty = 0
        overSixty = 0
        array = []
        for row in range(numrows):
            if df.iat[row,1] in getDayArray(start,end):
                array.append(age(df.iat[row,2], df.iat[row,7])/360)
        for entry in array:
            if entry <= 20:
                twenty += 1
            elif 20 < entry <= 30:
                thirty += 1
            elif 30 < entry <= 40:
                fourty += 1
            elif 40 < entry <= 50:
                fifty += 1
            elif 50 < entry <= 60:
                sixty += 1
            elif entry > 60:
                overSixty += 1
        report = (
        f"Date range entered: {start} - {end}\n"
        f"The Average Number of entries per day within the specified range is: {round(sum(counts_array)/len(counts_array),2)}\n"
        f"{getEntryMetrics(df, start, end)}\n"
        f"The Average Number of exits per day within the specified range is: {(exits)}\n"
        f"{getExitMetrics(df, start, end)}"
        )

        localGraphJSON = {
            "data": [
                {
                    "type": "bar",
                    "x": ['0-20',', 21-30', '31-40','41-50', '51-60', '61+'],
                    "y": [twenty,thirty,fourty,fifty,sixty,overSixty]
                }
            ],
            "layout": {
                "title": {"text": "Number of entries in specified data range per age group"}
            }
        }

        return render_template('index.html', report=report, graphJSON=localGraphJSON)
    return render_template('index.html', report = 'Please Upload a File First', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)