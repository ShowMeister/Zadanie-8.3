import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url_shootings = 'https://uploads.kodilla.com/bootcamp/pro-data-visualization/files/fatal-police-shootings-data.csv'
df = pd.read_csv(url_shootings)

print("Podstawowe informacje o danych:")
print(df.info())
print("\nPierwsze wiersze:")
print(df.head())

print("\n" + "="*80)
print("1. ZESTAWIENIE WEDŁUG RASY I CHOROBY PSYCHICZNEJ")
print("="*80)

pivot_table = pd.crosstab(df['race'], df['signs_of_mental_illness'], margins=True)
print(pivot_table)

print("\n" + "="*80)
print("2. ODSETEK OFIAR Z CHOROBĄ PSYCHICZNĄ DLA KAŻDEJ RASY")
print("="*80)

race_mental = df.groupby('race')['signs_of_mental_illness'].apply(
    lambda x: (x == True).sum() / len(x) * 100
).sort_values(ascending=False)

print("\nOdsetek ofiar z chorobą psychiczną według rasy:")
for race, percent in race_mental.items():
    print(f"{race}: {percent:.2f}%")

print(f"\nRasa z największym odsetkiem choroby psychicznej: {race_mental.index[0]} ({race_mental.iloc[0]:.2f}%)")

print("\n" + "="*80)
print("3. ANALIZA WEDŁUG DNI TYGODNIA")
print("="*80)

df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.day_name()

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = df['day_of_week'].value_counts().reindex(days_order)

print("\nLiczba interwencji według dnia tygodnia:")
print(day_counts)

plt.figure(figsize=(12, 6))
plt.bar(range(len(days_order)), day_counts.values, color='steelblue')
plt.xlabel('Dzień tygodnia', fontsize=12)
plt.ylabel('Liczba interwencji', fontsize=12)
plt.title('Liczba śmiertelnych interwencji policji według dnia tygodnia', fontsize=14)
plt.xticks(range(len(days_order)), ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Nie'])
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('interwencje_dni_tygodnia.png', dpi=300, bbox_inches='tight')
print("\nWykres zapisany jako: interwencje_dni_tygodnia.png")

print("\n" + "="*80)
print("4. ANALIZA WEDŁUG STANÓW (na 1000 mieszkańców)")
print("="*80)

state_population = {
    'CA': 39538223, 'TX': 29145505, 'FL': 21538187, 'NY': 20201249, 'PA': 13002700,
    'IL': 12812508, 'OH': 11799448, 'GA': 10711908, 'NC': 10439388, 'MI': 10077331,
    'NJ': 9288994, 'VA': 8631393, 'WA': 7705281, 'AZ': 7151502, 'MA': 7029917,
    'TN': 6910840, 'IN': 6785528, 'MO': 6154913, 'MD': 6177224, 'WI': 5893718,
    'CO': 5773714, 'MN': 5706494, 'SC': 5118425, 'AL': 5024279, 'LA': 4657757,
    'KY': 4505836, 'OR': 4237256, 'OK': 3959353, 'CT': 3605944, 'UT': 3271616,
    'IA': 3190369, 'NV': 3104614, 'AR': 3011524, 'MS': 2961279, 'KS': 2937880,
    'NM': 2117522, 'NE': 1961504, 'WV': 1793716, 'ID': 1839106, 'HI': 1455271,
    'NH': 1377529, 'ME': 1362359, 'MT': 1084225, 'RI': 1097379, 'DE': 989948,
    'SD': 886667, 'ND': 779094, 'AK': 733391, 'DC': 689545, 'VT': 643077, 'WY': 576851
}

state_incidents = df['state'].value_counts()

incidents_per_1000 = pd.DataFrame({
    'incidents': state_incidents,
    'population': pd.Series(state_population)
})
incidents_per_1000 = incidents_per_1000.dropna()
incidents_per_1000['per_1000'] = (incidents_per_1000['incidents'] / incidents_per_1000['population']) * 1000

incidents_per_1000 = incidents_per_1000.sort_values('per_1000', ascending=False)

print("\nTop 10 stanów z największą liczbą incydentów na 1000 mieszkańców:")
print(incidents_per_1000.head(10)[['incidents', 'population', 'per_1000']])

print("\n" + "="*80)
print("PODSUMOWANIE ANALIZY")
print("="*80)
print(f"Całkowita liczba incydentów: {len(df)}")
print(f"Rasa z największym odsetkiem choroby psychicznej: {race_mental.index[0]} ({race_mental.iloc[0]:.2f}%)")
print(f"Dzień tygodnia z największą liczbą incydentów: {day_counts.index[day_counts.argmax()]}")
print(f"Stan z największą liczbą incydentów na 1000 mieszkańców: {incidents_per_1000.index[0]} ({incidents_per_1000.iloc[0]['per_1000']:.4f})")

# Zapisz wyniki do CSV
incidents_per_1000.to_csv('incydenty_na_1000_mieszkancow.csv')
print("\nWyniki zapisane do: incydenty_na_1000_mieszkancow.csv")
