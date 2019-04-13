code segment
main:
    mov ah,01h ;
    int 21h          ;Reads first char of input
    mov cx, 0        ;initialize cx 0 as counter for stack for multidigit operations
	cmp al, 38       ;Checks '&' sign
    jz myand
	cmp al, 124      ;Checks '|' sign
    jz myor
	cmp al, 94       ;Checks '^' sign
    jz myxor
    cmp al, 43       ;Checks '+' sign
    jz addition
    cmp al, 47
    jz division      ;Checks '/' sign
    cmp al, 42
    jz multiplication;Checks '*' sign
read:
    cmp al, 57       ;Checks if input is letter or number
    jle num
    jge letter
myor:                ;pops the top of stack and the other to OR
	xor ax,ax        ;Make ax 0
	xor bx,bx        ;Make bx 0
    pop ax
    pop bx
	or ax, bx
    push ax
    jmp checkexit
	
myand:               ;pops the top of stack and the other to AND
	xor ax,ax        ;Make ax 0
	xor bx,bx        ;Make bx 0
    pop ax
    pop bx
	and ax, bx
    push ax
    jmp checkexit
	
myxor:              ;pops the top of stack and the other to XOR
	xor ax,ax       ;Make ax 0
	xor bx,bx       ;Make bx 0
    pop ax
    pop bx
	xor ax, bx
    push ax
    jmp checkexit
	
jmpmain:            ;To avoid jmp > 127 error
	jmp main

addition:           ;pops the top of stack and the other to ADD
    xor ax,ax       ;Make ax 0
	xor bx,bx       ;Make bx 0
    pop ax
    pop bx
    add ax, bx
    push ax
    jmp checkexit
   
division:           ;pops the top of stack and the other to DIVIDE
    xor ax,ax       ;Make ax 0
	xor bx,bx       ;Make bx 0
    pop bx
    pop ax
    xor dx,dx
	div bx
    push ax
    jmp checkexit

multiplication:     ;pops the top of stack and the other to MULTIPLY
    xor ax,ax       ;Make ax 0
	xor bx,bx       ;Make bx 0
    pop bx
    pop ax
    mul bx
    push ax
    jmp checkexit

checkexit:          ;If enter pressed convert result to hexadecimal or continue   
    mov ah,01h ;
    int 21h
    cmp al, 13
    jz convert
    jnz main

num:                ;If pressed char is num substract 48
    sub al, 48
	mov bx,0
	mov bl, al  
    cmp cl, 0       ;Checks if stack is empty for multidigit
    jz checkchar
    jnz multidigit

letter:             ;If pressed char is num substract 55
    sub al, 55
    mov bx,0
	mov bl, al
    cmp cl, 0       ;Checks if stack is empty for multidigit
    jz checkchar
    jnz multidigit
	
checkchar:          ;Checks if space is pressed or multidigit
    push bx
    mov ah, 01h 
    int 21h
    cmp al, 32
    jz jmpmain
	inc cx          ;Increments cx to indicate another digit is present
    jmp read        ;Jumps to start of the operation

multidigit:
    xor ax, ax
    pop ax          ;Pops the first element from stack
    dec cx          ;Decrement the counter for stack
    mov dx, 16      ;multiply with 10 for shift left 
    mul dx
    add ax, bx      ;adds the digits
    xor bx, bx
    mov bx, ax
    xor ax, ax
    jmp checkchar

convert:            ;Converts Decimal result to hexadecimal result
    xor dx,dx
    pop ax          ;Pops the result
    xor bx,bx
    mov bx,16       ;Put number 16 to bx
    div bx
    push dx
    xor dx,dx
    div bx          ;Divide 16 for hexadecimal result
    push dx
    xor dx,dx
    div bx
    push dx         ;Push remaining
    push ax         ;Push quotient
    mov ah, 02h
    mov bx, 4       ;Counter for 4 digits as 16bits

printnum:           ;Loop for printing numbers
    cmp bx,0
    jz ending
    xor dx,dx
    pop dx	
    cmp dx,10
    jge printletter
    add dx,48
    int 21h
    dec bx
    jmp printnum

printletter:        ;Loop for printing letters
    add dx,55
    int 21h
    dec bx
    jmp printnum

ending:
   int 20h 
code ends