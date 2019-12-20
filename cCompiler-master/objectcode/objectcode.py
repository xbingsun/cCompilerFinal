import os
import re

regs = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7']
table = {}  # 存储变量与寄存器的对应关系
reg_ok = {}  # 存储各个寄存器的使用情况
variables = []  # 存储所有还未被寄存器替代的temp变量(临时变量)
arrayDefinition = ['.align 2\n']  # .data代码段 分配数组空间
arrayAssign = ''
flag = 0  # 数组第一次调用


def Load_Var(Inter):  # 找到所有须用寄存器替代的变量
    global variables
    temp_re = '(temp\d+)'
    for line in Inter:
        temps = re.findall(temp_re, ' '.join(line))
        variables += temps


def Load_Inter(filename):  # 分割生成的中间代码，将每行代码转成一个存储各个关键字的列表
    lines = []
    for line in open(filename, 'r', encoding='utf-8'):
        line = line.replace('\r', '').replace('\n', '')
        print(line)
        if line == '':
            continue
        line = line.strip('(')
        line = line.strip(')')
        line = line.replace(',', '')
        lines.append(line.split(' '))
    return lines


def Get_R(string):  # 为variables中的变量分配寄存器
    try:
        variables.remove(string)
    except:
        pass
    if string in table:
        return '$' + table[string]  # 如果已经存在寄存器分配，那么直接返回寄存器
    else:
        keys = []
        for key in table:  # 已经分配寄存器的变量key
            keys.append(key)
        for key in keys:  # 当遇到未分配寄存器的变量时，清空之前所有分配的临时变量的映射关系！！！
            if 'temp' in key and key not in variables:  #
                reg_ok[table[key]] = 1
                del table[key]  # 将分配给此temp变量的寄存器收回
        for reg in regs:  # 对于所有寄存器
            if reg_ok[reg] == 1:  # 如果寄存器可用
                table[string] = reg  # 将可用寄存器分配给该变量，映射关系存到table中
                reg_ok[reg] = 0  # 寄存器reg设置为已用
                if "array" in string:
                    regs.remove(reg)  # array的寄存器永远不会被收回
                    print(regs)
                return '$' + reg


def translate(line):
    global arrayAssign, flag
    # 数组操作
    # 数组调用
    # sw $v0 0($t0)  # 将$vo中的数放到t0对应的地址中

    if "&array" in line[1]:
        res = '\tadd {0},{1},{2}\n'.format(Get_R(line[3]), Get_R(line[1].replace("&", "")),
                                           Get_R(line[2]))
        return res
    # 给数组元素赋值
    if line[0] == "=" and "*temp" in line[3]:
        res = '\tsw {} 0({})\n'.format(Get_R(line[1]), Get_R(line[3].replace("*", "")))
        return res


    # 定义数组
    if line[0] == 'DEC':
        res = '{}:.space 1024\n'.format(line[3])
        arrayDefinition.append(res)
        arrayAssign += '\tla {},{}\n'.format(Get_R(line[3]), line[3])
        return arrayAssign
    if line[0] == 'LABEL':  # 转换 label
        return line[1] + ':'
    if line[0] == '=':  # 无运算操作的赋值
        if line[1][0] == '#':  # 用常数赋值
            # 被赋值变量用分配的寄存器替换，使用li语句完成使用立即数赋值的功能
            return '\tli %s,%s' % (Get_R(line[3]), line[1].replace('#', ''))
        else:  # 用变量赋值
            # 分别找到两个变量所在寄存器，使用move语句实现赋值操作
            if "*" in line[1]:
                res = '\tlw {},0({})'.format(Get_R(line[3]), Get_R(line[1].replace("*", "")))
                return res
            else:
                return '\tmove %s,%s' % (Get_R(line[3]), Get_R(line[1]))

    if line[0] == '+':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tadd {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tadd {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tadd %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))
    # sub $1,$2,$3  $1=$2-$3
    elif line[0] == '-':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tsub {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tsub {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tsub %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))
    # mul $1,$2,$3  $1=$2*$3
    elif line[0] == '*':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tmul {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tmul {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tmul %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))
    # sub $1,$2,$3  $1=$2/$3
    elif line[0] == '/':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tdiv {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tdiv {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tdiv %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))

    elif line[0] == '%':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tdiv {},{}\n\tmfhi {}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[2]),
                                                          Get_R("temp*"), Get_R(line[3]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tdiv {},{}\n\tmfhi {}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[1]),
                                                          Get_R("temp*"), Get_R(line[3]))
        else:
            return '\tdiv %s,%s\n\tmfhi %s' % (Get_R(line[1]), Get_R(line[2]),Get_R(line[3]))


    # slt $1,$2,$3 if($2<$3)   $1=1 else $1=0
    elif line[0] == '<':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tslt {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tslt {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tslt %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))
    elif line[0] == '>':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tsgt {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tsgt {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tsgt %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))

    elif line[0] == '&&' and line[3][0] == 't':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tand {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tand {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                          Get_R(line[3]),
                                                          Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tand %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))
    elif line[0] == '||' and line[3][0] == 't':
        if "*" in line[1]:
            return '\tlw {},0({})\n\tor {},{},{}'.format(Get_R("temp*"), Get_R(line[1].replace("*", "")),
                                                         Get_R(line[3]),
                                                         Get_R("temp*"), Get_R(line[2]))
        elif "*" in line[2]:
            return '\tlw {},0({})\n\tor {},{},{}'.format(Get_R("temp*"), Get_R(line[2].replace("*", "")),
                                                         Get_R(line[3]),
                                                         Get_R("temp*"), Get_R(line[1]))
        else:
            return '\tor %s,%s,%s' % (Get_R(line[3]), Get_R(line[1]), Get_R(line[2]))
    elif line[0] == '&&' and line[3][0] == 'l':  # && || 跳转如何处理
        return '\tadd {4},{1},{0}\n\tli {3},2\n\tbeq {4},{3},{2}'.format(Get_R(line[1]), Get_R(line[2]), line[3],
                                                                         Get_R("2"), Get_R("tempand"))
    elif line[0] == '||' and line[3][0] == 'l':
        return '\tadd {4},{1},{0}\n\tli {3},0\n\tbgt {4},{3},{2}'.format(Get_R(line[1]), Get_R(line[2]), line[3],
                                                                         Get_R("0"), Get_R("tempor"))
    elif line[0] == '!':
        return '\tnot %s %s' % (Get_R(line[3]), Get_R(line[0]))

    if line[0] == 'CALL' and line[3] != '_':  # 函数调用并赋给变量
        res = ''
        if line[2] != '{}':  # 传递函数参数，先把a0中数据转移到t0,再将当前参数放到a0中
            arg = line[2].strip('}').strip('{')
            arglist = arg.split(';')
            if "*" in arglist[0]:
                # lw {},0({})'.format(Get_R(line[3]), Get_R(line[1].replace("*", "")
                res += '\tmove $t0,$a0\n\tlw $a0,0({})\n'.format(Get_R(arglist[0].replace("*", "")))
            else:
                res += '\tmove $t0,$a0\n\tmove $a0,%s\n' % Get_R(arglist[0])
        if line[1] == 'read' or line[1] == 'print':  # read 函数 与 print函数的调用，插入提前写好的固定代码段
            # addi	$sp, $sp, -4	# allocate stack space # 栈中开辟1个新地址
            # sw ra, 0($sp)	 # to save return address SW(Store Word)用于将源寄存器中的值存入指定的地址
            # lw $ra,0($sp) 存储返回地址到ra
            # $v0 - $v1 函数返回值  move .. $vo 获得函数返回值
            # addi	$sp, $sp, -4 回收堆栈空间
            res += '\taddi $sp,$sp,-4\n\tsw $ra,0($sp)\n\tjal %s\n\tlw $ra,0($sp)\n\tmove %s,$v0\n\taddi $sp,$sp,4' % (
                line[1], Get_R(line[3]))
            return res
        else:  # 分配新空间，存储当前指令地址，传递参数，跳转，恢复调用之前状态，获得返回值，回收空间
            res += '\taddi $sp,$sp,-24\n\tsw $t0,0($sp)\n\tsw $ra,4($sp)\n\tsw $t1,8($sp)\n\tsw $t2,12($sp)\n\tsw $t3,16($sp)\n\tsw $t4,20($sp)\n\tjal %s\n\tlw $a0,0($sp)\n\tlw $ra,4($sp)\n\tlw $t1,8($sp)\n\tlw $t2,12($sp)\n\tlw $t3,16($sp)\n\tlw $t4,20($sp)\n\taddi $sp,$sp,24\n\tmove %s $v0' % (
                line[1], Get_R(line[3]))
            return res

    if line[0] == 'j' and line[1] == '_' and line[2] == '_':  # 无条件跳转
        return '\tj %s' % line[3]

    if line[0] == 'RETURN':  # 函数调用结束，存储返回值，跳转回调用者位置
        return '\tmove $v0,%s\n\tjr $ra' % Get_R(line[3])
    if line[0][0] == 'j':  # 条件跳转
        # beq    $t0,$t1, target  # branch to target if  $t0 = $t1
        # blt    $t0,$t1, target  # branch to target if  $t0 < $t1
        # ble    $t0,$t1, target  # branch to target if  $t0 <= $t1
        # bgt    $t0,$t1, target  # branch to target if  $t0 > $t1
        # bge    $t0,$t1, target  # branch to target if  $t0 >= $t1
        # 四元式 (jop, arg1, arg2, res)
        if line[0] == 'j==':  # ==
            return '\tbeq %s,%s,%s' % (Get_R(line[1]), Get_R(line[2]), line[3])
        if line[0] == 'j!=':
            return '\tbne %s,%s,%s' % (Get_R(line[1]), Get_R(line[2]), line[3])
        if line[0] == 'j>':
            return '\tbgt %s,%s,%s' % (Get_R(line[1]), Get_R(line[2]), line[3])
        if line[0] == 'j<':
            return '\tblt %s,%s,%s' % (Get_R(line[1]), Get_R(line[2]), line[3])
        if line[0] == 'j>=':
            return '\tbge %s,%s,%s' % (Get_R(line[1]), Get_R(line[2]), line[3])
        if line[0] == 'j<=':
            return '\tble %s,%s,%s' % (Get_R(line[1]), Get_R(line[2]), line[3])

    if line[0] == 'FUNCTION':  # 转换函数标号
        if line[2] != '{}':  # 只将函数参数与a0寄存器关联，不生成汇编指令
            param = line[2].strip('}').strip('{')
            paramlist = param.split(';')
            table[paramlist[0]] = 'a0'  # 函数参数统一从a0取 (只能处理传递一个参数的情况)
        return '%s:' % line[1]

    if line[0] == 'CALL' and line[3] == '_':
        res = ''
        if line[2] != '{}':  # 传递函数参数，先把a0中数据转移到t0,再将当前参数放到a0中
            arg = line[2].strip('}').strip('{')
            arglist = arg.split(';')
            if "*" in arglist[0]:
                # lw {},0({})'.format(Get_R(line[3]), Get_R(line[1].replace("*", "")
                res += '\tmove $t0,$a0\n\tlw $a0,0({})\n'.format(Get_R(arglist[0].replace("*", "")))
            else:
                res += '\tmove $t0,$a0\n\tmove $a0,%s\n' % Get_R(arglist[0])
        if line[1] == 'read' or line[1] == 'print':
            res += '\taddi $sp,$sp,-4\n\tsw $ra,0($sp)\n\tjal %s\n\tlw $ra,0($sp)\n\taddi $sp,$sp,4' % (line[1])
            return res
        else:
            res += '\taddi $sp,$sp,-24\n\tsw $t0,0($sp)\n\tsw $ra,4($sp)\n\tsw $t1,8($sp)\n\tsw $t2,12($sp)\n\tsw $t3,16($sp)\n\tsw $t4,20($sp)\n\tjal %s\n\tlw $a0,0($sp)\n\tlw $ra,4($sp)\n\tlw $t1,8($sp)\n\tlw $t2,12($sp)\n\tlw $t3,16($sp)\n\tlw $t4,20($sp)\n\taddi $sp,$sp,24' % (
                line[1])
            return res

    return ''


def write_to_txt(Obj):  # 将最终转换结果写到result.asm文件中
    dataSection = ""
    for line in arrayDefinition:
        dataSection += line
    f = open('result.asm', 'w')
    # 统一使用开头：
    template = '''
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\\n"
''' + dataSection + '''
.globl main
.text''' + '''
jal main
li $v0,10
syscall
read:
    li $v0,4
    la $a0,_prompt
    syscall
    li $v0,5
    syscall
    jr $ra

print:
    li $v0,1
    syscall
    li $v0,4
    la $a0,_ret
    syscall
    move $v0,$0
    jr $ra
'''
    f.write(template)
    for line in Obj:
        f.write(line + '\n')
    f.close()


def parser():  # 转换的程序入口
    for reg in regs:
        reg_ok[reg] = 1  # 初始化，所有寄存器都可用
    Inter = Load_Inter('inter.txt')  # 读取中间代码
    Load_Var(Inter)  # 第一遍扫描，记录所有变量
    Obj = []  # 存储最终转换结果
    for line in Inter:  # 逐行进行转换
        obj_line = translate(line)  # 转换中间代码成MIPS汇编
        if obj_line == '':
            continue
        Obj.append(obj_line)
    write_to_txt(Obj)


parser()
