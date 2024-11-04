# Importiamo le librerie necessarie
import streamlit as st  # Streamlit per creare l'interfaccia web
import pandas as pd     # Pandas per gestire i dati in formato tabellare
import numpy as np      # Numpy per operazioni numeriche avanzate
import matplotlib.pyplot as plt  # Matplotlib per creare grafici

# Impostiamo il titolo dell'applicazione
st.title('Dashboard Raccolta Olive - Torre Oliva Molfetta')

# Descriviamo brevemente l'applicazione
st.write("""
Benvenuto nella dashboard interattiva per la raccolta delle olive del brand **Torre Oliva Molfetta**.

Questa applicazione permette di inserire, visualizzare e analizzare i dati della raccolta delle olive a partire dall'anno 2000. Potrai vedere statistiche dettagliate e grafici comparativi tra diversi anni.
""")

# Sezione per l'inserimento dei dati
st.header('Inserimento Dati Raccolta')

# Creiamo o carichiamo un DataFrame vuoto o esistente
# Proviamo a caricare i dati esistenti da un file CSV (se esiste)
@st.cache_data  # Cache dei dati per migliorare le prestazioni
def load_data():
    try:
        # Cerchiamo di leggere un file CSV esistente
        df = pd.read_csv('dati_raccolta_olive.csv', parse_dates=['Data raccolta olive', 'Data molitura olive'])
    except FileNotFoundError:
        # Se il file non esiste, creiamo un DataFrame vuoto con le colonne necessarie
        df = pd.DataFrame(columns=[
            'Anno',
            'Data raccolta olive',
            'Data molitura olive',
            'N° bidone 30 kg',
            'N° bidone 12 kg',
            'N° bidone 10 kg',
            'N° lattina 5 litri',
            'N° lattina 3 litri',
            'N° lattina 2 litri',
            'N° lattina 1 litro',
            'Costo contadino totale',
            'Costo molitura totale',
            'Costo molitura quintale',
            'Kg olive totale'
        ])
    return df

# Carichiamo il DataFrame
df = load_data()

# Funzione per convertire stringhe di data in oggetti datetime
def convert_to_date(date_str):
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT

# Creiamo un modulo per inserire nuovi dati
with st.form('Inserimento nuovi dati'):
    # Input per l'anno di riferimento
    anno = st.number_input('Anno', min_value=2000, max_value=2100, step=1, value=2023)
    # Input per le date, convertite in formato data
    data_raccolta = st.text_input('Data raccolta olive (AAAA-MM-GG)', value='2023-10-01')
    data_molitura = st.text_input('Data molitura olive (AAAA-MM-GG)', value='2023-10-05')
    # Input per il numero di bidoni e lattine
    num_bidone_30kg = st.number_input('N° bidone 30 kg', min_value=0, step=1, value=0)
    num_bidone_12kg = st.number_input('N° bidone 12 kg', min_value=0, step=1, value=0)
    num_bidone_10kg = st.number_input('N° bidone 10 kg', min_value=0, step=1, value=0)
    num_lattina_5l = st.number_input('N° lattina 5 litri', min_value=0, step=1, value=0)
    num_lattina_3l = st.number_input('N° lattina 3 litri', min_value=0, step=1, value=0)
    num_lattina_2l = st.number_input('N° lattina 2 litri', min_value=0, step=1, value=0)
    num_lattina_1l = st.number_input('N° lattina 1 litro', min_value=0, step=1, value=0)
    # Input per i costi
    costo_contadino = st.number_input('Costo contadino totale (€)', min_value=0.0, step=0.01, value=0.0)
    costo_molitura_totale = st.number_input('Costo molitura totale (€)', min_value=0.0, step=0.01, value=0.0)
    costo_molitura_quintale = st.number_input('Costo molitura per quintale (€)', min_value=0.0, step=0.01, value=0.0)
    kg_olive_totale = st.number_input('Kg olive totale', min_value=0.0, step=0.1, value=0.0)
    # Pulsante per inviare i dati
    submitted = st.form_submit_button('Aggiungi Dati')

    if submitted:
        # Convertiamo le date in formato datetime
        data_raccolta_dt = convert_to_date(data_raccolta)
        data_molitura_dt = convert_to_date(data_molitura)
        # Controlliamo se le date sono valide
        if pd.isna(data_raccolta_dt) or pd.isna(data_molitura_dt):
            st.error('Per favore inserisci le date in formato corretto (AAAA-MM-GG).')
        else:
            # Creiamo un nuovo record con i dati inseriti
            new_data = {
                'Anno': anno,
                'Data raccolta olive': data_raccolta_dt,
                'Data molitura olive': data_molitura_dt,
                'N° bidone 30 kg': num_bidone_30kg,
                'N° bidone 12 kg': num_bidone_12kg,
                'N° bidone 10 kg': num_bidone_10kg,
                'N° lattina 5 litri': num_lattina_5l,
                'N° lattina 3 litri': num_lattina_3l,
                'N° lattina 2 litri': num_lattina_2l,
                'N° lattina 1 litro': num_lattina_1l,
                'Costo contadino totale': costo_contadino,
                'Costo molitura totale': costo_molitura_totale,
                'Costo molitura quintale': costo_molitura_quintale,
                'Kg olive totale': kg_olive_totale
            }
            # A partire da Pandas 2.0, df.append() è stato deprecato e rimosso.
            # Utilizziamo pd.concat() per aggiungere un nuovo record al DataFrame.
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            # Salviamo i dati aggiornati in un file CSV
            df.to_csv('dati_raccolta_olive.csv', index=False)
            st.success('Dati aggiunti con successo!')

# Visualizziamo i dati attuali
st.header('Dati Attuali')
st.dataframe(df)

# Eseguiamo i calcoli necessari
st.header('Calcoli e Statistiche')

# Definiamo le tare dei contenitori (peso dei contenitori vuoti)
tare = {
    'bidone_30kg': 3.70,
    'bidone_12kg': 1.75,
    'bidone_10kg': 1.95,
    'lattina_5l': 0.400,
    'lattina_3l': 0.268,
    'lattina_2l': 0.221,
    'lattina_1l': 0.200
}

# Calcoliamo il totale kg olio considerando le tare
def calcola_totale_kg_olio(row):
    # Calcoliamo il peso netto per ogni tipo di contenitore
    peso_netto = (
        (row['N° bidone 30 kg'] * (30 - tare['bidone_30kg'])) +
        (row['N° bidone 12 kg'] * (12 - tare['bidone_12kg'])) +
        (row['N° bidone 10 kg'] * (10 - tare['bidone_10kg'])) +
        (row['N° lattina 5 litri'] * (5 * 0.916 - tare['lattina_5l'])) +
        (row['N° lattina 3 litri'] * (3 * 0.916 - tare['lattina_3l'])) +
        (row['N° lattina 2 litri'] * (2 * 0.916 - tare['lattina_2l'])) +
        (row['N° lattina 1 litro'] * (1 * 0.916 - tare['lattina_1l']))
    )
    return peso_netto

# Applichiamo la funzione al DataFrame per ottenere il totale kg olio
df['Totale kg olio'] = df.apply(calcola_totale_kg_olio, axis=1)

# Calcoliamo il totale litri olio convertendo i kg in litri
# Densità media dell'olio d'oliva: circa 0.916 kg/l
df['Totale litri olio'] = df['Totale kg olio'] / 0.916

# Calcoliamo la resa % (Totale kg olio / Kg olive totale * 100)
df['Resa %'] = (df['Totale kg olio'] / df['Kg olive totale']) * 100

# Visualizziamo le nuove colonne calcolate
st.write('Dati con calcoli aggiunti:')
st.dataframe(df[['Anno', 'Totale kg olio', 'Totale litri olio', 'Resa %']])

# Sezione per i grafici dinamici
st.header('Grafici Comparativi')

# Selezione degli anni per il confronto
anni_disponibili = sorted(df['Anno'].unique())
anni_selezionati = st.multiselect(
    'Seleziona gli anni da confrontare:',
    options=anni_disponibili,
    default=anni_disponibili[-2:] if len(anni_disponibili) >= 2 else anni_disponibili
)

# Verifichiamo che siano stati selezionati degli anni
if anni_selezionati:
    # Filtriamo i dati in base agli anni selezionati
    df_filtrato = df[df['Anno'].isin(anni_selezionati)]

    # Grafico comparativo del totale olio e kg olive per anno
    st.subheader('Totale Olio e Kg Olive per Anno')
    fig, ax1 = plt.subplots()

    # Creiamo un grafico a barre per il totale kg olio
    ax1.bar(df_filtrato['Anno'], df_filtrato['Totale kg olio'], color='green', label='Totale kg olio')
    ax1.set_xlabel('Anno')
    ax1.set_ylabel('Totale kg olio', color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    # Creiamo un secondo asse per il kg olive totale
    ax2 = ax1.twinx()
    ax2.plot(df_filtrato['Anno'], df_filtrato['Kg olive totale'], color='blue', marker='o', label='Kg olive totale')
    ax2.set_ylabel('Kg olive totale', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Aggiungiamo una legenda e il titolo
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    st.pyplot(fig)

    # Grafico comparativo dei costi per anno
    st.subheader('Confronto dei Costi per Anno')
    # Selezioniamo i costi da confrontare
    costi = ['Costo contadino totale', 'Costo molitura totale', 'Costo molitura quintale']
    df_costi = df_filtrato[['Anno'] + costi]

    # Raggruppiamo per anno e sommiamo i costi (nel caso ci siano più record per anno)
    df_costi_aggregati = df_costi.groupby('Anno').sum().reset_index()

    # Creiamo un grafico a barre per i costi
    fig2, ax = plt.subplots()
    indice = np.arange(len(df_costi_aggregati['Anno']))
    larghezza = 0.2  # Larghezza delle barre

    # Posizioni per le barre
    posizioni = [indice - larghezza, indice, indice + larghezza]
    colori = ['red', 'orange', 'purple']

    # Per ogni tipo di costo, creiamo una serie di barre
    for i, costo in enumerate(costi):
        ax.bar(posizioni[i], df_costi_aggregati[costo], width=larghezza, label=costo, color=colori[i])

    ax.set_xticks(indice)
    ax.set_xticklabels(df_costi_aggregati['Anno'])
    ax.set_xlabel('Anno')
    ax.set_ylabel('Costo (€)')
    ax.legend()
    st.pyplot(fig2)

else:
    st.warning('Per favore seleziona almeno un anno per visualizzare i grafici.')

# Messaggio finale
st.write("""
Speriamo che questa dashboard ti aiuti a gestire e analizzare efficacemente i dati della raccolta delle olive.

Puoi continuare ad aggiungere nuovi dati e a esplorare le statistiche aggiornate.
""")
