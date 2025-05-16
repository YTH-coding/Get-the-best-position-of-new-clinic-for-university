import math

def tuple_float(file_address)->dict:
    """
    文件里面保存的数据格式：
    坐标元组:浮点数据
    函数返回字典：
    {坐标元组:浮点数据,
    ...}
    """
    result = dict()
    with open(file_address, "r") as file:
        for line in file:
            if ":" in line:
                point_str, dist_str = line.strip().split(":")
                point = eval(point_str.strip())
                value = eval(dist_str.strip())
                result[point] = value
    print(f"文件{file_address}导入成功")
    return result

def xy(file_address)->list:
    """
    文件里面保存的数据格式：
    x坐标,y坐标
    函数返回列表：
    [坐标元组,
    ...]
    """
    result = list()
    with open(file_address,"r") as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            result.append((int(x),int(y)))
    print(f"文件{file_address}导入成功！")
    return result

def xy_string(file_address)->dict:
    """
    文件里面保存的数据格式：
    x坐标,y坐标,字符串
    函数返回字典：
    {坐标元组:字符串,
    ...}
    """
    result = dict()
    with open(file_address,"r",encoding='utf-8') as file:
        for line in file:
            x, y, name = line.strip().split(',')
            result[(int(float(x)),int(float(y)))] = name
    print(f"文件{file_address}导入成功！")
    return result

def tuple_list(file_address)->dict:
    """
    文件里面保存的数据格式：
    坐标元组:[坐标元组,坐标元组，...]
    函数返回字典：
    {坐标元组:{坐标元组1:距离1,坐标元组2:距离2,...},
    ...}
    """
    result = dict()
    with open(file_address,"r") as file:
        for line in file:
            p1, neigh = line.strip().split(":")
            p_now = eval(p1)
            p_neigh_s = eval(neigh)
            temp = dict()
            for p in p_neigh_s:
                distance = math.dist(p, p_now)
                temp[p] = distance
            result[p_now] = temp
    print(f"文件{file_address}导入成功！")
    return result

def string_float(file_address)->dict:
    """
    文件里面保存的数据格式：
    字符串:浮点数据
    函数返回字典：
    {字符串:浮点数据，
    ...}
    """
    result = dict()
    with open(file_address, "r",encoding="utf-8") as file:
        for line in file:
            string_data, float_data = line.strip().split(":")
            result[string_data] = float(float_data)
    print(f"文件{file_address}导入成功！")
    return result
            