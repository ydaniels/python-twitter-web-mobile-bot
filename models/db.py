# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engi
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('mysql://root:twitterbotks@localhost/migration',migrate=True,fake_migrate=False)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
auth.define_tables(username=True)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables


## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled.append('register')
#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)



db.define_table('accounts',Field('username',type='string', length=250,required=True,unique=True,label='Username'), Field('password',type='password', length=250,required=True,label='Password',readable=False),
                Field('firstname',type='string',default='0', length=250,label='Firstname'),Field('lastname',type='string',default='0', length=250,label='Lastname'),Field('email',type='string',required=True,default='0', length=250,label='Email'),
                Field('email_password',type='string', default='0',length=250,label='Password For Email'),Field('oauth_token',default='0',type='string', length=1000,label='Token Key'),Field('oauth_seceret',type='string',default='0',
                length=1000,label='Token Secret'),Field('proxy',type='string', length=100,default='0',label='Proxy'),Field('startunfollow',type='integer',default=0,comment='Please dont change this settings unless you need to',label='startunfollow'),Field('unfollowtrack',type='integer',default=0,readable=False,writable=False,label='startunfollow'),Field('followerscount',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('followingcount',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('likecount',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('suspended',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('phone',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('statuses_count',type='string',default=0,readable=False,writable=False,label='startunfollow'),Field('quitunfollow',type='integer',default=1000,label='Maximum Amount of People To Unfollow before Stating Follow campaign'), Field('inteluser',type='list:string',label='Add list of Intelligent Users'),Field('stopat',type='integer',default=0,label='How many of their users do you want to follow per run',comment='Cannot guarantee i would obey this depending on the amount of retweeters he or she has gotten on the latest hundred  post'), Field('ingnore',type='list:string',label='Add list of Users To Ignore when running Auto Unfollow'),Field('created_by',  default=auth.user_id,readable=False,writable=False,),format='%(username)s')


#db.accounts.user_id.requires = IS_IN_DB(db, db.auth_user.id)
db.define_table('globalsettings', Field('settingsfor',requires=IS_IN_DB(db, 'accounts.id','%(username)s'),label='Account Number Id',comment='Accounts ID  This Settings would apply too '), Field('followsize',type='integer',label='How Many People Do You Want To Follow' ),Field('unfollowsize',type='integer',label='How Many People Do You Want To UnFollow' ), Field('retweetsize',type='integer',label='How Many Tweet Do You Want To Retweet' ), Field('likesize',type='integer',label='How Many Tweet Do You Want To Like' ), Field('dmtext',type='list:string',label='List Of DMs',comment=' supported tokens are {{@}}-> username,{{n}} ->name,{{l}}->location,{{d}}->description,{{w}}-> website e.g (hello {{@}} check out my site ) {{@}} would be replaced by the username we want to mention'),Field('keywordtext',type='list:string',label='List Of Keyword To Watch For Favourite'),Field('retweettext',type='list:string',label='List Of Keyword To Watch For Retweet'),Field('timertofollow',type='list:integer',label='Time To Wait For Between Each Follows'),Field('timertounfollow',type='list:integer',label='Time To Wait For Between Each UNFollows'),Field('timertolike',type='list:integer',label='Time To Wait For Between Each Like'),Field('timertoretweet',type='list:integer',label='Time To Wait For Between Each Retweet'),Field('timertodm',type='list:integer',label='Time To Wait For Between Each Dm'),Field('autotext',type='list:string',label='List Of Keyword To Watch For Auto tweet back'), Field('autosize',type='integer',label='How Many People You want to auto tweet to' ),Field('tweetback',type='list:string',label='List of tweet to use when auto mentioning',comment=' supported tokens are {{@}}-> username,{{n}} ->name,{{l}}->location,{{d}}->description,{{w}}-> website e.g (hello {{@}} check out my site ) {{@}} would be replaced by the username we want to mention'),Field('startfollow',type='integer',label='How many days To Wait Before The Bots Start to Unfollow When It detects it need to unfollow ',comment='Please multiply how many times you run the bot per day with the number e.g 3 days but you run the bot 2 twice a day, then input 6'))
db.define_table('intelligent_users', Field('name',type='string',label='Username'),Field('stopat',type='integer',default=0,label='How many of their users do you want to follow per run',comment='Cannot guarantee i would obey this depending on the amount of retweeters he or she has gotten on the latest hundred  post'))
db.define_table('users_to_follow', Field('name',type='string',length=128,label='Username',unique=True))
db.define_table('users_to_scrape', Field('name',type='string',label='Username Of People You Want To Scrape Their Followers',length=128,unique=True),Field('scraped',type='integer',default=0,label='Scraped ',comment='Please Dont Change this Unless There is to much error in the scrappers log or delete this user it means the account has been scrapped'))
