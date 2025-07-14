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
li $t0, 2
sw $t0, x
lw $t1, x
mtc1 $t1, $f1
cvt.s.w $f1, $f1
li.s $f0, 3.2
mov.s $f2, $f0
add.s $f0, $f1, $f2
swc1 $f0, y
li $t0, 116
sb $t0, d
lw $t3, x
lw $t5, x
li $t6, 2
mul $t4, $t5, $t6
add $t1, $t3, $t4
li $t2, 1
add $t0, $t1, $t2
sw $t0, z
li $t0, 1
sb $t0, t
li $t0, 0
sb $t0, f
lb $t1, t
lb $t2, f
and $t0, $t1, $t2
sb $t0, logico1
li $t0, 0
sw $t0, i
for_start_1:
lw $t1, i
li $t2, 10
slt $t0, $t1, $t2
beq $t0, $zero, for_end_2
lb $t0, logico1
beq $t0, $zero, endif_3
lw $t1, i
li $t2, 3
add $t0, $t1, $t2
sw $t0, i
endif_3:
lw $t1, i
li $t2, 1
add $t0, $t1, $t2
sw $t0, i
j for_start_1
for_end_2:
