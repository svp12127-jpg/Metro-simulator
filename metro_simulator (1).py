#modules

#reading all data
def get_data():
    l=[]
    with open("metro_data.txt") as f:
        while True:
            line=f.readline()
            line = line.strip()   # remove \n
            if line:          
                s = line.split(',')
                l+=[s]
            else: # Reached the end of file
                break
    return l

#to dictionary
def to_dict():
    l=get_data()
    metro={}
    for i in l:
        color,station,destination,dur,change=i #5 values unpack
        
        #time to integers
        dur=int(dur)
        
        #create line if not present
        if color not in metro:
            metro[color]=[] #major key

         # append station details
        metro[color].append({
            "Station": station,
            "Destination": destination,
            "Time": dur,
            "Interchange": change})
    return metro
#Everything is of the form {1st Color: [{1st Station:'',Destination:'',Time: ,Interchange:''},....],2nd color:[{{1st Station:'',Destination:'',Time: ,Interchange:''},....],...}

#convert to mintues for calculations
def to_min(t): # t is of order HH:MM
    h, m = t.split(':')
    hr=int(h)
    min=int(m)
    return hr * 60 + min

#converting minutes back to time to display after doing calculations
def display_time(x): #x is in mins
    return f"{x//60:02d}:{x%60:02d}"

'''Peak and Non peak hours
Peak: 8:00-10:00  17:00-19:00
that is 480-600 mins and 1020-1140 mins
Peak - every 4 mins
Non peak - every 8 mins'''

#Metro Timings Module
#checking if peak or non peak hours
def interval(mins):
    if (mins>=480 and mins<=600) or (mins>=1020 and mins<=1140): #peak hours
        return 4
    else: #non peak hours
        return 8
    
#metro arrives at station
def metro_arrival(color,station,current_time):
    current=to_min(current_time)
    d=to_dict()
    for i in range(len(d[color])): #stations of a particular color
        if d[color][i]["Station"] == station:
            index = i
            break
    tot_time = 0
    for j in range(index):
        tot_time += d[color][j]["Time"] #time from inital to current station
    arrive_time=360+tot_time #360 because it starts at 6:00 am
    if current<=arrive_time: #they did not miss the metro
        return display_time(arrive_time)
    else: #missed the metro
        add=interval(current) #peak or non-peak hour
        diff=current - arrive_time #how much time passed since it arrived
        freq=diff//add #no. of metros that have passed
        next_time=arrive_time+(freq+1)*add #next metro time= time of arrival at station + [(no.of metros that passed) + 1] * addtime
        return display_time(next_time)

#Ride journey planner
#travel time
def travel_time(color,st,e):
    d=to_dict()
    tot_time=0
    for i in range(len(d[color])): #stations of a particular color
        if d[color][i]["Station"] == st: #starting point
            start=i
            break
    for j in range(len(d[color])):
        if d[color][j]["Station"] == e: #till where
            end=j
            break
    if start<end: #forward
        for k in range(start,end):
            tot_time+=d[color][k]["Time"]
    elif start>end: #backward
        for m in range(end,start):
            tot_time+=d[color][m]["Time"]
    else: #start=end
        pass
    return tot_time

#journey planner
def journey_planner():
    print()
    print("Welcome to Journey Planner!")
    source=input("Enter starting point:")
    dest=input("Enter destination:")
    time=input("Enter time of travel:")
    if to_min(time) < 360 or to_min(time) > 1380:  # before 6:00 AM or after 11:00 PM
        print("No service available at this time.")
        return
    d=to_dict()
    s_line=0
    d_line=0
    for k in d: #all stations of 1 particular color
        for info in d[k]:
            if source.lower()==info['Station'].lower(): #converting to lower case in case input is not given properly
                s_line=k
                break
        if s_line:
            break
    else:
        print("Source station not found!")

    for a in d:  
        for info in d[a]:  
            if dest.lower() == info['Station'].lower():  
                d_line = a 
                break
        if d_line:
            break
    else:
        print("Destination not found!")
    next_metro = metro_arrival(s_line, source, time)

    #next metro at source
    print("Next metro from", source, "is at:", next_metro)
    newtime=to_min(next_metro)
    subs=''
    for i in range(3):
        add = interval(newtime)          # recompute interval each time
        newtime += add                # next metro
        a=display_time(newtime)+', '
        subs+=a
    print("Subsequent metros at:",subs,'...')

    #source and destination are in same color line?
    #yes
    if s_line==d_line:
        s=travel_time(s_line,source,dest)
        print("Total travel time:",s)
        print("Total fare is Rs:",s) #1 rs. per min
        t=int(s)
        current=to_min(next_metro)
        reach_min=current+t
        reach=display_time(reach_min)
        reach=str(reach)
        print("You reach",dest,'at:',reach)
    
    #no
    else:
        def stationline(station):
            d=to_dict()
            lines = []
            for line, stations in d.items():  # d - metro dictionary
                for info in stations: #stations has all detials
                    if info['Station'] == station:
                        lines.append(line)
                        break
            return lines #stores the line color if station matches
        
        s_color=stationline(source)[0] #list to str
        d_color=stationline(dest)[0]
        
        d=to_dict()
        s=[] #source list
        de=[] #dest list
        common=[] #common station for interchange
        if s_color in d:
            for info in d[s_color]:
                station_names = info['Station']
                s.append(station_names)
        if d_color in d:
            for info in d[d_color]:
                station_names = info['Station']
                de.append(station_names)
        for b in s:
            for c in de:
                if b==c:
                    common.append(b)
                    
        if len(common)!=0: 
            #shortest route
            min=10**15
            go_to=''
            for i in common:
                #source to interchange
                stoi=travel_time(s_line, source, i)  # in minutes
                stoi_time=to_min(time) + stoi
                dis_stoi_time=display_time(stoi_time)

                #wait time
                next=metro_arrival(d_line,i,dis_stoi_time)
                wait=to_min(next)-stoi_time

                #inter to dest
                itodest = travel_time(d_line,i,dest)
                itodest_time=display_time(itodest)  #to "HH:MM"

                #total
                tot=stoi + wait +itodest
                if tot<min:
                    min=tot
                    go_to=i
                    
                    arriveatdest= display_time(to_min(next_metro)+min)
                    waiting=wait
            print("Best interchange:", go_to)
            print('Waiting time:',waiting,"minutes")
            print("You reach", dest, "at:",arriveatdest)   
            print("Total travel time:", min, "minutes") 
            print("Total fare:", min, "rs.") 

        else:
            print("No common station") 
def bonus1():
    #color
    print()
    print('You can view your map here!')
    print()
    global current_st
    current_st=input("Enter current station:")
    d=to_dict()
    #color
    f=False
    for color in d:
        for info in d[color]:
            if info['Station'].lower() == current_st.lower():
                print(color,'Line')
                f=True
                break
        #also checks for interchange stations
    if f==False:
        print("Station not found")
def bonus2(current_st):
    #map
    d=to_dict()
    for color in d:
        for i,info in enumerate(d[color]):
            if info['Station'].lower() == current_st.lower():
                print("Subsequent stations:")
                for j in d[color][i+1:]:
                    print(j['Station'])
                print()
                break

#main
while True:
    print()
    print("----- DELHI METRO ROUTE & SCHEDULE SIMULATOR -----")
    print()
    print("1. Journey Planner")
    print("2. Bonus Feature")
    print("3. Exit")
    choice=int(input("Enter choice:"))
    if choice==1:
        journey_planner()
    elif choice==2:
        bonus1()
        print()
        bonus2(current_st)
    elif choice==3:
        print("Thank you for visiting!")
        break
    else:
        print("Invalid choice. Please choose again")
        continue
