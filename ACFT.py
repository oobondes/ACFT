import pandas as pd
from datetime import datetime

t0 = datetime.now()

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



t1 = datetime.now()

def acft_score(age, male, rd3, spt, hrp, sdc, plank, mr2, **kwargs):
    print(kwargs)
    alternate_event = {event:pd.to_timedelta(time) for event, time in kwargs.items() if df_alternate['event'].apply(lambda k: k.lower() == event).any()} if kwargs else {}
    print(alternate_event)
    male = male.upper() == 'M'
    score = {'rd3':rd3,'spt':spt,'hrp':hrp,'sdc':pd.to_timedelta(sdc),'plank':pd.to_timedelta(plank),'2mr':pd.to_timedelta(mr2),'alt':alternate_event}
    

    #determines age category to determine what column to look up the score on each DF
    if age <= 21:
        if male:
            cat = 1
        else:
            cat = 2
    elif age <= 26:
        if male:
            cat = 3
        else:
            cat = 4
    elif age <= 31:
        if male:
            cat = 5
        else:
            cat = 6
    elif age <= 36:
        if male:
            cat = 7
        else:
            cat = 8
    elif age <= 41:
        if male:
            cat = 9
        else:
            cat = 10
    elif age <= 46:
        if male:
            cat = 11
        else:
            cat = 12
    elif age <= 51:
        if male:
            cat = 13
        else:
            cat = 14
    elif age <= 56:
        if male:
            cat = 15
        else:
            cat = 16
    elif age <= 61:
        if male:
            cat = 17
        else:
            cat = 18
    else:
        if male:
            cat = 19
        else:
            cat = 20
    
    print(score)

    for event, df in {'rd3':df_3rd,'spt':df_spt,'hrp':df_hrp,'sdc':df_sdc,'plank':df_plank,'2mr':df_2mr, 'alt':alternate_event}.items():
        print(f'{event}: {score[event]}')
        if event in ['rd3','spt','hrp','plank']:
            score[event] = max(df['points'][df[df.columns[cat]] <= score[event]])
        elif event == 'alt':
            alt_score = dict()
            for alt_event, time in score[event].items():
                print(df_alternate[df_alternate['event']==alt_event][df_alternate.columns[cat]])
                print(time, type(time))
                alt_score[alt_event] = df_alternate[df_alternate['event']==alt_event][df_alternate.columns[cat]].iloc[0] >= time
                print(alt_score)
            score.pop(event)
            for alt_event, alt_pass in alt_score.items():
                score[alt_event] = alt_pass
        else:
            score[event] = max(df['points'][df[df.columns[cat]] >= score[event]])   
    score['total'] = score['2mr'] + score['hrp'] + score['rd3'] + score['sdc'] + score['plank'] + score['spt']
    return score
    

if __name__ == '__main__':
    t2 = datetime.now()
    score = acft_score(28,'M',240,8.6,26,'00:1:57','00:2:00','00:13:30', swim='00:12:00')
    t3 = datetime.now()
    print(score)
    load = t1-t0
    run = t3-t2
    print(f'load time {load}s\nmethod run time {run}s')


