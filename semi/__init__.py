from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)


members = ['Akina','Daisuke','Douglus','Hayao',\
'Ken','Nozomi','Saison','Sakura','Suji','Takao','Takashi','Yuya']

break_time = 5
buffer = 10
class_time = 90



# Enter who attends
@app.route('/', methods=['GET','POST'])
def index():


    if request.method == 'GET':
        return render_template('index.html',members = members)
    else:
    
        import random
        import itertools
        
        # Initialize dictionary
        session['com'] = []
        session['pair'] = []
        session['timer'] = None
        session['r'] = 0
        session['timer_name'] = None

        session['attendance'] = request.form.getlist('attendance')
        random.shuffle(session['attendance'])
        session['attendance'].insert(0,'Aytun')
        
        session['rotation_list'] = [i for i in range(1,len(session['attendance'])+1)]

        session['n'] = len(session['rotation_list'])

        if session['n'] % 2 == 0:
            session['round'] = session['n']-1
        else:
            session['round'] = session['n']

        session['num_pair'] = int(session['n'] // 2)
        
        
        session['discussion_length'] = (class_time - break_time - buffer) / session['round']

        
    return redirect(url_for('aytun'))




# Generate permutations
@app.route('/Aytun')
def aytun():


    session['r'] += 1

    # When n is even
    ifsession['n'] % 2  == 0:
        if session['r'] == 1:

            # Assigning first pair which includes Aytun sensei
            session['pair'].append([session['rotation_list'][0],session['rotation_list'][1]])
            session['rotation_list'].remove(session['rotation_list'][0])
            session['rotation_list'].remove(session['rotation_list'][0])

            # Creating initial pair for first round (n/2 - 1 groups)
            for i in range(session['num_pair']-1):
                session['pair'].append([session['rotation_list'][0],session['rotation_list'][-1]])
                session['rotation_list'].remove(session['rotation_list'][0])
                session['rotation_list'].remove(session['rotation_list'][-1])

            session['com'] = [[session['attendance'][mem-1] for mem in p] for p in session['pair']]


        #Updating pair for each round from 2nd round up to (n-1)th round
        if 1 < session['r'] <= session['round']:

            if session['pair'][0][1] < session['n']:
                session['pair'][0][1] = session['pair'][0][1]+1
            else:
                session['pair'][0][1] = 2

            for i in range(session['num_pair']-1):
                if session['pair'][i+1][0] == session['n']:
                    session['pair'][i+1][0] = 2
                else:
                    session['pair'][i+1][0] = session['pair'][i+1][0]+1

                if session['pair'][i+1][1] == session['n']:
                    session['pair'][i+1][1] = 2
                else:
                    session['pair'][i+1][1] = session['pair'][i+1][1]+1


            session['com'] = [[session['attendance'][mem-1] for mem in p] for p in session['pair']]


    # When n is uneven
    else:
        if session['r'] == 1:

            # Creating initial pair for first round (n/2  groups)
            session['timer'] = session['rotation_list'][-1]
            session['rotation_list'].remove(session['rotation_list'][-1])

            for i in range(session['num_pair']):
                session['pair'].append([session['rotation_list'][0],session['rotation_list'][-1]])
                session['rotation_list'].remove(session['rotation_list'][0])
                session['rotation_list'].remove(session['rotation_list'][-1])

            session['com'] = [[session['attendance'][mem-1] for mem in p] for p in session['pair']]
            session['timer_name'] = session['attendance'][session['timer']-1]


        #Updating pair for each round from 2nd round up to (n-1)th round
        if 1 < session['r'] <= session['round']:
            session['timer'] -= 1


            for i in range(session['num_pair']):

                if session['pair'][i][0] == 1:
                    session['pair'][i][0] = session['n']
                else:
                    session['pair'][i][0] -= 1

                if session['pair'][i][1] == 1:
                    session['pair'][i][1] = session['n']
                else:
                    session['pair'][i][1] -= 1


            session['com'] = [[session['attendance'][mem-1] for mem in p] for p in session['pair']]
            session['timer_name'] = session['attendance'][session['timer']-1]

            
    return render_template('index.html', members = members, var_={{'attendance':session['attendance'],
                                                                   'rotation_list':session['rotation_list'],
                                                                   'com':session['com'],
                                                                   'discussion_length':session['discussion_length'],
                                                                   'n':session['n'],
                                                                   'round':session['round'],
                                                                   'num_pair':session['num_pair'],
                                                                   'pair':session['pair'],
                                                                   'timer':session['timer'],
                                                                   'r':session['r'],
                                                                   'timer_name':session['timer_name']}
})
