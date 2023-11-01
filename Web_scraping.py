def web_scrapper():
    print("Executing scraping population data from wikipedia........")
    from bs4 import BeautifulSoup
    import pandas as pd
    import requests
    import sqlite3

    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")

        # Try to find the table by searching for a specific caption
        table = soup.find("table", {"class": "wikitable"})
        header = table.find_all("th")

        column_names = [th.get_text(strip=True).replace('–', '').replace('\xa0', ' ').strip() for th in header if th.get_text(strip=True) != '' and not th.get_text(strip=True).isnumeric()]
        Headings = [item for item in column_names if item != '']
        print(Headings)
        Population_df = pd.DataFrame(columns=Headings)
        #print(Population_df)
        observations = table.find_all("tr")
        for i in observations[1:]:
            data = i.find_all("td")
            row_data = [column.get_text(strip=True) for column in data]
            row_data.pop()
            data.append(row_data)
            if len(row_data) == len(Headings):
                new_row = dict(zip(Headings, row_data))
                Population_df = pd.concat([Population_df, pd.DataFrame([new_row])], ignore_index=True)
        Population_df = Population_df.iloc[1:]
        # Remove commas from the "Population" column
        Population_df['Population'] = Population_df['Population'].str.replace(',', '', regex=True)

        # Convert the "Population" column to int
        Population_df['Population'] = Population_df['Population'].astype(int)

        # Remove % from the "% ofworld" column
        Population_df['% ofworld'] = Population_df['% ofworld'].str.replace('%', '', regex=True)

        # Convert the "Population" column to int
        Population_df['% ofworld'] = Population_df['% ofworld'].astype(float)


        #print(Population_df)
        #print(Population_df.columns)

    else:
        print("Failed to retrieve the webpage. Status code:", r.status_code)


    #inserting dataframe into sqlite database

    connetion = sqlite3.connect("population.db")
    Population_df.to_sql('total_population', connetion,if_exists='replace')
    connetion.commit()


    # # Create a cursor object to execute SQL commands
    # cursor = connetion.cursor()
    # cursor.execute("SELECT * FROM total_population")


    # result = cursor.fetchall()
    # #printing the table data
    # for i in result:
    #     print(i)

    # # Get the column names from the cursor's description attribute
    # column_total_poulations = [description[0] for description in cursor.description]

    # # Printing the column names
    # print(column_total_poulations)

    # cursor.execute("PRAGMA table_info(total_population)")

    # # Fetch the result and get the column names and data types
    # table_info = cursor.fetchall()

    # # Iterate through the result to print the column names and data types
    # for column_info in table_info:
    #     column_name = column_info[1]
    #     data_type = column_info[2]
    #     print(f"Column: {column_name}, Data Type: {data_type}")
    connetion.close()

if __name__ == "__main__":
    print("Web scraping Independandly executed")