
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\n"
.align 2
array0:.space 1024

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
	li $t1,1
	move $t2,$t1
	li $t1,0
	beq $t2,$t1,label0
	j label1
label0:
	li $t1,1
	move $t0,$a0
	move $a0,$t1
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
	j label2
label1:
	li $t1,2
	move $t0,$a0
	move $a0,$t1
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
label2:
	li $t1,10
	li $t3,4
	mul $t4,$t3,$t1
	la $t1,array0

	li $t3,2
	li $t5,4
	mul $t6,$t3,$t5
	add $t3,$t1,$t6

	li $t5,5
	sw $t5 0($t3)

	li $t3,2
	li $t5,4
	mul $t6,$t3,$t5
	add $t3,$t1,$t6

	li $t5,3
	lw $t6,0($t3)
	add $t3,$t6,$t5
	move $t5,$t3
	move $t0,$a0
	move $a0,$t5
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
	li $t3,0
	move $v0,$t3
	jr $ra
