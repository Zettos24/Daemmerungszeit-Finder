import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# Funktion zum Umwandeln der Daten
def convert_to_date(month_mapping, date_str):
    # Trenne den Monat und Tag von der Wochentagsabkürzung
    parts = date_str.split()
    month_str = parts[0]  # Monat (z.B. "Jan.")
    day_str = parts[1]    # Tag (z.B. "3")
    
    # Monat und Tag in ein korrektes Format bringen
    month = month_mapping.get(month_str, '01')  # Standard auf "01" setzen, falls nicht gefunden
    day = day_str.zfill(2)  # Tag auf 2 Stellen auffüllen (z.B. "03")
    
    # Das Jahr hinzufügen (2025)
    year = '2025'
    
    # Datum als String im Format "YYYY-MM-DD" zusammenbauen
    return f"{year}-{month}-{day}"


def get_data_for_date(tag, monat):
    result = df[(df['datum'].dt.day == tag) & (df['datum'].dt.month == monat)]
    return result

# Streamlit Web-App
def run_app():
    st.title("Dämmerungszeit Finder")
    
    # Benutzerinteraktion: Tag und Monat auswählen
    tag = st.number_input("Tag:", min_value=1, max_value=31, value=1)
    monat = st.number_input("Monat:", min_value=1, max_value=12, value=1)
    
    # Ergebnisse anzeigen
    result = get_data_for_date(tag, monat)
    
    if not result.empty:
        st.write(f"Ergebnisse für den {tag:02d}.{monat:02d}:")
        st.dataframe(result)
    else:
        st.write("Keine Daten für das angegebene Datum gefunden.")



def reinigeDF(df):
    month_mapping = {
        'Jan.': '01', 'Feb.': '02', 'Mrz.': '03', 'Apr.': '04',
        'Mai': '05', 'Juni': '06', 'Juli': '07', 'Aug.': '08',
        'Sep.': '09', 'Okt.': '10', 'Nov.': '11', 'Dez.': '12'
    }


    for column in df.columns:
        if column != 'datum':
            df[column] = df[column].astype(str)
            df[column] = df[column].replace('////', None)
            df[column] = df[column].apply(lambda x: (':'.join([i.zfill(2) for i in x.split()])) if x is not None else None)
        else:
            df[column] = df[column].apply(lambda x: convert_to_date(month_mapping, x))
            df[column] = pd.to_datetime(df[column])


# Die App ausführen
if __name__ == "__main__":
    df = pd.read_excel('data/Ephemeriden-Daten 2025.xlsx')
    df.head()
    reinigeDF(df)
    run_app()