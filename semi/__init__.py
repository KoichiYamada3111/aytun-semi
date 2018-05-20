from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)



members = ['Akina','Daisuke','Douglus','Hayao',\
'Ken','Nozomi','Saison','Sakura','Suji','Takao','Takashi','Yuya',]

num_mem = len(members)

var = {'attendance':[], 'rotation_list':[], 'com':[],
'discussion_length':0, 'n':None, 'round':0,
'num_pair':0, 'pair':[], 'timer':None, 'r':0,
'timer_name':None}


@app.route('/', methods=['GET','POST'])
def index():



    if request.method == 'GET':
        return render_template('index.html',members = members)
    else:
    
        import random
        import itertools
        
        var['discussion_length'] = 0
        var['com'] = []
        var['round'] = 0
        var['num_pair'] = 0
        var['pair'] = []
        var['timer'] = None
        var['r'] = 0
        var['timer_name'] = None


        #mem = n()

        var['attendance'] = request.form.getlist('attendance')

        random.shuffle(var['attendance'])
        var['attendance'].insert(0,'Aytun')
        #print(attendance)


        #print(combination,'//',len(combination))

        var['rotation_list'] = [i for i in range(1,len(var['attendance'])+1)]

        var['n'] = len(var['rotation_list'])

        num_combination = var['n'] * var['n']-1/ 2
        if var['n'] % 2 == 0:
            var['round'] = var['n']-1  # num_combination / (var['n'] / 2)
        else:
            var['round'] = var['n']

        var['num_pair'] = int(var['n'] // 2)
        
        break_time = 5
        buffer = 10
        class_time = 90
        
        var['discussion_length'] = (class_time - break_time - buffer) / var['round']

        
    return redirect(url_for('aytun'))





@app.route('/Aytun')
def aytun():


    #print('How many rounds are there?:',round,'times')
    #print('How many minutes for each round?:',discussion_length,'minutes','\n')

    var['r'] += 1

    # When n is even
    if var['n'] % 2  == 0:
        if var['r'] == 1:

            # Assigning first pair which includes Aytun sensei
            var['pair'].append([var['rotation_list'][0],var['rotation_list'][1]])
            var['rotation_list'].remove(var['rotation_list'][0])
            var['rotation_list'].remove(var['rotation_list'][0])

            # Creating initial pair for first round (n/2 - 1 groups)
            for i in range(var['num_pair']-1):
                var['pair'].append([var['rotation_list'][0],var['rotation_list'][-1]])
                var['rotation_list'].remove(var['rotation_list'][0])
                var['rotation_list'].remove(var['rotation_list'][-1])

            #print("------------------------------------------\
            #\n","This is 1st round"'\n', [[attendance[mem-1] for mem in p] for p in pair],'\n')
            #input("Please press Enter to continue:\n")
            var['com'] = [[var['attendance'][mem-1] for mem in p] for p in var['pair']]


        #Updating pair for each round from 2nd round up to (n-1)th round
        if 1 < var['r'] <= var['round']:

            if var['pair'][0][1] < var['n']:
                var['pair'][0][1] = var['pair'][0][1]+1
            else:
                var['pair'][0][1] = 2

            for i in range(var['num_pair']-1):
                if var['pair'][i+1][0] == var['n']:
                    var['pair'][i+1][0] = 2
                else:
                    var['pair'][i+1][0] = var['pair'][i+1][0]+1

                if var['pair'][i+1][1] == var['n']:
                    var['pair'][i+1][1] = 2
                else:
                    var['pair'][i+1][1] = var['pair'][i+1][1]+1


            #print("------------------------------------------\
            #\n","This is round", r+2,'\n', [[attendance[mem-1] for mem in p] for p in pair],'\n')
            #input("Please press Enter to continue:\n")
            var['com'] = [[var['attendance'][mem-1] for mem in p] for p in var['pair']]


    # When n is uneven
    else:
        if var['r'] == 1:

            # Creating initial pair for first round (n/2  groups)
            var['timer'] = var['rotation_list'][-1]
            var['rotation_list'].remove(var['rotation_list'][-1])

            for i in range(var['num_pair']):
                var['pair'].append([var['rotation_list'][0],var['rotation_list'][-1]])
                var['rotation_list'].remove(var['rotation_list'][0])
                var['rotation_list'].remove(var['rotation_list'][-1])

            #print("------------------------------------------\
            #\n","This is 1st round"'\n', [[attendance[mem-1] for mem in p] for p in pair], \
            #'Timer:',attendance[timer-1])
            #input("Please press Enter to continue:\n")
            var['com'] = [[var['attendance'][mem-1] for mem in p] for p in var['pair']]
            var['timer_name'] = var['attendance'][var['timer']-1]


        #Updating pair for each round from 2nd round up to (n-1)th round
        if 1 < var['r'] <= var['round']:
            var['timer'] -= 1


            for i in range(var['num_pair']):

                if var['pair'][i][0] == 1:
                    var['pair'][i][0] = var['n']
                else:
                    var['pair'][i][0] -= 1

                if var['pair'][i][1] == 1:
                    var['pair'][i][1] = var['n']
                else:
                    var['pair'][i][1] -= 1


            #print("------------------------------------------\
            #\n","This is round", r+2,'\n', [[attendance[mem-1] for mem in p] for p in pair],\
            #'Timer:',attendance[timer-1],'\n')
            #input("Please press Enter to continue:\n")
            var['com'] = [[var['attendance'][mem-1] for mem in p] for p in var['pair']]
            var['timer_name'] = var['attendance'][var['timer']-1]
    
    return render_template('index.html', members = members, var_=var)
