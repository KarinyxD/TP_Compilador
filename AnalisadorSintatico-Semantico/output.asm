.data
x: .word 0
y: .float 0.0
d: .byte 0
z: .word 0
t: .byte 0
f: .byte 0
logico1: .byte 0
i: .word 0

.text
.globl main
main:
li $t0, 2
sw $t0, x
lw $t0, x
mtc1 $t0, $f1
cvt.s.w $f1, $f1
li.s $f0, 3.2
mov.s $f2, $f0
add.s $f0, $f1, $f2
swc1 $f0, y
li $t0, 116
sb $t0, d
lw $t0, x
move $t2, $t1
lw $t0, x
move $t4, $t3
li $t0, 2
move $t5, $t3
mul $t3, $t4, $t5
move $t3, $t1
add $t1, $t2, $t3
move $t1, $t0
li $t0, 1
move $t2, $t0
add $t0, $t1, $t2
sw $t0, z
li $t0, 1
sb $t0, t
li $t0, 0
sb $t0, f
lb $t0, t
move $t1, $t0
lb $t0, f
move $t2, $t0
and $t0, $t1, $t2
sb $t0, logico1
li $t0, 0
sw $t0, i
for_start_1:
lw $t0, i
move $t1, $t0
li $t0, 10
move $t2, $t0
slt $t0, $t1, $t2
beq $t0, $zero, for_end_2
lb $t0, logico1
beq $t0, $zero, endif_3
lw $t0, i
move $t1, $t0
li $t0, 3
move $t2, $t0
add $t0, $t1, $t2
sw $t0, i
endif_3:
lw $t0, i
move $t1, $t0
li $t0, 1
move $t2, $t0
add $t0, $t1, $t2
sw $t0, i
j for_start_1
for_end_2:
li $v0, 10
syscall
