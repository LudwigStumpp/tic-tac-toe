def unique_2d(list1): 
  
    # intilize a null list 
    unique_list = []

    # get number of rows and cols
    rows = len(list1)
    cols = len(list1[0])
      
    # traverse for all elements 
    for i in range(rows): 
        for j in range(cols):
            x = list1[i][j]
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x)
    
    return unique_list