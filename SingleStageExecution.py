from utils import Utils


class SingleStageExecution(object):
    def __init__(self):
        pass

    def perform_operation(self, dInst, register, dataMem, take_Branch, PC):
        #R-type----------------------------------------------------------------------

        if(dInst['type'] == 'add'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            result = data1 + data2
            register.writeRF(rd, result)
        
        elif(dInst['type'] == 'sub'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            result = data1 - data2
            register.writeRF(rd, result)
        
        elif(dInst['type'] == 'xor'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            result = data1 ^ data2
            register.writeRF(rd, result)
        
        elif(dInst['type'] == 'or'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            result = data1 | data2
            register.writeRF(rd, result)

        elif(dInst['type'] == 'and'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            result = data1 & data2
            register.writeRF(rd, result)

        #I-type --------------------------------------------------------------------

        elif(dInst['type'] == 'addi'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            result = data1 + imm
            register.writeRF(rd, result)
        
        elif(dInst['type'] == 'xori'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            result = data1 ^ imm
            register.writeRF(rd, result)

        elif(dInst['type'] == 'ori'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            result = data1 | imm
            register.writeRF(rd, result)
        
        elif(dInst['type'] == 'andi'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            data1 = register.readRF(rs1)
            result = data1 & imm
            register.writeRF(rd, result)
        
        #Load-type --------------------------------------------------------------------
        
        elif(dInst['type'] == 'lw'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            address = register.readRF(rs1)
            address = address + imm
            result = dataMem.readDataMem(address)
            register.writeRF(rd, result)
        
        #Store-type --------------------------------------------------------------------
        
        elif(dInst['type'] == 'sw'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            data = register.readRF(rs2)
            address = register.readRF(rs1)
            address = address + imm
            dataMem.writeDataMem(address,data)
        
        #Branch-type --------------------------------------------------------------------

        elif(dInst['type'] == 'beq'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            
            result = abs(data1-data2)
            if result==0:
                take_Branch = True
                PC.IF["PC"] += imm
        
        elif(dInst['type'] == 'jal'):
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            register.writeRF(rd, PC.IF["PC"]+4)
            take_Branch = True
            PC.IF["PC"] += imm << 1
        
        elif(dInst['type'] == 'bne'):
            rs1 = Utils.binary_to_decimal(dInst['rs1'])
            imm = Utils.twos_complement(dInst['imm'])
            rs2 = Utils.binary_to_decimal(dInst['rs2'])
            data1 = register.readRF(rs1)
            data2 = register.readRF(rs2)
            result = abs(data1-data2)
            if result!=0:
                take_Branch = True
                PC.IF["PC"] += imm
        
        #JAL-type --------------------------------------------------------------------
        
        elif(dInst['type'] == 'jal'):
            imm = Utils.twos_complement(dInst['imm'])
            rd = Utils.binary_to_decimal(dInst['rd'])
            register.writeRF(rd, PC.IF["PC"]+4)
            take_Branch = True
            PC.IF["PC"] += imm << 1
        
        elif(dInst['type'] == 'HALT'):
            take_Branch = True
            PC.IF["nop"] = True

        if not take_Branch:
            PC.IF["PC"] += 4
