gold_path = r'E:\python\Numerical extraction\data\output(origin).txt'
out_path = r'E:\python\Numerical extraction\data\2022-07-18_output_5.txt'

with open(gold_path, 'r') as f:
    data_gold = f.read()

with open(out_path, 'r') as f:
    data_out = f.read()


data_gold_list = [i.strip(' ') for i in data_gold.split('\n') if i !=''] 
data_gold_list = data_gold_list[1:]
data_out_list = [i.strip(' ') for i in data_out.split('\n') if i !='']
data_out_list = data_out_list[1:]
n = 0
for i in range(len(data_gold_list)):
    data_gold_list_n = [i.strip(' ') for i in data_gold_list[i].split('\t') if i != '']
    data_out_list_n = [i.strip(' ') for i in data_out_list[i].split(' ') if i != '']
    data_out_list_n_a = []
    for i in data_out_list_n:
        if '.' in i:
            if i.split('.')[1] == '0':
                data_out_list_n_a.append(i.split('.')[0])
            
            elif i[-1] == '0':
                data_out_list_n_a.append(i[:-1])

            else:
                data_out_list_n_a.append(i)
                
        else:
            data_out_list_n_a.append(i)
    if data_gold_list_n != data_out_list_n_a:
        print(data_gold_list_n, data_out_list_n_a)
        n +=1
print(n)
