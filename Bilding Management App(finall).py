# Call the libraries used in the code  
import pandas as pd    
import jdatetime 
import ast
import os
# to show print dataframe complitly
pd.set_option('display.max_columns', None)


# Functional definition for faster access to code output dataforms by calculation and reporting method.
def service_chose():
    print('\n\nPlease select your service by help from the bottom legend and type it.')
    first_command = input('\ntype "Cost" to -add a new cost-\ntype "Distribute" to -distribute costs-\ntype "Pay" to -pay cost-\ntype "Report" to -get report-\ntype "Finish" to -finish the app-\n: ').title()
    if first_command == 'Cost':
        cost_service()
    elif first_command == 'Distribute':
        distribution()
    elif first_command == 'Pay':
        pay_service()
    elif first_command == 'Report':
        get_report()
    elif first_command == 'Finish':
        return ('Thank you'+'   ****   '+'Good bye')
    return service_chose() 

# Receive input values
def cost_service():
# Receive fixed building information in csv file format and create the ability to add secondary values
    print('\n\nPlease select your cost by help from the bottom list and type it; if you don\'t find your cost in list type it.')
    cost1 = pd.read_csv(addres+'/data cost.csv')
    Servise_list = set(cost1['cost'])
    print('\n'+'{} to Service'.format(list(i for i in Servise_list)))
    Service = input('\nWhat is your service?\n: ').title()
    Cost = input('\nwhat is it cost?\n: ')
    ids = input('\nthis cost is from which id\'s?(pleas write an space beetwen each id)\n: ').split()
        

# Time : Enter the date and time of arrival of transaction values and convert the Gregorian date to solar using the jdatetime module.  
    now = jdatetime.datetime.today()
    mm = str(now.month)
    dd = str(now.day)
    yy = str(now.year)
    hr = str(now.hour)
    mi = str(now.minute)
    ss = str(now.second)  
    date = now = yy + "/" + mm + "/" + dd + " "+ hr + ":" + mi + ":" + ss
        
# Add information to the file created in the pravious function or return to the original saved values        
    cost1.loc[len(cost1['number'])+1] = [len(cost1['date'])+1,date,Service,Cost,ids]
    cost1.to_csv(addres + '/data cost.csv',index = False)
    continue_command = input('\n\nif you want to continue type "Continue" in otherwise to back to first page of app type "Service".\n: ').title()
        
    if continue_command == 'Continue':
        cost_service()  
      
    elif continue_command == 'Service':
        service_chose()
    return service_chose() 
 


# Convert csv file to dataform using Pandas
# Separate the function delet date befor a specified interval , or save previous information and add new payment information to the original csv file.
def pay_service():
    D3=pd.read_csv(addres + '/sahm bandi shode.csv')
    D1=pd.read_csv(addres + '/data of building.csv')
    new_pay = input('\n\nIf you want to continue with past data type "Past" or type "New" to remove past paid and start with new data.\n: ').title()
    
    
    if new_pay == 'New':
        for nam in D1['number']:
            d3 = D3[D3['name']==nam]
            d3 = d3.reset_index()
            d3= d3.drop(columns='index')
            d3['number'] = list(i for i in range(1,len(d3['date'])+1))
            new_columns = d3.columns.tolist()
            new_columns = new_columns[-1:] + new_columns[:-1]
            d3 = d3[new_columns]
            d3=d3.drop(columns='name')
            name_of_report = 'sorse of {}'.format(D1['name'][nam-1])
            d3.to_csv(addres + '/sorse/' + name_of_report + '.csv',index=False)
    
    
    elif new_pay == 'Past':
        print('\nyour last data is used.')
    person = input('\nWho pay cost?\n: ')
    D4 = pd.read_csv(addres + '/sorse' + '/sorse of ' + person + '.csv')
    print('\nThis is a report of {}\n'.format(person))
    print(D4)
    cost_pay = eval(input('\nWhich number of cost was paid?\n: '))
    paid_amount = eval(input('\nHow much was paid?\n: '))
    D4['paid'][cost_pay-1] += paid_amount
    D4.to_csv(addres + '/sorse/sorse of ' + person + '.csv',index=False)
    continue_command = input('if you want to continue type "Continue" in otherwise to back to first page of app type "Service".\n: ').title()
    
    
    if continue_command == 'Continue':
        pay_service()  
   
    elif continue_command == 'Service':
        service_chose()
    return service_chose() 


# Definition of a function whith the ability to determine how payments are calculated based on the number of people , area of units and other situations.
# Add columns to separate costs by units and payment time to data frame
def distribution():
    D1=pd.read_csv(addres + '/data of building.csv')
    D2=pd.read_csv(addres + '/data cost.csv')
    D3=pd.read_csv(addres + '/sahm bandi shode.csv')
    print('\n\nChose your cost from bottom table\n')
    print(D2)
    list_of_cost = input('\nwhich cost\'s you want to distribute?(pleas write an space beetwen each number of cost)\n: ').split()
    for N in list_of_cost:
        N = eval(N) -1
        s=int(input('\nfor cost "{}"; if you want to distribute by number of people type "1" , by area type "2", by equal form type "3" and by parkings type "4".\n: '.format(D2['cost'][N])))
        p=0
        d3= pd.DataFrame(columns=(['name','date','cost','mablagh','sahm','mode']))
 
        
# Calculate the ratio of amounts paid according to the number of people (like water bills)       
        if s==1:    
            while p<(len(ast.literal_eval(D2.loc[N,'name']))):
                    d3.loc[p,'name']=(ast.literal_eval(D2.loc[N,'name']))[p] 
                    d3.loc[p,'date']=D2.loc[N,'date']
                    d3.loc[p,'cost']=D2.loc[N,'cost']
                    d3.loc[p,'residents']=D1.loc[p,'residents']
                    d3.loc[p,'mablagh']=D2.loc[N,'mablagh']
                    d3.loc[p,'mode']='number of people'
                    p=p+1
            d3['sahm']=(d3['mablagh']/(d3.residents.sum()))*d3['residents']
            d3['paid']=0
            d3['debit']=0
            d3=d3.drop(columns='residents')
        
        
# Calculate the ratio of amounts paid in terms of unit area (like gas bills)     
        elif s==2:
            while p<(len(ast.literal_eval(D2.loc[N,'name']))):
                    d3.loc[p,'name']=(ast.literal_eval(D2.loc[N,'name']))[p] 
                    d3.loc[p,'date']=D2.loc[N,'date']
                    d3.loc[p,'cost']=D2.loc[N,'cost']
                    d3.loc[p,'area']=D1.loc[p,'area']
                    d3.loc[p,'mablagh']=D2.loc[N,'mablagh']
                    d3.loc[p,'mode']='area'
                    p=p+1
            d3['sahm']=(d3['mablagh']/(d3.area.sum()))*d3['area']
            d3['paid']=0
            d3['debit']=0
            d3=d3.drop(columns='area')
       
        
# Calculate payment amounts in equal proportions between related units (like charging a building)     
        elif s==3:
            while p<(len(ast.literal_eval(D2.loc[N,'name']))):
                    d3.loc[p,'name']=(ast.literal_eval(D2.loc[N,'name']))[p] 
                    d3.loc[p,'date']=D2.loc[N,'date']
                    d3.loc[p,'cost']=D2.loc[N,'cost']
                    d3.loc[p,'mablagh']=D2.loc[N,'mablagh']
                    d3.loc[p,'mode']='equal'
                    p=p+1
            d3['sahm']=d3['mablagh']/(len(ast.literal_eval(D2.loc[N,'name'])))
            d3['paid']=0
            d3['debit']=0
        
        
# Definition of a specific situation for parking costs in terms of the number of parking spaces per unit                
        elif s==4:
            while p<(len(ast.literal_eval(D2.loc[N,'name']))):
                    d3.loc[p,'name']=(ast.literal_eval(D2.loc[N,'name']))[p] 
                    d3.loc[p,'date']=D2.loc[N,'date']
                    d3.loc[p,'cost']=D2.loc[N,'cost']
                    d3.loc[p,'parkings']=D1.loc[p,'parkings']
                    d3.loc[p,'mablagh']=D2.loc[N,'mablagh']
                    d3.loc[p,'mode']='parkings'      
                    p=p+1
            d3['sahm']=(d3['mablagh']/(d3.parkings.sum()))*d3['parkings']
            d3['paid']=0
            d3['debit']=0
            d3=d3.drop(columns='parkings')
        D3=D3.append(d3)
    D3.to_csv(addres + '/sahm bandi shode.csv',index = False)     
    continue_command = input('\n\nif you want to continue type "Continue" in otherwise to back to first page of app type "Service"\n: ').title()
    
    if continue_command == 'Continue':
        distribution()
   
    elif continue_command == 'Service':
        service_chose()
    return service_chose() 



# Definition of a function to calculate the financial for each unit on the specified date of adding the financial balance column to the final output.        
# Describe function for quick access to common statistical details and general information about the data
def get_report():
    commond_from_report = input('\n\nIf you want to get report one by one type "Total" and if you want to get report of a special residents type "Special"\n: ').title()
    D1=pd.read_csv(addres + '/data of building.csv')
    if commond_from_report == 'Total':
        for nam in D1['number']:
            person_of_report = '{}'.format(D1['name'][nam-1])
            d3 = pd.read_csv(addres + '/sorse/sorse of ' + person_of_report + '.csv')
            d3['debit'] = d3['sahm'] - d3['paid']
            A = d3.describe()
            for j in d3.columns:
                for i in d3[j]:
                    if i==0 or i=='0':
                        if j in A:
                            A[j][0] -= 1
            A = A.drop(columns='number')
            now = jdatetime.datetime.today()
            mm = str(now.month)
            dd = str(now.day)
            yy = str(now.year)
            hr = str(now.hour)
            mi = str(now.minute)
            ss = str(now.second)  
            date = now = yy + "/" + mm + "/" + dd + " "+ hr + ":" + mi + ":" + ss
            d4 = {'number':"##",'date':date,'cost':'Total','mablagh':d3['mablagh'].sum(),'sahm':d3['sahm'].sum(),'mode':'##','paid':d3['paid'].sum(),'debit':d3['debit'].sum()}
            d3 = d3.append(d4,ignore_index=True)
            A.to_csv(addres + '/report/information of report/information of report of ' + person_of_report + '.csv')            
            d3.to_csv(addres + '/report/report of ' + person_of_report + '.csv',index=False)
    
    elif commond_from_report == 'Special':
        nam = input('\nwhich residents you want to get report?\n: ')
        d3 = pd.read_csv(addres + '/sorse/sorse of ' + nam + '.csv')
        d3['debit'] = d3['sahm'] - d3['paid']
        A = d3.describe()
        for j in d3.columns:
            for i in d3[j]:
                if i==0 or i=='0':
                    if j in A:
                        A[j][0] -= 1
        A = A.drop(columns='number')
        now = jdatetime.datetime.today()
        mm = str(now.month)
        dd = str(now.day)
        yy = str(now.year)
        hr = str(now.hour)
        mi = str(now.minute)
        ss = str(now.second)  
        date = now = yy + "/" + mm + "/" + dd + " "+ hr + ":" + mi + ":" + ss
        d4 = {'number':"##",'date':date,'cost':'Total','mablagh':d3['mablagh'].sum(),'sahm':d3['sahm'].sum(),'mode':'##','paid':d3['paid'].sum(),'debit':d3['debit'].sum()}
        d3 = d3.append(d4,ignore_index=True)
        A.to_csv(addres + '/report/information of report/information of report of ' + nam + '.csv')
        d3.to_csv(addres + '/report/report of ' + nam + '.csv',index=False)
    continue_command = input('if you want to continue type "Continue" in otherwise to back to first page of app type "Service"\n: ').title()
    if continue_command == 'Continue':
        get_report()
    elif continue_command == 'Service':
        service_chose()
    return service_chose() 

#function to start app
def start():
    new_start = input('If you want to continue with past data addres type "Past" or type "New" to remove past addres and take new data addres.\n: ').title()
    if new_start == 'New':
        print('\nBefor all things if you don\'t download bases of this app befor\nplease download te based file of building data from "https://s16.picofile.com/file/8424286726/data_of_building.csv.html" and fill it such as this file"https://s16.picofile.com/file/8424287376/data_of_building_example_.csv.html"\nthen please download base of data cost from"https://s17.picofile.com/file/8424287584/data_cost.csv.html"\nthen please download base of sahm bandi from "https://s17.picofile.com/file/8424376126/sahm_bandi_shode.csv.html"\nin the end please take them in a folder.')
        addres = input('\nPlease copy addres of folder\n: ').replace('\\','/')
        addres = pd.DataFrame({addres})
        addres_save = addres.to_csv('addres.txt',index=False)
        addres = [i for i in pd.read_csv('addres.txt')['0']][0]
        os.makedirs(addres + '/sorse')
        os.makedirs(addres + '/report')
        os.makedirs(addres + '/report' + '/information of report')
        print('\n\nHello \nWelcome to Building Management APP\nPlease select your service by help from the bottom legend and type it.')
        return service_chose() 

    elif new_start == 'Past':
        addres = [i for i in pd.read_csv('addres.txt')['0']][0]
        print('\n\nHello \nWelcome to Building Management APP.')
        return service_chose() 
    return start()
start()
