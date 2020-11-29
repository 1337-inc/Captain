with open("project_data\\questions_file.txt") as q_file :
    mistake = 0
    for i in q_file :
        dolla = 0
        for j in i :
            if j == "$" :
                dolla += 1
        if dolla != 9 :
            mistake += 1
            print(f"mistake: {i}     dolla signs present: {dolla}")
    print(f"There were mistakes in {mistake} lines")