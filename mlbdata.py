import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


#-------------------------create GUI window--------------------------------------
st.title('MLB Data Analysis Application')

tab1, tab2, tab3 = st.tabs(["Batting", "Pitching", "Player Comparison"])


with tab1:
    st.header("Batting Analysis")
    st.write("Analyze team batting statistics by selecting a team and year.")

    # get data
    batting = pd.read_csv('data/Batting.csv')
    teams = pd.read_csv('data/Teams.csv')
    players = pd.read_csv('data/People.csv')

    #join batting with players
    batting = batting.merge(players[['playerID', 'nameFirst', 'nameLast']], on='playerID', how='left')

    #select team
    selected_team = st.selectbox("Select a Team", teams['name'].unique(), index=None, key='batting_team')
    if selected_team:
        teamID = teams[teams['name'] == selected_team]['teamID'].values[0]
        #get years from selected team
        years = sorted(batting[batting['teamID'] == teamID]['yearID'].unique())
        selected_year = st.selectbox("Select a Year", years, index=None, key='batting_year')

        if selected_year:
            #get filtered data for team, sort by number of hits
            filtered_data = batting[(batting['teamID'] == teamID) & (batting['yearID'] == selected_year)].sort_values(by='H', ascending=False)
            #remove pitchers with 0 AB
            filtered_data = filtered_data[filtered_data['AB'] > 0]

            #join first and last name
            filtered_data['Name'] = filtered_data['nameFirst'] + ' ' + filtered_data['nameLast']

            #create bar graph
            fig, ax = plt.subplots()
            ax.bar(['Hits', 'Home Runs', 'Runs', 'RBIs', 'Doubles', 'Triples', 'Strikeouts'], 
                   [filtered_data['H'].sum(), filtered_data['HR'].sum(), filtered_data['R'].sum(), filtered_data['RBI'].sum(), filtered_data['2B'].sum(), filtered_data['3B'].sum(), filtered_data['SO'].sum()])
            ax.set_ylabel('Count')
            ax.set_title(f'Batting Stats for {selected_team} in {selected_year}')
            ax.bar_label(ax.containers[0])
            st.pyplot(fig)

            #display player stats for that year
            df = filtered_data[['Name', 'G', 'AB', 'H', 'R', 'HR', '2B', '3B', 'RBI', 'SB', 'CS', 'BB', 'SO']]
            df.rename(columns={
                'G': 'Games',
                'AB': 'At Bats',
                'H': 'Hits',
                'R': 'Runs',
                'HR': 'Home Runs',
                '2B': 'Doubles',
                '3B': 'Triples',
                'RBI': 'RBIs',
                'SB': 'Stolen Bases',
                'CS': 'Caught Stealing',
                'BB': 'Walks',
                'SO': 'Strikeouts'
            }, inplace=True)
            st.write(df.reset_index(drop=True))

with tab2:
    st.header("Pitching Analysis")
    st.write("Analyze team pitching statistics by selecting a team and year.")

    #get data
    pitching = pd.read_csv('data/Pitching.csv')
    teams = pd.read_csv('data/Teams.csv')
    players = pd.read_csv('data/People.csv')

    #merge on playerID
    pitching = pitching.merge(players[['playerID', 'nameFirst', 'nameLast']], on='playerID', how='left')

    #select team
    selected_team = st.selectbox("Select a Team", teams['name'].unique(), index=None, key='pitching_team')
    if selected_team:
        teamID = teams[teams['name'] == selected_team]['teamID'].values[0]
        #get years from selected team
        years = sorted(pitching[pitching['teamID'] == teamID]['yearID'].unique())
        selected_year = st.selectbox("Select a Year", years, index=None, key='pitching_year')

        if selected_year:
            #get filtered data for team, sort by number of strikeouts
            filtered_data = pitching[(pitching['teamID'] == teamID) & (pitching['yearID'] == selected_year)].sort_values(by='SO', ascending=False)
            #remove players with 0 IP
            filtered_data['IP'] = filtered_data['IPouts'] / 3
            filtered_data = filtered_data[filtered_data['IP'] > 0]

            #join first and last name
            filtered_data['Name'] = filtered_data['nameFirst'] + ' ' + filtered_data['nameLast']

            #create bar graph
            fig, ax = plt.subplots()
            ax.bar(['Strikeouts', 'Wins', 'Losses', 'Games', 'Saves', 'Hits', 'Home Runs', 'ER', 'IP'], 
                   [filtered_data['SO'].sum(), filtered_data['W'].sum(), filtered_data['L'].sum(), filtered_data['G'].sum(), filtered_data['SV'].sum(), filtered_data['H'].sum(), filtered_data['HR'].sum(), filtered_data['ER'].sum(), filtered_data['IP'].sum()])
            ax.set_ylabel('Count')
            ax.set_title(f'Pitching Stats for {selected_team} in {selected_year}')
            ax.bar_label(ax.containers[0])
            st.pyplot(fig)

            #display player stats for that year
            df = filtered_data[['Name', 'SO', 'W', 'L', 'G', 'SV', 'H', 'HR', 'ER', 'IP']]
            df.rename(columns={
                'SO': 'Strikeouts',
                'W': 'Wins',
                'L': 'Losses',
                'G': 'Games',
                'SV': 'Saves',
                'H': 'Hits',
                'HR': 'Home Runs',
                'ER': 'Earned Runs',
                'IP': 'Innings Pitched',
            }, inplace=True)
            st.write(df.reset_index(drop=True))

with tab3:
    st.header("Player Comparison")
    st.write("Compare career stats of two players")
    #get data
    players = pd.read_csv('data/People.csv')
    teams = pd.read_csv('data/Teams.csv')
    batting = pd.read_csv('data/Batting.csv')
    pitching = pd.read_csv('data/Pitching.csv')

    #join batting with players
    batting = batting.merge(players[['playerID', 'nameFirst', 'nameLast']], on='playerID', how='left')
    batting['Name'] = batting['nameFirst'] + ' ' + batting['nameLast']

    #get players from user search using auto-complete
    available_players = batting['Name'].unique()
    player1 = st.selectbox("Select First Player", available_players, index=None, key='player1')
    player2 = st.selectbox("Select Second Player", available_players, index=None, key='player2')
    if player1 and player2:
        #get data point from user
        stat = st.selectbox("Select Stat", ['AVG', 'H', 'RBI', 'R', 'HR'], index=None, key='stat')
        batting['AVG'] = batting['H'] / batting['AB']
        if stat:
            #calculate avg if stat is avg
            if stat == 'AVG':
                player1_stat = batting[batting['Name'] == player1]['H'].sum() / batting[batting['Name'] == player1]['AB'].sum()
                player2_stat = batting[batting['Name'] == player2]['H'].sum() / batting[batting['Name'] == player2]['AB'].sum()
                player1_stat = round(player1_stat, 3)
                player2_stat = round(player2_stat, 3)
            else:
                player1_stat = batting[batting['Name'] == player1][stat].sum()
                player2_stat = batting[batting['Name'] == player2][stat].sum()
            #display graph of data to compare
            fig, ax = plt.subplots()
            ax.bar([player1, player2], [player1_stat, player2_stat])
            ax.set_ylabel(stat)
            ax.set_title(f'Comparison of career {stat} for {player1} and {player2}')
            ax.bar_label(ax.containers[0])
            if stat == 'AVG':
                #make y axis label 3 digits
                ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
            st.pyplot(fig)

            #graph yearly stat
            player1_yearly = batting[batting['Name'] == player1].groupby('yearID')[stat].sum()
            player2_yearly = batting[batting['Name'] == player2].groupby('yearID')[stat].sum()
            fig, ax = plt.subplots()
            ax.plot(player1_yearly.index, player1_yearly.values, label=player1)
            ax.plot(player2_yearly.index, player2_yearly.values, label=player2)
            ax.set_ylabel(stat)
            ax.set_title(f'Yearly {stat} for {player1} and {player2}')
            ax.legend()
            if stat == 'AVG':
                #make y axis label 3 digits
                ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
            st.pyplot(fig)
