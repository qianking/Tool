import math

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_split_pair(p_x, p_y, delta, best_pair):
    ln_x = len(p_x)  # store length - quicker
    mx_x = p_x[ln_x // 2][0]  # select midpoint on x-sorted array
    
    # Create a subarray of points not further than delta from midpoint on x-sorted array
    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
    
    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length - quicker
    for i in range(ln_y - 1):
        for j in range(i+1, min(i + 7, ln_y)):  # make loop run from i+1 to i+7
            p, q = s_y[i], s_y[j]  # store points
            dst = calculate_distance(p, q)  # compute distance
            if dst < best:
                best_pair = p, q
                best = dst  # update best distance
    return best_pair

def closest_pair_recursive(p_x, p_y):
    ln_x = len(p_x)  # store length - quicker
    # base case
    if ln_x <= 3:
        return min([((p_x[i], p_x[j]), calculate_distance(p_x[i], p_x[j]))
                    for i in range(ln_x-1)
                    for j in range(i+1, ln_x)],
                   key=lambda x: x[1])[0]
    # Recursive D&C part
    mid = ln_x // 2  # compute midpoint
    q_x = p_x[:mid]  # split p_x into two halves
    r_x = p_x[mid:]
    
    # Determine midpoint on x-axis
    midpoint = p_x[mid][0]  
    
    # split p_y into two halves
    q_y = list(filter(lambda x: x[0] <= midpoint, p_y))
    r_y = list(filter(lambda x: x[0] > midpoint, p_y))
    
    # Call recursively both arrays after split
    (p1, q1) = closest_pair_recursive(q_x, q_y)
    (p2, q2) = closest_pair_recursive(r_x, r_y)
    
    # Determine smaller distance between points of 2 arrays
    if calculate_distance(p1, q1) < calculate_distance(p2, q2):
        delta = calculate_distance(p1, q1)
        best_pair = p1, q1
    else:
        delta = calculate_distance(p2, q2)
        best_pair = p2, q2
    
    # Call function to account for points on the boundary
    (p3, q3) = closest_split_pair(p_x, p_y, delta, best_pair)
    
    # Determine smallest distance for the array
    if calculate_distance(p3, q3) < delta:
        return p3, q3
    else:
        return best_pair

def closest_pair(points):
    p_x = sorted(points, key=lambda x: x[0])  # sort array of points by the x coordinate
    p_y = sorted(points, key=lambda x: x[1])  # sort array of points by the y coordinate
    return closest_pair_recursive(p_x, p_y)


if "__main__" == __name__:
    led_points = {'A_00': (71.0, 93.5), 'A_01': (232.5, 94.0), 'A_02': (335.5, 93.5), 'A_03': (441.0, 91.0), 'A_04': (544.0, 91.0), 'A_05': (128.0, 147.5), 'A_06': (233.5, 146.0), 'A_07': 
(337.5, 144.0), 'A_08': (443.0, 144.0), 'A_09': (548.0, 141.5), 'A_10': (127.5, 200.0), 'A_11': (233.5, 198.5), 'A_12': (338.0, 196.5), 'A_13': (442.5, 196.0), 'A_14': (546.5, 194.0), 'A_15': (127.5, 252.0), 'A_16': (234.0, 252.0), 'A_17': (338.5, 248.5), 'A_18': (442.5, 248.0), 'A_19': (550.5, 246.5), 'A_20': (130.5, 304.0), 'A_21': (234.0, 303.5), 'A_22': (339.0, 301.0), 'A_23': (443.5, 300.5), 'A_24': (545.0, 300.0), 'A_25': (134.0, 353.0), 'A_26': (236.0, 355.5)}
    print(closest_pair(list(led_points.values())))

# Example usage:
# led_points = {...}  # your points go here
# print(closest_pair(list(led_points.values())))
