from random import randint
import pandas as pd
from datetime import datetime

t0 = datetime.now()

#import all score csv's to DataFrames (DF)
_df_mr2 = pd.read_csv('2MR_SC.csv')
_df_3rd = pd.read_csv('3RD_SC.csv')
_df_hrp = pd.read_csv('HRP_SC.csv')
_df_plank = pd.read_csv('plank_SC.csv')
_df_sdc = pd.read_csv('SDC_SC.csv')
_df_spt = pd.read_csv('SPT_SC.csv')
_df_alternate = pd.read_csv('special_SC.csv')

#sets all timed events to timemdeltas so lookups can be done
for _df in [_df_plank,_df_mr2,_df_sdc,_df_alternate]:
    for col in _df.columns[1::]:
        _df[col] = pd.to_timedelta(_df[col])



t1 = datetime.now()

def calc_score(age, male, rd3, spt, hrp, sdc, plank, mr2, **kwargs):
    """a method to calculate someone's ACFT score given their raw scores

    Args:
        age (int): persons age in yrs
        male (str): M for male, anything else will calculate a score for a female
        rd3 (int): 3 rep dead lift raw score
        spt (int): standing power throw raw score
        hrp (int): hand release push ups raw score
        sdc (str): sprint drag carry time in the format 'hh:mm:ss'
        plank (str): plank time in the format 'hh:mm:ss'
        mr2 (str): 2 mile run time in the format 'hh:mm:ss'

    Returns:
        dict: a dictionary of all calculated score per category and total score
    """

    print(kwargs)
    alternate_event = {event:pd.to_timedelta(time) for event, time in kwargs.items() if _df_alternate['event'].apply(lambda k: k.lower() == event).any()} if kwargs else {}
    print(alternate_event)
    male = male.upper() == 'M'
    score = {'rd3':rd3,'spt':spt,'hrp':hrp,'sdc':pd.to_timedelta(sdc),'plank':pd.to_timedelta(plank),'mr2':pd.to_timedelta(mr2),'alt':alternate_event}
    

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

    for event, df in {'rd3':_df_3rd,'spt':_df_spt,'hrp':_df_hrp,'sdc':_df_sdc,'plank':_df_plank,'mr2':_df_mr2, 'alt':alternate_event}.items():
        print(f'{event}: {score[event]}')
        if event in ['rd3','spt','hrp','plank']:
            try:
                score[event] = max(df['points'][df[df.columns[cat]] <= score[event]])
            except: # ValueError needs to be handled
                score[event] = 0
        elif event == 'alt':
            alt_score = dict()
            for alt_event, time in score[event].items():
                print(_df_alternate[_df_alternate['event']==alt_event][_df_alternate.columns[cat]])
                print(time, type(time))
                alt_score[alt_event] = _df_alternate[_df_alternate['event']==alt_event][_df_alternate.columns[cat]].iloc[0] >= time
                print(alt_score)
            score.pop(event)
            for alt_event, alt_pass in alt_score.items():
                score[alt_event] = alt_pass
        else:
            try:
                score[event] = max(df['points'][df[df.columns[cat]] >= score[event]])
            except:
                score[event] = 0
    score['total'] = score['mr2'] + score['hrp'] + score['rd3'] + score['sdc'] + score['plank'] + score['spt']
    print(score)
    return score

def calc_scores(raw_score_dict):
    
    score = list()
    for raw_score in raw_score_dict:
        print('test:',raw_score)
        calculated_score=calc_score(**raw_score)
        for key, value in raw_score.items():
            if key not in calculated_score:
                calculated_score[key] = value
            else:
                calculated_score[f'raw_{key}'] = value
        score.append(calculated_score)
    return score

def scores_to_excel(raw_score_dict, file='test.xlsx'):
    score_df = pd.DataFrame(calc_scores(raw_score_dict))
    score_df.to_excel(file,index=False)


if __name__ == '__main__':
    """
    data to test this module with
    """
    import random as r
    t2 = datetime.now()
    score = calc_score(28,'M',240,8.6,26,'00:1:57','00:2:00','00:13:30', swim='00:12:00')
    t3 = datetime.now()
    print(score)
    load = t1-t0
    run = t3-t2
    print(f'load time {load}s\nmethod run time {run}s')
    print(*calc_scores([{'name':f'test#{test}','age':r.randint(19,30),'male':'M' if r.randint(0,1) else 'F','rd3':r.randint(200,400),'spt':r.randint(40,140)/10,'hrp':randint(5,60),'sdc':f'00:{r.randint(0,3)}:{r.randint(0,59)}','plank':f'00:{r.randint(1,4)}:{r.randint(0,59)}','mr2':f'00:{r.randint(10,30)}:{r.randint(0,59)}'} for test in range(20)]), sep='\n')
    scores_to_excel([{'name':f'test#{test}','age':r.randint(19,30),'male':'M' if r.randint(0,1) else 'F','rd3':r.randint(200,400),'spt':r.randint(40,140)/10,'hrp':randint(5,60),'sdc':f'00:{r.randint(0,3)}:{r.randint(0,59)}','plank':f'00:{r.randint(1,4)}:{r.randint(0,59)}','mr2':f'00:{r.randint(10,30)}:{r.randint(0,59)}'} for test in range(20)])