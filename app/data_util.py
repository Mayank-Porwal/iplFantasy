import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from datetime import datetime


class ProcessData:
    def __init__(self, file='/Users/mayankporwal/Downloads/ipl_2023_dataset.csv'):
        self.file = file
        self.player_df = pd.read_csv(file, index_col=0)
        self.category_map = {'All-Rounder': 'ar', 'Bowler': 'bowler', 'Wicket-Keeper': 'wk', 'Batter': 'batsman'}
        self.ipl_team_map = {
            'Chennai Super Kings': 'CSK', 'Delhi Capitals': 'DC', 'Gujarat Titans': 'GT', 'Lucknow Super Giants': 'LSG',
            'Mumbai Indians': 'MI', 'Punjab Kings': 'PK', 'Royal Challengers Bangalore': 'RCB',
            'Rajasthan Royals': 'RR', 'Sunrisers Hyderabad': 'SRH'
        }

    @staticmethod
    def rds_engine():
        url = os.environ['DATABASE_URL'].replace('postgresql', 'postgresql+psycopg2')
        return create_engine(url)

    def process_df(self):
        self.player_df = self.player_df[self.player_df['Team'].ne('Unsold')]
        self.player_df['Type'] = self.player_df['Type'].map(self.category_map)
        self.player_df['Team'] = self.player_df['Team'].map(self.ipl_team_map)
        self.player_df.columns = ['name', 'category', 'price', 'ipl_team']
        self.player_df['image_file'] = ''
        self.player_df['cap'] = 6
        self.player_df[['created_at', 'updated_at']] = datetime.now()
        self.player_df.drop('price', axis=1, inplace=True)

    def insert_df_to_table(self, table):
        self.process_df()
        print(self.player_df)
        self.player_df.to_sql(name=table, con=ProcessData.rds_engine(), index=False, if_exists='append')


if __name__ == '__main__':
    obj = ProcessData()
    obj.insert_df_to_table('player')
