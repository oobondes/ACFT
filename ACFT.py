import pandas as pd
from datetime import datetime
#import all score csv's to DataFrames (DF)
df_2mr = pd.read_csv('2MR_SC.csv')
df_3rd = pd.read_csv('3RD_SC.csv')
df_hrp = pd.read_csv('HRP_SC.csv')
df_plank = pd.read_csv('plank_SC.csv')
df_sdc = pd.read_csv('SDC_SC.csv')
df_spt = pd.read_csv('SPT_SC.csv')
df_alternate = pd.read_csv('special_SC.csv')

#sets all timed events to timemdeltas so lookups can be done
for df in [df_plank,df_2mr,df_sdc,df_alternate]:
    for col in df.columns[1::]:
        df[col] = pd.to_timedelta(df[col])

def acft_score(age, gender, rd3, spt, hrp, sdc, plank, mr2, alternate_event=None):
    score = {'rd3':rd3,'spt':spt,'hrp':hrp,'sdc':pd.to_timedelta(sdc),'plank':pd.to_timedelta(plank),'2mr':pd.to_timedelta(mr2),'alt':None if not alternate_event else pd.to_timedelta(alternate_event)}

    #determines age category to determine what column to look up the score on each DF
    if age <= 21:
        if gender == 'M':
            cat = 1
        else:
            cat = 2
    elif age <= 26:
        if gender == 'M':
            cat = 3
        else:
            cat = 4
    elif age <= 31:
        if gender == 'M':
            cat = 5
        else:
            cat = 6
    elif age <= 36:
        if gender == 'M':
            cat = 7
        else:
            cat = 8
    elif age <= 41:
        if gender == 'M':
            cat = 9
        else:
            cat = 10
    elif age <= 46:
        if gender == 'M':
            cat = 11
        else:
            cat = 12
    elif age <= 51:
        if gender == 'M':
            cat = 13
        else:
            cat = 14
    elif age <= 56:
        if gender == 'M':
            cat = 15
        else:
            cat = 16
    elif age <= 61:
        if gender == 'M':
            cat = 17
        else:
            cat = 18
    else:
        if gender == 'M':
            cat = 19
        else:
            cat = 20
    
    for event, df in {'rd3':df_3rd,'spt':df_spt,'hrp':df_hrp,'sdc':df_sdc,'plank':df_plank,'2mr':df_2mr}.items():
        print(f'{event}: {score[event]}')
        if event in ['rd3','spt','hrp','plank']:
            score[event] = max(df['points'][df[df.columns[cat]] <= score[event]])#.iloc[0]
        else:
            score[event] = max(df['points'][df[df.columns[cat]] >= score[event]])#.iloc[0]    
        print(f'{event}: {score[event]}')
    score['total'] = score['2mr'] + score['hrp'] + score['rd3'] + score['sdc'] + score['plank'] + score['spt']
    return score
    

if __name__ == '__main__':
    score = acft_score(28,'M',240,8.6,26,'00:1:57','00:2:00','00:13:30')
    print(score)


