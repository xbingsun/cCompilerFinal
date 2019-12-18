
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\n"
.globl main
.text
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
main:
	li $t1,3
	move $t2,$t1
	li $t1,2
	move $t3,$t1
	li $t1,1
	li $t4,2
	slt $t5,$t1,$t4
	li $t1,4
	li $t4,3
	slt $t6,$t1,$t4
	and $t1,$t5,$t6
	li $t4,3
	li $t5,1
	sgt $t6,$t4,$t5
	add $t4,$t6,$t1
	li $t1,0
	bgt $t4,$t1,label0
	j label1
label0:
	move $t0,$a0
	move $a0,$t2
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
	j label2
label1:
	move $t0,$a0
	move $a0,$t3
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
label2:
	li $t4,0
	move $v0,$t4
	jr $ra
