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