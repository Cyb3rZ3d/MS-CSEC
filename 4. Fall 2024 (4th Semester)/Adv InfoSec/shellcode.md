



# Task 1: Writing Assembly Code

- Run `nano hello.s` to review the assembly program code

    ![alt text](<Screenshot 2024-09-08 at 4.46.28 PM.png>)

- Compile to object code using the command `nasm -f elf64 hello.s -o hello.o`

- Run the linker program using the command, `ld hello.o -o hello`, to generate the final binary to get the executable code.  We should then see `Hello, World!`

    ![alt text](<Screenshot 2024-09-08 at 4.53.29 PM.png>)

- Now we can extract the machine code from the executablefile or object file.  There are two different ways to complete this.

    1. Using the `jdump` to disassemble the executable or object file

        - Command:  `objdump -Mintel -d hello.o`
            
            ![alt text](<Screenshot 2024-09-08 at 5.02.00 PM.png>)

    2. Using the `xxd` to print out the binary contents

        - Command:  `xxd -p -c 20 hello.o`

            ![alt text](<Screenshot 2024-09-08 at 5.02.51 PM.png>)


# Task 2: Writing Shellcode (Approach 1)

## Task 2.a. Understand the code

- Run `nano mysh64.s` to review the assembly program code

    ![alt text](<Screenshot 2024-09-08 at 5.10.13 PM.png>)

- Using `nasm` to assemble the code and `ld` linker to create the executable. After running the linker command, we can now run the shellcode binary which should launch a shell.  Once we're in the shell we can start debugging using `gdb`.

    ```
    nasm -g -f elf64 -o mysh64.o mysh64.s`
    ld --omagic -o mysh64 mysh64.o
    ./mysh64
    ```

    ![alt text](<Screenshot 2024-09-08 at 6.12.12 PM.png>)

    - Debugging the shell using the following gdb command
    
        ```
        gdb mysh64
        break one
        run
        print $rbx
        x/40bx 0x400082
        x/40bx $rsp
        x/5gx $rsp
        ```

        ![alt text](<Screenshot 2024-09-08 at 6.24.55 PM.png>)


## Task 2.b. Eliminate zeros from the code

- `mysh64.s` code review

    ![alt text](<Screenshot 2024-09-08 at 6.37.02 PM.png>)


- Updated and modified `mysh64.s` code to remove 0's

    ![alt text](<Screenshot 2024-09-08 at 7.12.30 PM.png>)



