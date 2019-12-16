flex compiler.l
bison -vdty compiler.y
g++ -std=gnu++0x -o compiler tree.cpp Praser.cpp innerCode.cpp tools.cpp codeOptimize.cpp lex.yy.c y.tab.c
compiler.exe test/test.c
