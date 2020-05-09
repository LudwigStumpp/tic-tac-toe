def unique_2d(list1): 
    # intilize an empty set
    my_set = set()

    # get number of rows
    rows = len(list1)
      
    # traverse for all rows
    for i in range(rows): 
        my_set.update(list1[i])
    
    return list(my_set)