#ASSEMBLER

#defining all  the available registers along with their register numbers
reg={"$0":0, "$zero":0, "$v0":2, "$v1":3, "$a0":4, "$a1":5, "$a2":6, "$a3":7, "$t0":8, "$t1":9, "$t2":10, "$t3":11, "$t4":12, "$t5":13, "$t6":14, 
"$t7":15, "$s0":16, "$s1":17, "$s2":18, "$s3":19, "$s4":20, "$s5":21, "$s6":22, "$s7":23, "$t8":24, "$t9": 25, "$k0":26, "$k2":27, "$gp":28, 
"$sp":29, "$fp":30, "$ra":31}


def bintohex(a): #binary to hexadecimal conversion 
  decimal_rep = int(a,2)
  return hex(decimal_rep)
  

def dectobin(x): #decimal  to binary conversion
    b = bin(x)
    return b[2:]

def dectobin_signed(n, size): #coversion of the signed decimal to signed binary number
    a = bin(n & int("1"*size, 2))[2:]
    return ("{0:0>%a}" % (size)).format(a)
    

# R format 
#{
# type1 : ins r1 r2 r3
# type2 : ins r1 r2 
# type3 : ins r1
# type4 : ins r1 r2 imm
#}


#I format
#{
#type 1 : instructions with 3 parts and 1 part as immediate value
#type 2 : instructions with label
#type 3 : instructoins with 2 parts and 1 part as imm val
#}


#defining all the format, type, opcode, shamt and function values as and when required
# pnemonics = {function:{format, type , opcode, shamt, func} } for R type format
# pnemonics = {function:{format, opcode, type}} for I type format
# pnemonics = {function:{format, opcode}} for J type format
pnemonics={
    "add":{"format":"R", "type":1 , "opcode":0 , "shamt":0 , "func":32 },"sub": {"format":"R", "type":1 , "opcode":0 , "shamt":0 , "func":34 },
    "and":{"format":"R", "type":1 , "opcode":0, "shamt":0, "func": 36},
    "jr": {"format":"R", "type":3, "opcode": 0, "shamt":0,  "func":8 },
    "nor": {"format":"R", "type":1 , "opcode": 0, "shamt":0 ,"func": 39},
    "or":{"format":"R", "type": 1, "opcode": 0, "shamt": 0, "func":37 },
    "slt": {"format":"R", "type": 1, "opcode": 0, "shamt":0 , "func": 42},
    "sltu": {"format":"R", "type":1 , "opcode": 0, "shamt":0 , "func": 43},
    "sll": {"format":"R", "type": 4, "opcode": 0, "shamt": 0, "func": 0},
    "srl": {"format":"R", "type": 4, "opcode": 0, "shamt": 0, "func": 2},
    'addi':{'format':'I', 'opcode':8, 'type':1},
    'andi':{'format':'I', 'opcode':12, 'type':1},
    'beq':{'format':'I', 'opcode':4, 'type':2},
    'bne':{'format':'I', 'opcode':5, 'type':2},
    'lb':{'format':'I', 'opcode':32, 'type':3},
    'lbu':{'format':'I', 'opcode':36, 'type':3},
  'll': {'format':'I', 'opcode':48, 'type':3},
  "sc":{'format':'I', 'opcode':56, 'type':3},
  
    'lh':{'format':'I', 'opcode':33, 'type':3},
    'lhu':{'format':'I', 'opcode':37, 'type':3},
    'lui':{'format':'I', 'opcode':15, 'type':4},
    'lw':{'format':'I', 'opcode':35, 'type':3},
    'ori':{'format':'I', 'opcode':13, 'type':1},
    'sb':{'format':'I', 'opcode':40, 'type':3},
    'slti':{'format':'I', 'opcode':10, 'type':1},
    'sltiu':{'format':'I', 'opcode':11, 'type':1},
    'sh':{'format':'I', 'opcode':41, 'type':3},
    'sw':{'format':'I', 'opcode':43, 'type':3},
    'j':{"format":"J", "opcode":2},
    'jal': {"format":"J", "opcode":3}
}


#input text file
file_loc=input('Enter the file location or name here:') 
input_code=open(file_loc,'r')

#define the required variables 
base_address=int(input("Enter Base address in decimal: ")) 
code_lines=input_code.readlines()
instructions=[]
labels={}
address=[base_address]

# +++++++ PASS 1 +++++++

#lines in input text file
num_of_lines=len(code_lines)

#track of the order of text file lines
num =0

#tracks the number of valid instrcutions encountered 
count = 0

#running through each and every line in the text file 
while num < (num_of_lines):
    code_lines[num]= code_lines[num].strip() # trimming the unnecessary white spaces
    if (len(code_lines[num])==0): #eliminating the blank lines
        num+= 1 #skipping to the next line
        continue  
    elif ":" in code_lines[num]:  # presence of label in the line
        current_ins = code_lines[num].split(":") #seperating the label from the instruction
        address.append(address[count]+4) #updating the address
        current_ins[1]= current_ins[1].strip() #removing white spaces from the text placed(in the same line) after the label
        
        if len(current_ins[1])!=0: # if the following instruction is written in the same line as the label
            instructions.append(current_ins[1]) # update the instructions list with the current valid instruction
            label_name = current_ins[0].strip() 
            labels[label_name]=address[count] #updating the symbol table with the label as well as their addresses  
            count+=1 #skip to the next instruction
            num+=1 #next line from the text
            
        else:  #if the instruction is not present in the same line as the label
            label_name = current_ins[0].strip() #striping the white spaces
            labels[label_name]= address[count] #updating the symbol table 
            num+=1
            count+=1
            while True: #search until come across a valid instruction
                code_lines[num] = code_lines[num].strip() 
                if len(code_lines[num])==0: # a blank line
                    num+=1
                else:
                    if ":" in code_lines[num]: #comes across a label
                        break
                    else:
                        current_ins = code_lines[num].strip() #finds a valid instruction
                        instructions.append(current_ins)
                        num+=1
                        break
                    
    else: #a valid instruction
        current_ins = code_lines[num].strip()
        instructions.append(current_ins) #adding it to the list of instructions
        address.append(address[count]+4) #update the address
        count+=1
        num+=1

      
del address[-1] # in the pass loop we add an extra address to the list so we eliminate it from the list

final_address = address[-1] # maximum address
binary_nor =[] #

final_binary_code = []
final_hex_code=[]

inst_index=-1
  

#++++++++ PASS-2 ++++++++


try: #used to display an error incase of wrong input
  for code in instructions: #running through each and every instructions for pass 2
      inst_index+=1 # track of the current instruction
      code=code.replace(","," ") #replacing all the comas with white spaces. This enables the acceptancen of the two widely used syntaxes
      elements=code.split() 
  
      oper=pnemonics[elements[0]] 
  
      if oper['format']=='I': #identifing the I format
     
          if oper['type']==1: #type 1 : func r1 r2 imm
              rs=dectobin(reg[elements[2]])
              rt=dectobin(reg[elements[1]])
              op=dectobin(oper['opcode'])
              if 'x' in elements[3]: # imm in hexadeciamal
                imm=dectobin(int(elements[3][2:],16))
              else: #imm in decimal
                imm=dectobin(int(elements[3]))
              output=op.zfill(6)+rs.zfill(5)+rt.zfill(5)+imm.zfill(16) 
      
  
          elif oper['type']==2: #type 2: func r1 r2 label(or offset)
              rt=dectobin(reg[elements[2]])
              rs=dectobin(reg[elements[1]])
              op=dectobin(oper['opcode'])
              x= elements[3]
              try: 
                  x = int(x)
                  offset=int(elements[3])
              except: #incase of the label
                  offset=((labels[elements[3]] - address[inst_index])//4)-1
              labl=dectobin_signed(offset,16)
              output=op.zfill(6)+rs.zfill(5)+rt.zfill(5)+str(labl)
  
  
          elif oper['type']==3: #type 3: fun r1 imm(r2)
            
              rt=dectobin(reg[elements[1]])
              op=dectobin(oper['opcode'])
  
              imm,regis=elements[2].split('(')
              regis = regis.split(")")[0]
              rs=dectobin(reg[regis])
              imm=dectobin(int(imm))
  
              output=op.zfill(6)+rs.zfill(5)+rt.zfill(5)+imm.zfill(16) #output
  
                                                                   
          elif oper['type']==4: #type 4: func r1 imm
            
              rt=dectobin(reg[elements[1]])
              imm=dectobin(int(elements[2]))
              rs="00000"
              op=dectobin(oper['opcode'])
              
              output=op.zfill(6)+rs.zfill(5)+rt.zfill(5)+imm.zfill(16)
  
          
      elif (oper['format']=='R'): #identifing the R format
          if oper['type']==1: #type1 : func r1 r2 r3
              rs=dectobin(reg[elements[2]])
              rd=dectobin(reg[elements[1]])
              op=dectobin(oper['opcode'])
              rt=dectobin(int(reg[elements[3]]))
              output=op.zfill(6)+rs.zfill(5)+rt.zfill(5)+rd.zfill(5)+ str(oper["shamt"]).zfill(5)+ str(dectobin(oper["func"])).zfill(6)
            
          elif oper['type']==3: #type 2 : jr r1
              rs = dectobin(int(reg[elements[1]]))
              output = "000000"+ rs.zfill(5)+"0".zfill(15)+ str(dectobin(oper["func"])).zfill(6)
            
          elif oper["type"]==4: #type 4: func r1 r2 imm
              rd = dectobin(reg[elements[1]])
              rt = dectobin(reg[elements[2]])
              rs = "00000"
              sham = dectobin(int(elements[3]))
              output = "000000"+ rs.zfill(5)+rt.zfill(5)+ rd.zfill(5) + sham.zfill(5) +str(dectobin(oper["func"])).zfill(6)
          
  
      elif (oper["format"])=="J": # identifing the J format for jump functions
          if ((elements[1].strip()).isnumeric() and int(elements[1].strip())>=base_address//4 and int(elements[1].strip())<=final_address//4): #limiting the address
              addr= dectobin(int(elements[1])).zfill(26)
              op= dectobin(oper["opcode"]).zfill(6)
              output= op.zfill(6) + addr
              
          else:
            addr=dectobin((labels[(elements[1]).strip()])//4).zfill(26)
            op= dectobin(oper["opcode"]).zfill(6)
            output= op + addr
              
          
          
      output_read= output[:4]+" "+output[4:8]+" " + output[8:12] +" "+ output[12:16] +" "+ output[16:20] +" "+ output[20:24] +" "+ output[24:28] +" "+ output[28:]   #modifing the output for readability    
  
      final_binary_code.append(output_read) 
      binary_nor.append(output)
      final_hex_code.append((bintohex(output))[:2]+(bintohex(output))[2:].zfill(8))
  
  
 #displaying the output     
  print("\nBinary code\n")
  for i in final_binary_code:
    print(i+"\n" )
  
  print()
  print("\nHexadecimal code\n")
  for i in final_hex_code:
    print(i+"\n" )

# error display
except:
  print("A ERROR OCCURED IN THE INPUT!!")
  print("\nKindly check the following:")
  print('\n- Instructions used must be included in the provided data sheet\n- Numerical inputs must be in decimal form\n- Comments are not allowed\n- Colon must be used to denote label\n- Address out of range for jump instructions\n- Syntax error')
  