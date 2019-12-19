
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\n"
.align 2
array0:.space 1024
array1:.space 1024

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
	li $t1,10
	li $t2,4
	mul $t3,$t2,$t1
	la $t1,array0

	li $t2,5
	li $t4,4
	mul $t5,$t4,$t2
	la $t1,array0
	la $t2,array1

	li $t4,2
	li $t6,4
	mul $t7,$t4,$t6
	add $t4,$t1,$t7

	li $t6,5
	sw $t6 0($t4)

	li $t4,3
	li $t6,4
	mul $t7,$t4,$t6
	add $t4,$t2,$t7

	li $t6,10
	sw $t6 0($t4)

	li $t4,2
	li $t6,4
	mul $t7,$t4,$t6
	add $t4,$t1,$t7

	li $t6,3
	lw $t7,0($t4)
	add $t4,$t7,$t6
	move $t6,$t4
	li $t4,3
	li $t7,4
	mul $t8,$t4,$t7
	add $t4,$t2,$t8

	li $t7,1
	lw $t8,0($t4)
	sub $t4,$t8,$t7
	move $t7,$t4
	blt $t6,$t7,label0
	j label1
label0:
	li $t4,1
	move $t0,$a0
	move $a0,$t4
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
label1:
	li $t4,0
	move $v0,$t4
	jr $ra
