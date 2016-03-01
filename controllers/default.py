# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
@auth.requires_login()
def delete_run():
    from sys import platform
    import os
    from crontab import CronTab
    if 'win' in platform:
            cron = CronTab(tabfile='filename.tab')
    elif 'linu' in platform:
            cron  = CronTab(user=True)
    crons=[]
    i=1
    for job in cron:
        crons.append(OPTION('Job:'+str(i)+' ' +str(job.command),_value=i))
        i+=1
    crons=tuple(crons)
    form = FORM('What Schedule Do You Want To Delete ? ',SELECT(crons,_name='settings'),BR(),
             BR(),INPUT(_type='submit'))
    if form.process().accepted:
        cron.remove( cron[int(form.vars.settings)-1] )
        response.flash = 'Cron Deleted Successfully'
        cron.write()
    return dict(form=form)
    
    
@auth.requires_login()
def schedule_run():
    settings = db().select(db.globalsettings.ALL)
    sett=tuple([OPTION('Settings '+str(int(x.id))+' with '+str(x.settingsfor)+' accounts' , _value=int(x.id)) for x in settings])
    
    form = FORM('What Settings Do You want to Schedule For ? ',SELECT(sett,_name='settings'),BR(),
             BR(),'What Action or Function Do You Want To Perform ',SELECT(OPTION('Follow',_value=1),OPTION('Unfollow',_value=2),OPTION('Scrape Users',_value=10),_name='functions'),BR(),BR(),'Minute ',INPUT(_name='min'),BR(),BR(),BR(),BR(),'Hour ',INPUT(_name='hour'),BR(),BR(),'Day ',INPUT(_name='day'),BR(),BR(),'Week ',INPUT(_name='week',_value='*'),BR(),BR(),'Month ',INPUT(_name='month',_value='*'),BR(),BR(),INPUT(_type='submit'))
    if form.process().accepted:
        
        settings = form.vars.settings
        func = form.vars.functions
        minu=form.vars.min
        houru=form.vars.hour
        dayu=form.vars.day
        weeku=form.vars.week
        monthu=form.vars.month
        from sys import platform
        import os
        from crontab import CronTab
        if 'win' in platform:
            cron = CronTab(tabfile='filename.tab')
        elif 'linu' in platform:
            cron  = CronTab(user=True)
        dirname, filename = os.path.split(os.path.abspath(__file__))
        file_name = os.path.join(dirname,'scheduler.py')
        if int(func)==1:
            log='follow.txt'
        elif int(func)==2:
            log='unfollow.txt'
        elif int(func)==10:
            log='scraper.txt'
        log_name = os.path.join(dirname,'scheduler.py')
        ilog = os.path.join(dirname,log)
        job  = cron.new(command='python '+file_name+' '+settings+' '+func+'  >> '+ilog+' 2>&1')
 
        def ps(minu):
            if minu.isdigit():
                return minu
            else:
                if minu=='*':
                     return minu
                elif '/' in minu or '-' in minu:
                    try:
                        m=minu.split('/')
                        if m[0] == '*' and  m[1].isdigit()==True:
                            if len(m)>2:
                                return 'xyz'
                            else:
                                return minu
                    except:
                        m=minu.split('-')
                        if len(m)>2:
                                return 'xyz'
                    if m[0].isdigit() == False or  m[1].isdigit()==False:
                        return 'xyz'
                    else:
                        return minu
                else:
                    return 'xyz'
        minu=ps(minu)
        #response.flash = 'Please Check Your Minute'
        if minu=='xyz':
            response.flash = 'Please Check Your Minute'
        houru=ps(houru)
        if houru=='xyz':
            response.flash = 'Please Check Your Hour'
        dayu=ps(dayu)
        if dayu=='xyz':
            response.flash = 'Please Check Your Day'
        weeku=ps(weeku)
        if weeku=='xyz':
            response.flash = 'Please Check Your week'
        monthu=ps(monthu)
        if monthu=='xyz':
            response.flash = 'Please Check Your month'
        comm=str(minu)+' '+str(houru)+' '+str(dayu)+' ' +str(weeku)+' '+str(monthu)
        job.setall(comm)
        job.enable()
        response.flash = 'Jobs Added Susccefuly'
        cron.write()
        if 'linu' in platform:
                cron.write_to_user( user=True )
    return dict(form=form)
@auth.requires_login()
def index():
    images = db().select(db.accounts.ALL)
    return dict(images=images)

@auth.requires_login()
def import_account():
    form = FORM(TEXTAREA(_name='accounts', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    format=0
    if form.process().accepted:
        accounts = form.vars.accounts
        accounts=accounts.splitlines()
        datalist=['username','password','email','email_password','firstname','lastname','oauth_token','oauth_seceret','proxy']
        result=[]
        for i in accounts:
            if ':' in i:
                data={}
                spl=i.strip().split(':')
                if spl[0] and spl[1]:
                    for l in zip(datalist,spl):
                        data[l[0]]=l[1]
                    result.append(data)
                else:
                    format+=1
            else:
                    format+=1
        if result:
            res=db.accounts.bulk_insert(result)
            
            response.flash = 'parsed and inputted ',len(res),'and ', format,' not inputted'
        else:
            response.flash = 'We could not parse any Line Please check your input'
        #db.person.insert(name="Alex")
        #[{'name':'Alex'}, {'name':'John'}, {'name':'Tim'}]
    elif format > 0:
        response.flash = 'Some Accounts Format Have Errors',len(format)
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please Copy and Paste The Text to this Box'
    return dict(form=form)

@auth.requires_login()
def legacy_run():
    images = db().select(db.accounts.ALL)
    return dict(images=images)

@auth.requires_login()
def dashboard():
    
    images = db().select(db.accounts.ALL)
    return dict(images=images)

@auth.requires_login()
def settings():
   form = SQLFORM(db.globalsettings)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)



@auth.requires_login()
def manage_users():
    grid = SQLFORM.grid(db.auth_user)
    return locals()

@auth.requires_login()
def manage_accounts():
    grid = SQLFORM.grid(db.accounts)
    return locals()

@auth.requires_login()
def bot_output():
    grid = SQLFORM.grid(db.scheduler_run)
    return locals()

@auth.requires_login()
def run_bot():
    grid = SQLFORM.grid(db.scheduler_task)
    return locals()

@auth.requires_login()
def manage_user_scrapers():
    grid = SQLFORM.grid(db.users_to_scrape)
    return locals()


@auth.requires_login()
def manage_settings():
    grid = SQLFORM.grid(db.globalsettings)
    return locals()
@auth.requires_login()
def accounts():
   form = SQLFORM(db.accounts)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

@auth.requires_login()
def follow_logs():
    
    d=[]
    import os
    dirname, filename = os.path.split(os.path.abspath(__file__))
    file_name = os.path.join(dirname,'follow.txt')
    
    try:
        if request.vars.delete:
            os.remove(file_name)
            redirect(URL('logs'))
        with open(file_name) as e:
            for i in e:
                d.append(i)
    except:
        d=['No Logs Or You Have Not Used This Function']
    return dict(logs=d)

@auth.requires_login()
def unfollow_logs():
    d=[]
    import os
    dirname, filename = os.path.split(os.path.abspath(__file__))
    file_name = os.path.join(dirname,'unfollow.txt')
    try:
        if request.vars.delete:
            os.remove(file_name)
            redirect(URL('logs'))
        with open(file_name) as e:
            for i in e:
                d.append(i)
    except:
        d=['No Logs Or You Have Not Used This Function']
    return dict(logs=d)


@auth.requires_login()
def scraper_logs():
    d=[]
    import os
    dirname, filename = os.path.split(os.path.abspath(__file__))
    file_name = os.path.join(dirname,'scraper.txt')
    try:
        if request.vars.delete:
            os.remove(file_name)
            redirect(URL('logs'))
        with open(file_name) as e:
            for i in e:
                d.append(i)
    except:
        d=['No Logs Or You Have Not Used This Function']
    return dict(logs=d)
@auth.requires_login()
def logs():
    return dict()
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
