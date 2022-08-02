#!/usr/bin/env python
# coding: utf-8

# In[72]:


#CSV 데이터 파일을 불러오기 위하여 pandas 라이브러리 불러온다
import pandas as pd


# In[73]:


data = pd.read_csv('C:/Users/82108/Documents/data/Fifa_data.csv')


# In[74]:


data.head()


# In[75]:


pd.set_option('display.max_columns',80)


# In[76]:


data.head()


# In[77]:


afc = data[data['Club'] == 'Arsenal']


# In[78]:


afc['Club'].unique()


# In[79]:


data['Club'].unique()


# In[80]:


print(f"인원 : {afc.shape[0]}")
print(f"아스날 선수들의 포지션 : {afc['Position'].unique()}")
print(f"평균 능력치 : {afc['Overall'].mean()}")
print(f"평균 잠재능력치 : {afc['Potential'].mean()}")


# In[81]:


import seaborn as sns
sns.countplot(afc['Age'])


# In[82]:


sns.countplot(afc['Position'])


# In[83]:


sns.boxplot(data = afc, x = 'Position', y ='Overall')


# In[84]:


#이상치 확인 overall이 150 있는지 확인
afc[afc['Overall']>100]


# In[85]:


afc[afc['Position'] == 'CB'][['Position', 'Overall', 'CB']]


# In[86]:


#결측치 확인
afc.info()


# In[87]:


#LS ~ RB까지 결측치 3개가 보인다. 원인을 찾아보자
afc[afc.isnull()['LS']]
#포지션이 GK인 선수는 다른 포지션들의 값이 비어 있는 것을 확인


# In[88]:


afc = afc.fillna(-1)


# In[89]:


afc.info()


# In[90]:


#3. 어떤 포지션을 보강을 해야되는지 다른 팀과 비교

df = data[(data['Club'] == 'Arsenal')| (data['Club'] =='Tottenham Hotspur')]


# In[91]:


df['Club'].unique()


# In[92]:


df['Value'].head()


# In[93]:


#환율 환전
import warnings
warnings.filterwarnings(action = 'ignore')


# In[94]:


#M 이랑 K 0으로 교체
df['Value'] = df['Value'].str.replace('M','000000')
df['Value'] = df['Value'].str.replace('K','000')


# In[95]:


#유로 마크 자르기
df['Value'] = df['Value'].str.slice(1,)
df['Value'] = df['Value'].str.replace('.','')


# In[96]:


#String을 int로 전환
df['Value'] = df['Value'].astype(int)


# In[97]:


afc = df[df['Club']=='Arsenal']
tot = df[df['Club']=='Tottenham Hotspur']


# In[98]:


df.head()


# In[99]:


#포지션 별 주전 선수 비교
gk_list = ['GK']
cb_list = ['CB','LCB','RCB','RB','LB']
mf_list = ['RCM','LCM','RDM','LDM','CM','RM','LM',"CAM"]
st_list = ['ST', 'LW', 'RW']


# In[110]:


#각 포지션별 남은자리 숫자를 입력
st_count = 2 
mf_count = 4
cb_count = 4
gk_count = 1

afc_id =[]

for index in afc.index:
    if afc['Position'][index] in gk_list :
        if gk_count != 0 :
            afc_id.append(afc['ID'][index])
            gk_count -= 1
    elif afc['Position'][index] in cb_list :
        if cb_count != 0:
            afc['Position'][index] = 'CB'
            afc_id.append(afc['ID'][index])
            cb_count -= 1
    elif afc['Position'][index] in mf_list :
        if mf_count != 0:
            afc['Position'][index] = 'MF'
            afc_id.append(afc['ID'][index])
            mf_count -= 1
    else :
        if st_count != 0:
            afc['Position'][index] = 'ST'
            afc_id.append(afc['ID'][index])
            st_count -= 1
        


# In[111]:


afc[afc['ID'].isin(afc_id)]


# In[108]:


st_count = 2 
mf_count = 4
cb_count = 4
gk_count = 1

tot_id =[]

for index in tot.index:
    if tot['Position'][index] in gk_list :
        if gk_count != 0 :
            tot_id.append(tot['ID'][index])
            gk_count -= 1
    elif tot['Position'][index] in cb_list :
        if cb_count != 0:
            tot['Position'][index] = 'CB'
            tot_id.append(tot['ID'][index])
            cb_count -= 1
    elif tot['Position'][index] in mf_list :
        if mf_count != 0:
            tot['Position'][index] = 'MF'
            tot_id.append(tot['ID'][index])
            mf_count -= 1
    else :
        if st_count != 0:
            tot['Position'][index] = 'ST'
            tot_id.append(tot['ID'][index])
            st_count -= 1


# In[109]:


tot[tot['ID'].isin(tot_id)]


# In[113]:


#afc,tot 주전 선수가 모인 데이터를 만든다
df = pd.concat([afc,tot])


# In[105]:


df.tail()


# In[114]:


sns.boxplot(data = df, x = 'Position', y = 'Overall', hue ='Club')


# In[115]:


#어떤 포지션을 보강해야될까
#1) 방출 - 잔류포인트 기준으로 / 잔류 포인트 (overall * 2 + potentail)/AGE

afc['Point'] = (afc['Overall'] * 2 + afc['Potential'])/afc['Age']


# In[119]:


afc[afc['Position'] == 'RB'][['Name','Overall','Potential','Age','Joined','Point']]


# In[120]:


afc[afc['Position'] == 'CM'][['Name','Overall','Potential','Age','Joined','Point']]


# In[121]:


#RB , CM 포지션을 제외한 선수들을 제거 합니다
market = data[(data['Position'] == 'RB') | (data['Position'] == 'CM')]


# In[122]:


import matplotlib.pyplot as plt


# In[130]:


f,ax = plt.subplots(2,4, figsize = (20,10))


# In[152]:


f,ax = plt.subplots(2,4,figsize = (20,10))

vs_list = ['Age', 'Overall', 'Potential', 'Weak Foot']

for i in range(8) :
    if i < 4 :
        
        colors = ['firebrick' if x > market[market['Position'] == 'RB'][:13][vs_list[i]].mean() else 'gray' for x in market[market['Position']=='RB'][:13][vs_list[i]]]
        
        sns.barplot(x = vs_list[i], y = 'Name', data = market[market['Position'] == 'RB'][:13],ax = ax[i//4,i%4], palette = colors)
        
        ax[i//4, i%4].axvline(market[market['Position']=='RB'][:13][vs_list[i]].mean(), ls = '--')
    
    else :
        sns.barplot(x = vs_list[i%4], y = 'Name', data = market[market['Position'] == 'CM'][:13], ax = ax[i//4,i%4], palette = colors)
        
        ax[i//4, i%4].axvline(market[market['Position']=='CM'][:13][vs_list[i%4]].mean(), ls = '--')
        
        


# In[ ]:




