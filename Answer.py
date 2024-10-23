import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

''' Question 1 '''
df_original = pd.read_csv('game_data.csv', delimiter='|')

### Removing any rows with missing values ###
# print(df_original.isna().sum())
df_clean = df_original.columns = df_original.columns.str.strip()
df_clean = df_original.dropna(axis=1, how='any')
df_clean = df_clean.iloc[1:]
df_clean.reset_index(drop=True, inplace=True)

# print(df_clean)
# print(df_clean.dtypes)

df_clean['game_id'] = df_clean['game_id'].astype(int)
df_clean['player_id'] = df_clean['player_id'].astype(int)
df_clean['score'] = pd.to_numeric(df_clean['score'], errors='coerce')
df_clean['level'] = pd.to_numeric(df_clean['level'], errors='coerce')
df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], errors='coerce')
df = df_clean
print(df.dtypes)

#### Create a new column score_category ('Low': score < 50, 'Medium': 50 <= score < 80,'High': score >= 80) ###
criteria = [
    df['score'] < 50,
    (df['score'] >= 50) & (df_clean['score'] < 80),
    df['score'] >= 80
]

categories = ['Low', 'Medium', 'High']
df['score_category'] = np.select(criteria, categories, default='Unknown')
# print(df)
    
### Group the data by score_category and calculate the average score for each level ###
grouped_data = df.groupby(['score_category', 'level']).agg(average_score=('score', 'mean'))
grouped_data['average_score'] = grouped_data['average_score'].round().astype(int)
print(grouped_data)

''' Question 2 '''

# What is the average score of players across all levels?
all_levels_average_score = df['score'].mean()
print(f"The average score of players across all levels: {round(all_levels_average_score)}")

# Which level has the highest average score?
average_score_by_level = df.groupby('level')['score'].mean()
highest_average_score_level = average_score_by_level.idxmax()
highest_average_score = average_score_by_level.max()
print(f"Level with Highest Average Score: Level {highest_average_score_level} with an average score of {round(highest_average_score)}")

# How many players scored in the 'High' category?
high_category_count = df[df['score_category'] == 'High']['player_id'].nunique()
print(f"Number of Players in 'High' Score Category: {high_category_count}")

''' Question 3 '''
# Create a bar chart that shows the average score for each level

fig, ax = plt.subplots(figsize=(8, 8)) 
average_score_by_level.plot(kind='bar', color='skyblue', ax=ax)
plt.title('The Average Score For Each Level')
plt.xlabel('Level')
plt.ylabel('Average Score')
plt.xticks(rotation=0)
for p in ax.patches:
    height = round(p.get_height())  
    ax.annotate(f'{height}',  
                (p.get_x() + p.get_width() / 2., p.get_height()),  
                ha='center', va='bottom',  
                textcoords="offset points",  
                xytext=(0,4))  

plt.show()

# Create a pie chart that displays the distribution of score categories ('Low', 'Medium', 'High')
category_distribution = df['score_category'].value_counts(normalize=True)

plt.figure(figsize=(8, 6))
plt.pie(category_distribution, labels=category_distribution.index, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'orange', 'blue'])
plt.title('Distribution of Score Categories')
plt.show()

''' Question 4 '''
# Write a function that takes a player_id as input and returns the player's highest score and the level at which it was achieved

def get_highest_score(player_id):
    player_data = df[df['player_id'] == player_id]
    
    if player_data.empty:
        return f"No data available for player_id {player_id}"
    
    max_score_entry = player_data[player_data['score'] == player_data['score'].max()].iloc[0]

    highest_level = max_score_entry['level']
    highest_score = max_score_entry['score']
    
    return highest_score, highest_level

def main():
    while True:
        user_input = input("Please enter a player_id (or type 'exit' to quit): ").strip()
        
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        
        if user_input.isdigit():
            player_id = int(user_input)
            result = get_highest_score(player_id)
            if isinstance(result, tuple):
                print(f"Player_id {user_input} highest Score: {result[0]}, highest Level: {result[1]}")
            else:
                print(result)
        else:
            print("Invalid input. Please enter a numeric player id. For example, type 1, 2, or 3.")

if __name__ == "__main__":
    main()