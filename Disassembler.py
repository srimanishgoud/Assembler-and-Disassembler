#defining the registers and the register values 
reg_rev={0: "$0", 2:"$v0", 3:"$v1", 4:"$a0", 5:"$a1",6: "$a2", 7: "$a3", 8: "$t0", 9: "$t1", 10:"$t2", 11: "$t3", 12:"$t4",13: "$t5", 14: "$t6", 15: "$t7", 16: "$s0", 17:"$s1", 18:"$s2", 19: "$s3", 20: "$s4", 21: "$s5", 22: "$s6", 23: "$s7", 24:"$t8", 25: "$t9", 26: "$k0", 27: "$k2", 28: "$gp", 29: "$sp", 30:"$fp", 31: "$ra"}


#defining the R, J, I function formats
R_fun = {32: ["add", 1],34:["sub", 1], 36:["and", 1], 8:["jr", 3],39:["nor", 1],37:["or", 1], 42:["slt", 1], 43:["sltu", 1], 0:["sll", 4], 2:["srl", 4]}

J_op = {2: "j", 3:"jal" }
I_op ={8:["addi", 1], 12:["andi", 1], 4:["beq", 2], 5:["bne", 2], 32:["lb", 3], 36: ["lbu",3], 48:["ll", 3], 56:["sc", 3], 33:["lh", 3], 37:["lhu", 1], 15:["lui", 4], 35: ["lw", 3], 13:["ori", 1], 40:["sb", 3], 10:["slti",1], 11: ["sltiu",1], 41:["sh", 3], 43:["sw", 3]}

#taking the input text file 
file_loc=input('Enter the fie location or name : ')
Base_address = int(input("Enter the vaule of Base address in decimal: "))

Address =[]

types_I = { 1:[ 6, 5, 5,16], 2: [6, 6,5,5,16], 3:[]}

final_bin=[]

#track of the current index label
lable_index = None

line_index = 0 

binary_code = []

#binary to decimal conversion
def bintodec(x):
  dec = int(x,2)
  return dec



# taking the input text file 
input_code=open(file_loc,'r')
code_lines=input_code.readlines()

num_lines = len(code_lines)



lables=[] #label name storage

# Labelling and addressing every line
for instruction_num in range(num_lines):
  lables.append('Lable-%d'%instruction_num)
  binary_code.append(code_lines[instruction_num])
  Address.append(Base_address+ instruction_num*4)

try:

  for binary in binary_code:
    binary = binary.strip()
    
    if binary[:2]=='0x': # if the input is in hexadecimal format
      hexa = int(binary[2:],16)
      binary= (bin(hexa))[2:]#convert to binary
      binary=binary.zfill(32)
      
      
    
    opcode_rev = bintodec(binary[:6]) 
    if opcode_rev ==0: #identifing the type of formats
      format_rev= "R"
      op_rev = binary[:6]
      fun = bintodec(binary[-6:])
      type = R_fun[fun][1]
      
      if type ==1:# func r1 r2 r3
        rs = bintodec(binary[6:11])
        rt = bintodec(binary[11:16])
        rd = bintodec(binary[16:21])
        shamt = bintodec(binary [21:26])
        output = R_fun[fun][0]+ " "+ reg_rev[rd]+', '+ reg_rev[rs]+', '+reg_rev[rt]
      elif type ==3: #func r1
        rs = bintodec(binary[6:11])
        output = R_fun[fun][0]+ " "+ reg_rev[rs]
      elif type ==4:# func r1 r2 imm
        rt = bintodec(binary[11:16])
        rd = bintodec(binary[16:21])
        shamt = bintodec(binary [21:26])
        output = R_fun[fun][0]+ ' '+ reg_rev[rd]+', '+ reg_rev[rt]+', '+str(shamt)
      
    elif (opcode_rev == 2 or opcode_rev == 3): #J format
      format_rev = "J"
      lable_index = Address.index(int(bintodec(binary[-26:]))*4)
      output = J_op[opcode_rev]+" "+ lables[lable_index]
      
    elif (opcode_rev >3): # I format
      format_rev = "I"
      type = I_op[opcode_rev][1]
      if type ==1 : #func r1 r2 imm
        rt = bintodec(binary[11:16])
        rs = bintodec(binary[6:11])
        imm = bintodec(binary[-16:])
        output = I_op[opcode_rev][0]+" "+ reg_rev[rt] + ", "+ reg_rev[rs]+", "+str(imm)
  
      elif type ==2 : #func r1 r2 label
        lab = binary[-16:]
        if lab[0]=='1':
          ans = -(2**(15))
          for bi in range(1,16):
            ans=ans+(int(lab[bi])*(2**(15-bi)))
          lab=ans
        else:
          lab = bintodec(binary[-16:])
        
        rt = bintodec(binary[11:16])
        rs = bintodec(binary[6:11])
        lable_index = line_index + int(lab)+1
        output= I_op[opcode_rev][0]+" "+ reg_rev[rs]+", "+ reg_rev[rt]+", "+ lables[lable_index]
      
      elif type ==3 : # func r1 imm(r2)
        rt = bintodec(binary[11:16])
        rs = bintodec(binary[6:11])
        imm = bintodec(binary[-16:])
        output = I_op[opcode_rev][0]+ " "+ reg_rev[rt]+", "+ str(imm)+"("+reg_rev[rs]+")"
  
      elif type == 4: #func r1 imm
        rt = bintodec(binary[11:16])
        rs = bintodec(binary[6:11])
        imm = bintodec(binary[-6:])
        output =  I_op[opcode_rev][0]+ " "+ reg_rev[rt]+", "+ str(imm)
          
  
      
    final_bin.append(output)
    line_index+=1
  
  print('\n')
  for i in range(num_lines):
    print(lables[i],":",  final_bin[i])

except: #error display
  print("AN ERROR OCCURED IN THE INPUT!!\n")
  print("Kindly check the following:")
  print("\n- Make sure you do not put any blank line in between the lines of code\n- The hexadecimal code must be started with 0x....\n- Make sure you only use the instructions provided in the data sheet\n- Make sure that the machine code is valid")