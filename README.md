# cCompilerFinal

### 一个简单的C语言编译器

- Introduction：这是一个编译原理大作业
- author：sunxiaobing、zhaoyurou、zhangxinyi
- time：2019/12

> 运行

- 环境要求：flex bison g++11 python3
- 工具：Mars（汇编器）

> 中间代码生成

- 运行

  ``` makefile.bat```

> 目标代码生成

1.  将目录下innerCode.txt（生成的四元式）中的内容，复制到objectcode文件夹下的inter.txt
2. 进入objectcode文件夹，执行```python objectcode.py```
3. 生成result.asm文件，即为生成的mips汇编码

> 生成可执行二进制文件

- 在Mars中运行result.asm文件即可

> 修改测试文件

-  测试者可以选择**更改**makefile.bat文件中**最后一行**的测试文件名，来修改测试文件（默认test.c）
- **注意**：我们为测试者准备了四个测试样例，分别为test文件夹下的**test.c、test1.c、test2.c、test3.c**。其中，test.c文件支持了绝大多数的实验要求以及函数调用，test1.c支持了数组运算以及bool表达式的使用、test2.c为各种类型检查以及程序检查报错的样例、test3.c支持了break退出循环。



#### 测试文件test.c内容：

```c
//test.c
// 函数调用 ++ += 
//是否是素数 是返回1
int judge(int num)
{
    int a = 0;
    for(int i=2;i<num;i++){
        if(num % i == 0){
            a++;  // 素数个数加1
        }
    }
    if(a!=0) {
        return 0;
    }
    else {
        return 1;
    }
}
int main(){
    int num=0;  // 输入的整数
    num = read();
    int flag = judge(num);
    if( flag > 0 || 2 < 4 && 3 > 6 ) {
        print(flag);
    } 
    else
    {
        int i = 0;
        int m = 0;
        while (i <= 3)
        {
            m += 2;
            i++;
        }
        print(m); //8
    }
    return 0;
}
```

