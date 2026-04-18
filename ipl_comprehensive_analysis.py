import pandas as pd
import numpy as np

# ==========================================
# 1. DATA EXTRACTION & CLEANING
# ==========================================
print("Loading and cleaning IPL dataset...")
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# Handle missing data and align primary keys
deliveries['player_dismissed'] = deliveries['player_dismissed'].fillna('No wicket')
matches.rename(columns={'id': 'match_id'}, inplace=True)

# Merge datasets
df = pd.merge(matches, deliveries, on='match_id')
print(f"✅ Data Successfully Merged! Total deliveries analyzed: {len(df):,}\n")

# ==========================================
# 2. BATTING MASTERCLASS
# ==========================================
print("🏆 TOP 5 RUN SCORERS IN IPL HISTORY")
top_batsman = df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5)
print(top_batsman.to_string(), "\n")

print("💥 MOST SIXES HIT")
sixes_data = df[df['batsman_runs'] == 6]
top_six_hitters = sixes_data.groupby('batter')['batsman_runs'].count().sort_values(ascending=False).head(5)
print(top_six_hitters.to_string(), "\n")

print("🏏 MOST FOURS HIT")
four_stats = df[df['batsman_runs'] == 4]
most_fours = four_stats.groupby('batter')['batsman_runs'].count().sort_values(ascending=False).head(5)
print(most_fours.to_string(), "\n")

print("🦆 MOST DUCKS (0 RUNS)")
match_score = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
true_ducks = match_score[match_score['batsman_runs'] == 0]
most_ducks = true_ducks['batter'].value_counts().head(5)
print(most_ducks.to_string(), "\n")

# ==========================================
# 3. FIELDING & BOWLING RECORDS
# ==========================================
print("🎯 TOP 5 WICKET-TAKERS")
bowler_wickets = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wickets']
true_wickets = df[df['dismissal_kind'].isin(bowler_wickets)]
top_bowlers = true_wickets.groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(5)
print(top_bowlers.to_string(), "\n")

print("🧤 MS DHONI STUMPING RECORD")
dhoni_stumpings = df[(df['dismissal_kind'] == 'stumped') & (df['fielder'] == 'MS Dhoni')]
print(f"Total Career Stumpings: {len(dhoni_stumpings)}\n")

print("👐 VIRAT KOHLI CATCHING RECORD")
kohli_catches = df[(df['dismissal_kind'] == 'caught') & (df['fielder'] == 'V Kohli')]
print(f"Total Career Catches: {len(kohli_catches)}\n")

print("🏃 RAVINDRA JADEJA RUN-OUT RECORD")
jadeja_runouts = df[(df['dismissal_kind'] == 'run out') & (df['fielder'] == 'RA Jadeja')]
print(f"Total Career Run-Outs: {len(jadeja_runouts)}\n")

# ==========================================
# 4. MATCH & TEAM METRICS
# ==========================================
print("⭐ MOST 'PLAYER OF THE MATCH' AWARDS")
most_potm = matches['player_of_match'].value_counts().head(5)
print(most_potm.to_string(), "\n")

print("🔥 HIGHEST TEAM TOTALS IN A SINGLE MATCH")
highest_runs = df.groupby(['match_id', 'batting_team'])['total_runs'].sum().sort_values(ascending=False).head(5)
print(highest_runs.to_string(), "\n")

# ==========================================
# 5. ADVANCED NUMPY METRICS (STRIKE RATES)
# ==========================================
print("⚡ LEGENDARY BATTER STRIKE RATES (OVERALL)")
legends = ['V Kohli', 'S Dhawan', 'RG Sharma', 'DA Warner', 'CH Gayle']
legends_data = df[df['batter'].isin(legends)]

runs = legends_data.groupby('batter')['batsman_runs'].sum()
legal_deliveries = legends_data[legends_data['extras_type'] != 'wides']
balls = legal_deliveries.groupby('batter')['batsman_runs'].count()

runs_array = runs.to_numpy()
balls_array = balls.to_numpy()

# Vectorized Math
strike_rates = np.round((runs_array / balls_array) * 100, 2)

# Zipping the names and rates together for a clean print
for name, sr in zip(runs.index, strike_rates):
    print(f"{name}: {sr}")

# --- Single Player Single Season Deep Dive ---
target_player = 'V Kohli'
target_year = '2016'  # Changed to his legendary 2016 season!

print(f"\n📊 DEEP DIVE: {target_player} ({target_year} Season)")
player_data = df[(df['batter'] == target_player) & (df['season'] == target_year)]

runs_pandas = player_data['batsman_runs'].sum()
legal_balls_pandas = player_data[player_data['extras_type'] != 'wides']['batsman_runs'].count()

if legal_balls_pandas > 0:
    clean_sr = np.round((runs_pandas / legal_balls_pandas) * 100, 2)
    print(f"Runs Scored: {runs_pandas}")
    print(f"Balls Faced: {legal_balls_pandas}")
    print(f"True Strike Rate: {clean_sr}")
else:
    print(f"No data found for {target_player} in {target_year}.")