
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\n"
.align 2

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
judge:
	li $t1,0
	move $t2,$t1
	li $t1,2
	move $t3,$t1
label0:
	blt $t3,$a0,label1
	j label2
label1:
	div $a0,$t3
	mfhi $t1
	li $t4,0
	beq $t1,$t4,label3
	j label4
label3:
	li $t1,1
	add $t2,$t2,$t1
label4:
	li $t1,1
	add $t3,$t3,$t1
	j label0
label2:
	li $t1,0
	bne $t2,$t1,label5
	j label6
label5:
	li $t1,0
	move $v0,$t1
	jr $ra
	j label7
label6:
	li $t1,1
	move $v0,$t1
	jr $ra
label7:
main:
	li $t1,0
	move $t4,$t1
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal read
	lw $ra,0($sp)
	move $t1,$v0
	addi $sp,$sp,4
	move $t4,$t1
	move $t0,$a0
	move $a0,$t4
	addi $sp,$sp,-24
	sw $t0,0($sp)
	sw $ra,4($sp)
	sw $t1,8($sp)
	sw $t2,12($sp)
	sw $t3,16($sp)
	sw $t4,20($sp)
	jal judge
	lw $a0,0($sp)
	lw $ra,4($sp)
	lw $t1,8($sp)
	lw $t2,12($sp)
	lw $t3,16($sp)
	lw $t4,20($sp)
	addi $sp,$sp,24
	move $t1 $v0
	move $t5,$t1
	li $t1,0
	sgt $t6,$t5,$t1
	li $t1,2
	li $t7,4
	slt $t8,$t1,$t7
	li $t1,3
	li $t7,6
	sgt $s0,$t1,$t7
	and $t1,$t8,$s0
	add $t6,$t1,$t6
	li $t1,0
	bgt $t6,$t1,label8
	j label9
label8:
	move $t0,$a0
	move $a0,$t5
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
	j label10
label9:
	li $t6,0
	move $t7,$t6
	li $t6,0
	move $t8,$t6
label11:
	li $t6,3
	ble $t7,$t6,label12
	j label13
label12:
	li $t6,2
	add $s0,$t8,$t6
	move $t8,$s0
	li $t6,1
	add $t7,$t7,$t6
	j label11
label13:
	move $t0,$a0
	move $a0,$t8
	addi $sp,$sp,-4
	sw $ra,0($sp)
	jal print
	lw $ra,0($sp)
	addi $sp,$sp,4
label10:
	li $t6,0
	move $v0,$t6
	jr $ra
