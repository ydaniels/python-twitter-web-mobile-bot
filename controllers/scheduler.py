# -*- coding: utf-8 -*-
import tweepy

import time
import random
consumer_key=""
consumer_secret=""


def fopen(filen,cond,data=''):
    filen=filen
    retn=''
    if cond=='r':
        try:
            gt=open(filen,cond)
            err=int(gt.read())
            retn=err
            gt.close()
        except IOError:
            print 'couldnt find file ',filen
            #raise IOError('We couldnt find the file so we initilaize with 0')
            gt=open(filen,'w')
            gt.write(str(0))
            retn=0
            gt.close()



    elif cond=='w':
        if data==0:
            data='0'
        if data:
            gt=open(filen,cond)
            gt.write(str(data))
            gt.close()
        else:
            raise Exception('You are not writting anything')
            retn =-1
    return retn







def ifollow(api,FOLLOWSIZE,acc_id):
    flwn=0
    err=fopen('usert','r')
    dt=fopen('dbtrack','r')
    print err
    if err==0:
        er=list(db(db.users_to_follow.id > int(dt)).select(limitby=(0, 1000)))
        if len(er)<500:
            print 'sorry we couldn continue please scrape more followers'
            return#but call yoe no time to use chang.py to get thier recent tweet
        fopen('dbtrack','w',er[len(er)-1].id)
        import pickle
        er=[x.name for x in er]
        pickle.dump(er,open('www','wb'))
    elif err==-1:
    	err=0
    	er=[]
        print 'but not calling yoe this time'
        import pickle
        er=pickle.load(open('www','rb'))
        print len(er)
    elif err > 0:
        er=[]
        import pickle
        er=pickle.load(open('www','rb'))
        print len(er)
    tokcheck=0
    for t in er:
        if flwn==FOLLOWSIZE:
            print 'reached the following size'
            return 0
        if err==len(er):
            fopen('usert','w','0')
        try:
            if tokcheck==4:
                    print 'something is wrong pls go and we will start unfollow for this user but meanwhile lets keep it in a sandbox for safety'
                    db(db.accounts.id==acc_id).update(startunfollow=1)
                    db.commit()
                    err=err-4
                    if err<=0:
                              err=-1
                    fopen('usert','w',err)
                    break
            raise tweepy.error.TweepError('Sorry')
            api.create_friendship(er[err])
            time.sleep(4)
            tokcheck=0
            flwn=flwn+1
            print 'followed ',er[err]
            #time.sleep(1)
            err=err+1
            fopen('usert','w',err)
        except tweepy.error.TweepError as r:
            tokcheck=tokcheck+1
            err=err+1
            fopen('usert','w',err)
            print r
    return 0



def iunfollow(api,number,t,myid):
    print number
    pg=api.friends_ids()
    po=api.followers_ids()
    o=0
    
    ro =list(db(db.accounts.id==myid).select())[0]
    iu=list(ro.ingnore)
    nonlist=[]
    import time
    for i in iu:
        nonlist.append(api.get_user(i).id_str)
        time.sleep(3)
    for p in pg:
        if o==number:
            break
        if p not in po:
                try:
                    if p in nonlist:
                        continue
                    api.destroy_friendship(p)
                    
                    time.sleep(4)
                except Exception as e:
                    print e
                    o=o+1
                    continue
                else:
                    o=o+1
                    print p,' freindship .destroyed '
                    continue
        else:
            continue
    newo=o+t
    db(db.accounts.id==myid).update(unfollowtrack=newo)
    db.commit()


def scraper(api):
    rows = list(db(db.users_to_scrape).select())
    rows=[x for x in rows if x.scraped==0]
    flist=[]
    from tweepy import Cursor
    if len(rows)==0:
        print 'all users have been scraped please go and update more users from settings'
        return
    st=random.choice(rows)
    error=0
    for page in Cursor(api.followers_ids, screen_name=st).pages():
        flist.extend(page)
        for uid in page:
            try:
                db.users_to_follow.insert(name=uid)
                db.commit()
                print 'inserted ',uid
                if error!=0:
                    error=-1
            except Exception as e:
                if error==1000:
                    print 'Sorry i think we have scrapped this user or the internet connection broke while we were scrapping'
                    break
                error=+1
                print 'error ocurred ',e
              
                continue
        if len(page) == 5000:
            time.sleep(60)
    uid=db(db.users_to_scrape.id==st.id).update(scraped=1)
    db.commit()










def gettoken(email,passwd):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    try:
       
        token=auth.get_access_token(email,passwd)
    except tweepy.TweepError as e:
        print 'sorry couldn not get token seems the account information you entered is wrong or change in  proxy or try and access from a browser',email,passwd
        print e
        return None
    return token


def worker(ans):
    rows = db(db.globalsettings).select()
    rows=[x for x in rows if int(x.id)==SETTINGS]
    for row in rows:

            acc =  row.settingsfor
#	    print acc
            try:
                acc=[int(x) for x in acc ]
            except:
                print 'are you sure you put the correct account number'
                break
            ro = list(db(db.accounts).select())
#            j=1
 #           lass=[]
  #          for i in ro:
   #             if j not in acc:
    #                continue
     #           lass.append(i)
      #          j+=1
	    lass=[x for x in ro if x.id in acc] 
#	    print lass
            for ac in lass:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                if ac.oauth_seceret=='0' or ac.oauth_token=='0':
                    print 'token empty now getting one'
                    tokens=gettoken(ac.username,ac.password)
                    if tokens:
                        uid=db(db.accounts.id==ac.id).update(oauth_seceret=tokens.key,oauth_token=tokens.secret)
                        db.commit()
                        print uid
                    else:
                        return
                    auth.secure = True
            
                    auth.set_access_token(tokens.key, tokens.secret)
                else:
                    auth.set_access_token(ac.oauth_seceret, ac.oauth_token)
                try:
                    apie = tweepy.API(auth_handler=auth,retry_count=4,retry_delay=5)
                    me=apie.me()
                    st=me.screen_name
                    db(db['accounts']._id==ac.id).update(**{'followerscount':str(me.followers_count),'followingcount':str(me.friends_count),
                                                            'likecount':str(me.favourites_count),'statuses_count':str(me.statuses_count),'suspended':str(me.suspended),
                                                           'phone':str(me.needs_phone_verification)})
                    db.commit()
                except Exception as e:
                    print e
                    continue
                print st,'logged in '
                if ans=='follow':
                    if ac.startunfollow==1:
                        print 'still in sandbox keeping your account safe'
                        ans='unfollow'
                    else:
                        ifollow(apie,row.followsize,acc_id=ac.id)
                if ans=='unfollow':
                    
                    if ac.startunfollow>0 and ac.startunfollow<row.startfollow:
                        start=ac.startunfollow+1
                        db(db.accounts.id==ac.id).update(startunfollow=start)
                        db.commit()
                        print 'Waiting in Sandbox before starting unfollow'
                    elif ac.startunfollow==0:
                        print 'Not ready for unfollow yet this is not an error it will start by itself but you can force it to unfollow settings '
                    else:
                        if  ac.unfollowtrack>=ac.quitunfollow:##check if we have unfollowed the number specified in the settings
                            print 'we need to start following done unfollowing'##if we have then reset the following trak and how many days we wait to 0 to start following'
                            db(db.accounts.id==ac.id).update(startunfollow=0)
                            db(db.accounts.id==ac.id).update(unfollowtrack=0)
                            db.commit()
                        else:
                            e=ac.unfollowtrack
                            iunfollow(apie,row.unfollowsize,e,ac.id)
                elif ans=='lhome':
                    
                    lhome(apie,row.likesize)
                elif ans=='rhome':
                    rhome(apie,row.retweetsize)

                elif ans=='lkey':
                    meg=list(row.keywordtext)
                    
                    lkey(apie,random.choice(meg),row.likesize)
                 
                elif ans=='rkey':
                    meg=list(row.retweettext)
                    
                    rkey(apie,random.choice(meg),row.retweetsize)
                elif ans=='ckey':
                    meg=list(row.tweetback)
                    imeg=list(row.autotext)
                    ckey(apie,meg,random.choice(imeg),int(row.autosize))
                elif ans=='fret':
                    roc = list(db(db.accounts.id==ac.id).select())[0]
		   # print ro

                    iu=list(roc.inteluser)
                    #iu= list(db(db.intelligent_users).select())
                    #les=random.choice(iu)
                    fret(apie,iu,int(roc.stopat))
                elif ans=='duser':
                    message=list(row.dmtext)
                    duser(apie,message)
                elif ans=='suser':
                    scraper(apie)
                else:
                    print 'does not understand'


#@

def follow():
    worker('follow')

def unfollow():
     worker ('unfollow')

def like_home():
     return
     worker('lhome')


def retweet_home():
     return
     worker( 'rhome')


def like_keyword():
     worker( 'lkey')


def retweet_keyword():
     worker('rkey')


def comment_keyword():
    worker( 'ckey')


def follow_retweet():
#    print 'd'
    worker( 'fret')

def dm_user():
     worker( 'duser')

def s_user():
    worker( 'suser')

def mytables(db):
    db.define_table('accounts',Field('username',type='string', length=250,required=True,unique=True,label='Username'), Field('password',type='password', length=250,required=True,label='Password'),
                Field('firstname',type='string',default='0', length=250,label='Firstname'),Field('lastname',type='string',default='0', length=250,label='Lastname'),Field('email',type='string',required=True,default='0', length=250,label='Email'),
                Field('email_password',type='string', default='0',length=250,label='Password For Email'),Field('oauth_token',default='0',type='string', length=1000,label='Token Key'),Field('oauth_seceret',type='string',default='0',
                length=1000,label='Token Secret'),Field('proxy',type='string', length=100,default='0',label='Proxy'),Field('startunfollow',type='integer',default=0,readable=False,writable=False,label='startunfollow'),Field('unfollowtrack',type='integer',default=0,readable=False,writable=False,label='startunfollow'),Field('followerscount',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('followingcount',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('likecount',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('suspended',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('phone',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('statuses_count',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('quitunfollow',type='integer',default=1000,label='Maximum Amount of People To Unfollow before Stating Follow campaign'),  Field('inteluser',type='list:string',label='Add list of Intelligent Users'),Field('stopat',type='integer',default=0,label='How many of their users do you want to follow per run',comment='Cannot guarantee i would obey this depending on the amount of retweeters he or she has gotten on the latest hundred  post'), Field('ingnore',type='list:string',label='Add list of Users To Ignore when running Auto Unfollow'),Field('created_by',  default=1,readable=False,writable=False,),format='%(username)s')

    db.define_table('globalsettings', Field('settingsfor',type='list:string',label='Account Number Id',comment='Accounts Id This Settings would apply too '), Field('followsize',type='integer',label='How Many People Do You Want To Follow' ),Field('unfollowsize',type='integer',label='How Many People Do You Want To UnFollow' ), Field('retweetsize',type='integer',label='How Many Tweet Do You Want To Retweet' ), Field('likesize',type='integer',label='How Many Tweet Do You Want To Like' ), Field('dmtext',type='list:string',label='List Of DMs',comment=' supported tokens are {{@}}-> username,{{n}} ->name,{{l}}->location,{{d}}->description,{{w}}-> website e.g (hello {{@}} check out my site ) {{@}} would be replaced by the username we want to mention'),Field('keywordtext',type='list:string',label='List Of Keyword To Watch For Favourite'),Field('retweettext',type='list:string',label='List Of Keyword To Watch For Retweet'),Field('timertofollow',type='list:integer',label='Time To Wait For Between Each Follows'),Field('timertounfollow',type='list:integer',label='Time To Wait For Between Each UNFollows'),Field('timertolike',type='list:integer',label='Time To Wait For Between Each Like'),Field('timertoretweet',type='list:integer',label='Time To Wait For Between Each Retweet'),Field('timertodm',type='list:integer',label='Time To Wait For Between Each Dm'),Field('autotext',type='list:string',label='List Of Keyword To Watch For Auto tweet back'), Field('autosize',type='integer',label='How Many People You want to auto tweet to' ),Field('tweetback',type='list:string',label='List of tweet to use when auto mentioning',comment=' supported tokens are {{@}}-> username,{{n}} ->name,{{l}}->location,{{d}}->description,{{w}}-> website e.g (hello {{@}} check out my site ) {{@}} would be replaced by the username we want to mention'),Field('startfollow',type='integer',label='How many days To Wait Before The Bots Start to Unfollow When It detects it need to unfollow ',comment='Please multiply how many times you run the bot per day with the number e.g 3 days but you run the bot 2 twice a day, then input 6'))
    db.define_table('intelligent_users', Field('name',type='string',label='Username'),Field('stopat',type='integer',default=0,label='How many of their users do you want to follow per run',comment='Cannot guarantee i would obey this depending on the amount of retweeters he or she has gotten on the latest hundred  post'))

    db.define_table('users_to_follow', Field('name',type='string',label='Username',unique=True))
    db.define_table('users_to_scrape', Field('name',type='string',label='Username Of People You Want To Scrape Their Followers',unique=True),Field('scraped',type='integer',default=0,label='Scraped ',comment='Please Dont Change this Unless There is to much error in the scrappers log or delete this user it means the account has been scrapped'))
    return db


if __name__ == '__main__':
    from pydal import DAL, Field

    db = DAL('mysql://@localhost/migration',migrate=False,fake_migrate=True)
    db=mytables(db)
    import os
    import sys
    if len(sys.argv)<3:
        print 'Sorry not enough command to run arguement'
        sys.exit(0)
    SETTINGS=int(sys.argv[1])
    func=int(sys.argv[2])
    if func==1:
        print 'Follow fuction'
        follow()
    elif func==2:
        print 'Unfollow fuction'
        unfollow()
    elif func==5:
        print 'Like a Particular Keyword'
        like_keyword()
    elif func==6:
        print 'Retweet a Particular Keyword'
        retweet_keyword()
    elif func==7:
        print 'Auto Reply at Keyword function '
        comment_keyword()
    elif func==8:
        print 'Intelligent Follow users function '
        follow_retweet()
    elif func==9:
        print 'DM users function '
        dm_user()
    elif func==10:
        print 'scrape users function '
        s_user()
    else:
        print 'cant understand ',func
else:
    from gluon.scheduler import Scheduler
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db,dict(follow=follow,Unfollow=unfollow,like_home=like_home,Retweet_Home_Feed=retweet_home,
                             Like_Keyword_or_Hashtag_By_Search=like_keyword,Retweet_Keyword_or_Hashtag_By_Search=retweet_keyword,
                             Auto_Tweet_to_Keyword_or_Hashtag=comment_keyword,Intelligent_Follow=follow_retweet,Auto_Message=dm_user ,Scrape_User=s_user ))
