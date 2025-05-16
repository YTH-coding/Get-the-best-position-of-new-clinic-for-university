def hex_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    # 将十六进制转换为整数
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    return rgb

n = 1
while n==1:
    color = input("请输入颜色的HEX:")
    try:
        result = hex_rgb(color)
        print(result)
    except:
        print("颜色代码无效，请重新输入")
    
    n = int(input("输入1以继续程序:"))
    