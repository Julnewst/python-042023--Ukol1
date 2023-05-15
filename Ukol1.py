import pandas as pd

# načtení dat
data = pd.read_csv('1976-2020-president.csv')
print(data.head(15))


# 1 Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()). Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby().

data['rank'] = data.groupby(['year', 'state'])['candidatevotes'].rank(method='min', ascending=False)

print(data)



# 2 Pro další analýzu jsou důležití pouze vítězové. Vytvoř novou tabulku, která bude obsahovat pouze vítěze voleb.

winners = data[data['rank'] == 1]
winners = winners.reset_index(drop=True)

# výpis výsledků
print(winners)


# 3 Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany ve dvou po sobě jdoucích letech.
winners['previous_winner_party'] = winners.groupby(['state'])['party_simplified'].shift(1)
winners = winners.sort_values(['state', 'year'])


# výpis vítězů s novým sloupcem previous_winner
print(winners)

# 4 Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana. Můžeš k tomu použít např. funkci numpy.where() nebo metodu apply().

import numpy as np

winners['change'] = np.where(winners['previous_winner_party'].fillna(winners['party_simplified']) == winners['party_simplified'], 0, 1)

# výpis výsledků
print(winners)

# 5 Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran. Zde je nápověda i s kódem. Abyste totiž mohli data sařadit, je nutné tabulku vytvořenou metodou groupby převést na klasickou tabulku. Použitím metody groupby vám totiž vznikne "groupovaná tabulka", která nejde řadit.

data_pivot = winners.groupby('state')['change'].sum()
data_pivot = pd.DataFrame(data_pivot)

# Seřadíme státy podle počtu změn vítězných stran
data_pivot = data_pivot.sort_values("change", ascending=False)


# Výpis výsledků
print(data_pivot.head(15))

# 5 Vytvoření sloupcového grafu

import matplotlib.pyplot as plt

# Popisky os a titulek grafu
data_pivot = data_pivot.iloc[:10]
data_pivot.plot(kind="bar")
plt.xlabel('State')
plt.ylabel('Number of Changes')
plt.title('Státy s nejčastější změnou vítězné strany')


# Zobrazení grafu
plt.show()

# Pro další část pracuj s tabulkou se dvěma nejúspěšnějšími kandidáty pro každý rok a stát (tj. s tabulkou, která oproti té minulé neobsahuje jen vítěze, ale i druhého v pořadí).
# Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí.

# Seřazení dat podle roku, státu a počtu hlasů
data = data.sort_values(['year', 'state', 'candidatevotes'], ascending=[True, True, False])

# Vytvoření nového sloupce second_candidate_votes
data['second_candidate_votes'] = data.groupby(['year', 'state'])['candidatevotes'].shift(-1)

print(data)
winners2 = data[data['rank'] == 1]

# Výpis výsledků
print(winners2.head(15))

# 1 vytvoření sloupce s absolutním rozdílem mezi vítězem a druhým v pořadí
winners2['margin'] = abs(winners2['candidatevotes'] - winners2['second_candidate_votes'])
winners2 = winners2.reset_index(drop=True)
print(winners2)


# 2 Přidání sloupce s relativním marginem
winners2['relative_margin'] = winners2['margin'] / winners2['totalvotes']
print(winners2)

# 3 Seřaď tabulku podle velikosti relativního marginu a zjisti, kdy a ve kterém státě byl výsledek voleb nejtěsnější.

# Seřazení tabulky podle relativního marginu
winners2 = winners2.sort_values(by='relative_margin')
print(winners2)
winners2.insert(0, 'Index', range(1, len(winners2) + 1))
print(winners2)

# Výběr řádku s nejnižší relativní marží
lowest_margin_row = winners2.loc[winners2['relative_margin'].idxmin()]

# Vypsání názvu státu a roku s nejnižší relativní marží
print('Stát s nejnižší relativní marží: ' + lowest_margin_row['state'])
print('Rok: ' + str(int(lowest_margin_row['year'])))
print(f"Nejmenší relativní rozdíl byl ve státě {lowest_margin_row['state']} v roce {lowest_margin_row['year']}.")




# 4 Vytvoř pivot tabulku, která zobrazí pro jednotlivé volební roky, kolik států přešlo od Republikánské strany k Demokratické straně, kolik států přešlo od Demokratické strany k Republikánské straně a kolik států volilo kandidáta stejné strany.



# nastavení podmínek pro vytvoření sloupce "swing"

winners.loc[:, 'swing'] = 'no swing'
winners.loc[winners['party_simplified'] == winners['previous_winner_party'], 'swing'] = 'no swing'
winners.loc[(winners['party_simplified'] != 'REPUBLICAN') & (winners['previous_winner_party'] == 'REPUBLICAN'), 'swing'] = 'To Dem'
winners.loc[(winners['party_simplified'] != 'DEMOCRAT') & (winners['previous_winner_party'] == 'DEMOCRAT'), 'swing'] = 'To Rep'
print(winners)


# Vytvoření pivot tabulky
pivot = pd.pivot_table(winners.dropna(subset=['previous_winner_party']), values='state', index='year', columns='swing', aggfunc=len, fill_value='NaN')
pivot = pivot.reindex(columns=['no swing', 'To Dem', 'To Rep'])





# Výpis výsledné tabulky
print(pivot)