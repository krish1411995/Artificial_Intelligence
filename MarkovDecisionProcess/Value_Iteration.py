import numpy as np
import time
import sys

obstacle_placement = set()
length_of_grid = 0
start_location_car = []
end_location_car = []
final_state_reward = 100
obstacle_state_reward = -100
transition_value = -1
reward_matrix = {}
gamma = 0.9
list_of_direction = ["North", "South", "East", "West"]
t1 = time.time()



def readData():
    with open("input.txt", "r") as f:
        data = f.readlines()
        i = int(0)
        global length_of_grid
        global obstacle_placement
        length_of_grid= int(data[i].strip("\n").strip("\r"))
        i+=1
        number_of_cars = int(data[i].strip("\n").strip("\r"))
        i+=1
        number_of_obstacle = int(data[i].strip("\n").strip("\r"))
        i+=1
        for k in range(0 , number_of_obstacle):
            obstacle = data[i].strip("\n").strip("\r").split(",")
            obstacle_placement.add((int(obstacle[0]),int(obstacle[1])))
            i+=1
        for k in range(0, number_of_cars):
            location_start = data[i].strip("\n").strip("\r").split(",")
            start_location_car.append((int(location_start[0]), int(location_start[1])))
            i+=1
        for k in range(0, number_of_cars):
            location_end = data[i].strip("\n").strip("\r").split(",")
            end_location_car.append((int(location_end[0]), int(location_end[1])))
            i+=1
    # print("Placement of obstacle")
    # print(obstacle_placement)
    # print("start_location_car")
    # print(start_location_car)
    # print("end_location_car")
    # print(end_location_car)
    # if (0,2) in obstacle_placement:
    #     print("In the placement")
    # else:
    #     print("In not the placement")


def calculateRewardMatrix(end_location):
    global obstacle_placement
    reward_matrix={}
    for i in range(0,length_of_grid):
        for j in range(0, length_of_grid):
            if(j,i) in obstacle_placement:
                reward_matrix[(j,i)]=-101
            elif (j,i) == end_location:
                reward_matrix[(j,i)]=99
            else:
                reward_matrix[(j,i)]=-1
    return reward_matrix


def fetchUtilityValue(utililty, transition_cell, current_cell):
    if transition_cell in utililty:
        return utililty.get(transition_cell)
    else:
        return utililty.get(current_cell)


def getDirectionValue(previous_utility, current_cell, direction):
    (j,i) = current_cell
    # here the sum is north south east west
    if(direction=="North"):
        sum=np.float64(np.float64(0.7*fetchUtilityValue(previous_utility, (j,i-1), (j,i)))+np.float64(0.1*fetchUtilityValue(previous_utility,(j,i+1), (j,i)))+np.float64(0.1*fetchUtilityValue(previous_utility,(j+1,i),(j,i)))+np.float64(0.1*fetchUtilityValue(previous_utility,(j-1,i),(j,i))))
    elif(direction=="South"):
        sum = np.float64(np.float64(0.1 * fetchUtilityValue(previous_utility, (j, i - 1), (j,i))) + np.float64(0.7 * fetchUtilityValue(previous_utility, (j, i + 1),(j,i))) + np.float64(0.1 * fetchUtilityValue(previous_utility, (j + 1, i),(j,i))) + np.float64(0.1 * fetchUtilityValue(previous_utility, (j - 1, i),(j,i))))
    elif(direction=="East"):
        sum = np.float64(np.float64(0.1 * fetchUtilityValue(previous_utility, (j, i - 1),(j,i))) + np.float64(0.1 * fetchUtilityValue(previous_utility, (j, i + 1),(j,i))) + np.float64(0.7 * fetchUtilityValue(previous_utility, (j + 1, i),(j,i))) + np.float64(0.1 * fetchUtilityValue(previous_utility, (j - 1, i),(j,i))))
    else:
        sum = np.float64(np.float64(0.1 * fetchUtilityValue(previous_utility, (j, i - 1),(j,i))) + np.float64(0.1 * fetchUtilityValue(previous_utility, (j, i + 1),(j,i))) + np.float64(0.1 * fetchUtilityValue(previous_utility, (j + 1, i),(j,i))) + np.float64(0.7 * fetchUtilityValue(previous_utility, (j - 1, i),(j,i))))
    # print(sum)
    return (sum, direction)

def getUtility(previous_utility, reward_matrix, policy, end_location_car):
    global gamma
    new_utility ={}
    for i in range(0,length_of_grid):
        for j in range(0,length_of_grid):
            if end_location_car==(j,i):
                #print((j,1))
                new_utility[(j,i)]=99
                policy[(j,i)]=None
                continue
            max_direction_list =[]
            value_north = getDirectionValue(previous_utility, (j,i), "North")
            #print(value_north)
            max_direction_list.append(value_north)
            value_south = getDirectionValue(previous_utility, (j,i), "South")
            max_direction_list.append(value_south)
            value_east = getDirectionValue(previous_utility, (j,i), "East")
            max_direction_list.append(value_east)
            value_west = getDirectionValue(previous_utility, (j,i), "West")
            max_direction_list.append(value_west)
            # print(max_direction_list[0])
            maximum_value = max(max_direction_list, key=lambda item:item[0])
            policy[(j,i)]=maximum_value[1]
            # print(maximum_value)
            new_utility[(j,i)] = reward_matrix.get((j,i))+(gamma*maximum_value[0])
    # print (new_utility)
    #print (policy)
    return (new_utility, policy)





def getFinalPolicy(utility1, reward_matrix, end_location_car):
    policy_intial={}
    old_utility = utility1
    ## here we will have the for loop to check the the old vs new utility value
    flag = False
    epsilon = 0.1
    delta = epsilon*((1-gamma)/gamma)
    while(flag==False):
        utility_and_policy = getUtility(old_utility, reward_matrix, policy_intial, end_location_car)
        new_utility = utility_and_policy[0]
        policy_intial=utility_and_policy[1]

        initial_flag = True

        for i in range(0, length_of_grid):
            for j in range(0, length_of_grid):
                if end_location_car==(j,i):
                    continue
                if abs(new_utility.get((j,i))-old_utility.get((j,i))) > delta:
                    initial_flag = False
                    break
            if initial_flag == False:
                break

        if initial_flag==False:
            old_utility = new_utility.copy()
        else:
            break
    return policy_intial








def turnLeft(current_move):
    if current_move=="North":
        return "West"
    elif current_move=="South":
        return "East"
    elif current_move=="East":
        return "North"
    elif current_move=="West":
        return "South"
    else:
        return None


def transit(policy, state, direction):
    if direction=="North":
        a = (state[0], state[1]-1)
    elif direction=="South":
        a = (state[0], state[1]+1)
    elif direction=="East":
        a =  (state[0]+1, state[1])
    elif direction=="West":
        a = (state[0]-1, state[1])

    if a in policy:
        return a
    else:
        return state


def getFinalReward(reward_matrix, final_policy, start_location, end_location):
    reward_array = np.zeros(10)
    for j in range(0,10):
        pos = start_location
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k = 0

        while pos != end_location:
            move = final_policy.get(pos)
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turnLeft(turnLeft(move))
                    else:
                        move = turnLeft(turnLeft(turnLeft(move)))

                else:
                    move = turnLeft(move)
            pos=transit(final_policy, pos, move)
            reward_array[j]+=reward_matrix.get(pos)
            k += 1
    return np.mean(reward_array)

def main():
    global t1
    outputFile = open("output.txt", "w")
    readData()
    result_map = np.zeros(len(start_location_car))
    for i in range(0,len(start_location_car)):
        if start_location_car[i]==end_location_car[i]:
            sum = 100
        else:
            if time.time()-t1>175:
                sys.exit(0)
            reward_matrix = calculateRewardMatrix(end_location_car[i])
            utility1 = reward_matrix.copy()
            #print(reward_matrix)
            final_policy = getFinalPolicy(utility1, reward_matrix, end_location_car[i])
            #print(final_policy)
            sum = getFinalReward(reward_matrix, final_policy, start_location_car[i], end_location_car[i])
            #print(int(sum))
        result_map[i]=sum
    result_map=np.floor(result_map)
    result_map_final = result_map.astype(int)
    for i in result_map_final:
        outputFile.write(str(i)+"\n")

    outputFile.close()
    #     for i in final_policy.keys():
    #         if (final_policy.get(i)=="North"):
    #             outputFile.write(str(i)+": (0, -1)"+"\n")
    #         elif (final_policy.get(i)=="South"):
    #             outputFile.write(str(i) + ": (0, 1)" + "\n")
    #         elif (final_policy.get(i)=="East"):
    #             outputFile.write(str(i) + ": (1, 0)" + "\n")
    #         elif (final_policy.get(i)=="West"):
    #             outputFile.write(str(i) + ": (-1, 0)" + "\n")
    #         else:
    #             outputFile.write(str(i) + ": None" + "\n")
    # outputFile.close()




if __name__ == '__main__':
    main()
    # print(time.time()-t1)

