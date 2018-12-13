import numpy as np
import time
dict_fetch_value_user={}
numpy_spaces=np.full(7, 0, int)
numpy_beds=np.full(7,0,int)
total_people_pool=set()
total_people_SPLA_pool=[]
total_people_LAHSA_pool=[]
final_output=""
startTime = time.time()





def readData():
    with open("input.txt", "r") as f:
        data = f.readlines()
        i=int(0)
        global numpy_beds
        global numpy_spaces
        number_of_beds=int(data[i].strip("\n").strip("\r"))
        i += 1
        numpy_beds=np.full(7, number_of_beds, int)
        number_of_spaces=int(data[i].strip("\n").strip("\r"))
        if number_of_spaces==0 and numpy_beds==0:
            return
        numpy_spaces = np.full(7, number_of_spaces, int)
        i += 1
        people_assigned_LAHSA=int(data[i].strip("\n").strip("\r"))
        i += 1
        list_people_assigned_LAHSA=[]
        for j in range(0,people_assigned_LAHSA):
            list_people_assigned_LAHSA.append(data[i].strip("\n").strip("\r"))
            i += 1
        people_assigned_SPLA = int(data[i].strip("\n").strip("\r"))
        i += 1
        list_people_assigned_SPLA = []
        for j in range(0,people_assigned_SPLA):
            list_people_assigned_SPLA.append(data[i].strip("\n").strip("\r"))
            i += 1
        total_people=int(data[i].strip("\n").strip("\r"))
        if total_people==0:
            return
        #print total_people
        i += 1
        global total_people_pool#set of the number of available participants
        global total_people_SPLA_pool# set of particiapnts qualified for SPLA
        global total_people_LAHSA_pool#list of participants qualified for LAHSA
        global dict_fetch_value_user#dictionary to fetch the participant by id and get values contains tuples with t[1] is total efficieny and t[2] is days needed for occupancy
        for j in range(0,total_people):
            if list_people_assigned_SPLA.__contains__(data[i][0:5]):#check whether the people assigned the parking
                numpy_spaces = numpy_spaces-np.array(list(data[i][13:20].strip("\n").strip("\r")),int) #subtract with the spaces left
                i += 1
                continue
            elif list_people_assigned_LAHSA.__contains__(data[i][0:5]):#check whether the people assigned the beds
                numpy_beds = numpy_beds - np.array(list(data[i][13:20].strip("\n").strip("\r")), int) #subtract with the beds left
                i += 1
                continue
            #print ("hello")

            if data[i][10:11] == 'N' and data[i][11:12] == 'Y' and data[i][12:13] == 'Y':#check the conditions for SPLA
                total_people_SPLA_pool.append(data[i][0:5])
                value_np= np.array(list(data[i][13:20].strip("\n").strip("\r")),int)
                dict_fetch_value_user[data[i][0:5]] = (np.count_nonzero(value_np),value_np)
                if data[i][5:6] == 'F' and int(data[i][6:9])>17 and data[i][9:10] == 'N':#check conditions for LASPA
                    total_people_LAHSA_pool.append(data[i][0:5])
                total_people_pool.add(data[i][0:5].strip("\n").strip("\r"))

            elif data[i][5:6] == 'F' and int(data[i][6:9])>17 and data[i][9:10] == 'N':#check conditions for LASPA
                value_np = np.array(list(data[i][13:20].strip("\n").strip("\r")),int)
                dict_fetch_value_user[data[i][0:5]] = (np.count_nonzero(value_np), value_np)
                total_people_LAHSA_pool.append(data[i][0:5])
                total_people_pool.add(data[i][0:5])
            i += 1 


    #print(dict_fetch_value_user)
    # print (total_people_pool)
    # print (total_people_SPLA_pool)
    # print (total_people_LAHSA_pool)
    # print (dict_fetch_value_user)
    # print ("number of spaces", number_of_spaces)
    # print ("number of beds", number_of_beds)


depth1=3
maxDepth = 0
count=0

#function to check the number of days and places left with the organisation
def checkAndSubtractSpla(key):
    np_days = dict_fetch_value_user.get(key)[1]
    temp=np.full(7,0,int)
    np.put(temp,[0,1,2,3,4,5,6],np.subtract(numpy_spaces, np_days))
    if np.where(temp<0)[0].size !=0:
        return False
    else:
        #print("this is value of temp", temp)
        np.put(numpy_spaces, [0, 1, 2, 3, 4, 5, 6], temp)
        return True

def checkoutTime():
    global startTime
    endTime = time.time()-startTime
    if endTime >= 167:
        getOutput()
        exit(0)

#function to check the number of days and places left with the organisation
def checkAndSubtractLahsa(key):
    np_days = dict_fetch_value_user.get(key)[1]
    temp = np.full(7, 0, int)
    np.put(temp, [0, 1, 2, 3, 4, 5, 6], np.subtract(numpy_beds, np_days))
    if np.where(temp < 0)[0].size != 0:
        return False
    else:
        np.put(numpy_beds, [0, 1, 2, 3, 4, 5, 6], temp)
        return True

def addSpla(key):
    np_days = dict_fetch_value_user.get(key)[1]
    np.put(numpy_spaces, [0, 1, 2, 3, 4, 5, 6], np.add(numpy_spaces, np_days))

def addLahsa(key):
    np_days = dict_fetch_value_user.get(key)[1]
    np.put(numpy_beds, [0, 1, 2, 3, 4, 5, 6], np.add(numpy_beds, np_days))




class GameNode(object):
    def __init__(self, name, lahsa_score=0, spla_score=0, parent=None):
        self.Name =name
        self.lahsa_score=lahsa_score
        self.spla_score=spla_score
        self.parent = parent
        self.children = []
        self.value = spla_score-lahsa_score

    def addChild(self, childNode):
        self.children.append(childNode)




def play():

    global root
    root = GameNode("root")
    global depth1
    # while(depth1<20):
    global count

    # if (count==depth1 or len(spla_pool)==0):
    #     string_append.append(string1)
    #     return


    # ---- constructing a root node
    global total_people_SPLA_pool
    global total_people_LAHSA_pool
    global temp
    abc0=temp
    for key in abc0:
        if (count == depth1):
            return
        flag = 0

        # string1+=key
        if not checkAndSubtractSpla(key):
            continue
        #print("new")
        #print (key)




        current_node = GameNode(key, lahsa_score=root.lahsa_score, spla_score=dict_fetch_value_user.get(key)[0], parent=root)
        root.addChild(current_node)
        # print("print current", current_node.Name)
        # print("print current node's parent", current_node.parent.Name)
        # print("print current node's children", current_node.children)
        # print("print current node's spla", current_node.spla_score)
        # print("print current node' lahsa", current_node.lahsa_score)
        # print("value of the current_node", current_node.value)




        count += 1
        total_people_SPLA_pool.remove(key)
        if key in total_people_LAHSA_pool:
            total_people_LAHSA_pool.remove(key)
            flag = 1
        playLahsa(count, 0, 0, current_node)
        #print ("backtracking")
        addSpla(key)
        count -= 1
        total_people_SPLA_pool.append(key)
        if flag == 1:
            total_people_LAHSA_pool.append(key)

    return





#alternating recursion which allows spla and lahsa to play turn by turn
def playSpla(count, spla, lahsa, parent):
    global total_people_SPLA_pool
    global total_people_LAHSA_pool
    checkoutTime()


    if (count==depth1 or len(total_people_SPLA_pool)==0):
        #string_append.append(string1)
        return
    abc = total_people_SPLA_pool[:]
    for key in abc:
        if (count==depth1):
            return
        flag=0
        #string1+=key
        if not checkAndSubtractSpla(key):
            continue
        #print (key)



        value_to_pass = parent.spla_score + dict_fetch_value_user.get(key)[0]
        current_node = GameNode(key, lahsa_score=parent.lahsa_score, spla_score=value_to_pass, parent=parent)
        parent.addChild(current_node)
        # print("print current", current_node.Name)
        # print("print current node's parent", current_node.parent.Name)
        # print("print current node's children", current_node.children)
        # print("print current node's spla", current_node.spla_score)
        # print("print current node' lahsa", current_node.lahsa_score)
        # print("value of the current_node", current_node.value)




        total_people_SPLA_pool.remove(key)
        count += 1
        if key in total_people_LAHSA_pool:
            total_people_LAHSA_pool.remove(key)
            flag=1
        playLahsa(count, spla, lahsa, current_node)
        #print ("backtracking")
        addSpla(key)
        count -= 1
        total_people_SPLA_pool.append(key)
        if flag==1:
            total_people_LAHSA_pool.append(key)

    return




def playLahsa(count, spla, lahsa, parent):
    global total_people_LAHSA_pool
    global total_people_SPLA_pool
    
    if (len(total_people_LAHSA_pool) == 0 and count !=depth1):
        count += 1



        current_node=GameNode("dummy", lahsa_score=parent.lahsa_score, spla_score=parent.spla_score, parent=parent)
        parent.addChild(current_node)
        # print("print current", current_node.Name)
        # print("print current node's parent",current_node.parent.Name)
        # print("print current node's children",current_node.children)
        # print("print current node's spla", current_node.spla_score)
        # print("print current node' lahsa", current_node.lahsa_score)
        # print("value of the current_node", current_node.value)



        playSpla(count, spla, lahsa, current_node)

    if (count==depth1 or len(total_people_LAHSA_pool)==0):
        #string_append.append(string1)
        return
    abc1= total_people_LAHSA_pool[:]
    for key in abc1:
        if (count==depth1):
            return
        flag=0
        #string1+=key
        if not checkAndSubtractLahsa(key):
            continue


        value_to_pass=parent.lahsa_score+dict_fetch_value_user.get(key)[0]
        current_node = GameNode(key, lahsa_score=value_to_pass, spla_score=parent.spla_score, parent=parent)
        parent.addChild(current_node)
        # print("print current", current_node.Name)
        # print("print current node's parent", current_node.parent.Name)
        # print("print current node's children", current_node.children)
        # print("print current node's spla", current_node.spla_score)
        # print("print current node' lahsa", current_node.lahsa_score)
        # print("value of the current_node", current_node.value)


        #print (key)
        count += 1
        total_people_LAHSA_pool.remove(key)
        if key in total_people_SPLA_pool:
            total_people_SPLA_pool.remove(key)
            flag=1

        playSpla(count, spla, lahsa, current_node)
        #print ("backtracking")
        addLahsa(key)
        count -= 1
        total_people_LAHSA_pool.append(key)
        if flag==1:
            total_people_SPLA_pool.append(key)

    return


#achieving aplha beta pruning
class AlphaBeta:
    def __init__(self, game_tree):
        self.game_tree = game_tree
        return

    def alpha_beta_search(self, node):
        global final_output
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        if self.isTerminal(node):
            return self.getUtility(node)

        nextstate = self.getSuccessors(node)
        best_state = None
        for state in nextstate:
            value = self.minimize(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        final_output=best_state.Name
        return best_state

    def minimize(self, node, alpha, beta):

        infinity = float('inf')
        value = infinity
        if self.isTerminal(node):
            return self.getUtility(node)

        nextstate = self.getSuccessors(node)
        for state in nextstate:
            value = min(value, self.maximize(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value



    def maximize(self, node, alpha, beta):

        infinity = float('inf')
        value = -infinity
        if self.isTerminal(node):
            return self.getUtility(node)

        nextstate = self.getSuccessors(node)
        for state in nextstate:
            value = max(value, self.minimize(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def getUtility(self, node):
        return node.value



    def isTerminal(self, node):
        return len(node.children) == 0



    def getSuccessors(self, node):
        return node.children

def getOutput():
    outputFile = open("output.txt", "w")
    outputFile.write(str(final_output))

class GameTree:
    def __init__(self):
        self.root = None
        return


def main():
    readData()
    global root
    global temp
    global depth1
    global total_people_SPLA_pool
    global total_people_LAHSA_pool
    global maxDepth
    maxDepth = max(len(total_people_SPLA_pool), len(total_people_LAHSA_pool))*2 + 1 #max depth is set because we wont achiecve new answers after this value

    temp=total_people_SPLA_pool[:]

    
    #logic for iterative deepning 
    while depth1 <= maxDepth:
        
        play()

        aplha_beta = AlphaBeta(root)
        b=aplha_beta.alpha_beta_search(root)
        depth1 = depth1+2
        getOutput()
        del root
        

        del b

    getOutput()

if __name__ == '__main__':

    main()
