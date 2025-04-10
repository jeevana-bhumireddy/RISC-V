from utils import Utils

class FiveStageDecode(object):
    @staticmethod
    def FS_decode(state,register):
        Utils.reset(state)
        instruction = state.ID["Instr"]

        #R-type---------------------------------------------------------------------------------

        if instruction[-7:] == "0110011":  
            state.EX["Rs"] = instruction[-20:-15]
            state.EX["Rt"] = instruction[-25:-20]
            state.EX["Wrt_reg_addr"] = instruction[-12:-7]

            rs1 = Utils.binary_to_decimal(state.EX["Rs"])
            rs2 = Utils.binary_to_decimal(state.EX["Rt"])
            state.EX["Wrt_reg_addr"] = Utils.binary_to_decimal(state.EX["Wrt_reg_addr"])

            hazard_rs1 = Utils.detect_hazard(state, rs1)
            hazard_rs2 = Utils.detect_hazard(state, rs2)

            if hazard_rs1 == 3 or hazard_rs2 ==3:
                return 

            if hazard_rs1 == 1:
                state.EX["Read_data1"] = state.MEM["ALUresult"]
            elif hazard_rs1 == 2:
                state.EX["Read_data1"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data1"] = register.readRF(rs1)

            if hazard_rs2 == 1:
                state.EX["Read_data2"] = state.MEM["ALUresult"]
            elif hazard_rs2 == 2:
                state.EX["Read_data2"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data2"] = register.readRF(rs2)  
            

            state.EX["wrt_enable"] = 1
            state.EX["is_I_type"] = False

            if instruction[-15:-12] == "000" and instruction[-32:-25] == "0000000":
                # add func
                state.EX["alu_op"] = "add"

            elif instruction[-15:-12] == "000" and instruction[-32:-25] == "0100000":
                # sub func
                state.EX["alu_op"] = "sub"

            elif instruction[-15:-12] == "100" and instruction[-32:-25] == "0000000":
                # xor func
                state.EX["alu_op"] = "xor"

            elif instruction[-15:-12] == "110" and instruction[-32:-25] == "0000000":
                # or func
                state.EX["alu_op"] = "or"

            elif instruction[-15:-12] == "111" and instruction[-32:-25] == "0000000":
                # AND func
                state.EX["alu_op"] = "and"

        #I-type ---------------------------------------------------------------------------------


        elif instruction[-7:] == "0010011":  # I-type
            state.EX["Rs"] = instruction[-20:-15]
            state.EX["Imm"] = instruction[-32:-20]
            state.EX["Wrt_reg_addr"] = instruction[-12:-7]
            
            rs1 = Utils.binary_to_decimal(state.EX["Rs"])
            state.EX["Wrt_reg_addr"] = Utils.binary_to_decimal(state.EX["Wrt_reg_addr"])

            hazard_rs1 = Utils.detect_hazard(state, rs1)
            
            if hazard_rs1 == 3:
                return 

            if hazard_rs1 == 1:
                state.EX["Read_data1"] = state.MEM["ALUresult"]
            elif hazard_rs1 == 2:
                state.EX["Read_data1"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data1"] = register.readRF(rs1)

            state.EX["is_I_type"] = True
            state.EX["wrt_enable"] = 1

            if instruction[-15:-12] == "000":
                # Addi func
                state.EX["alu_op"] = "addi"

            elif instruction[-15:-12] == "100":
                # xori
                state.EX["alu_op"] = "xori"

            elif instruction[-15:-12] == "110":
                # ori
                state.EX["alu_op"] = "ori"

            elif instruction[-15:-12] == "111":
                # andi
                state.EX["alu_op"] = "andi"
        
        #Load-type --------------------------------------------------------------------
        
        elif instruction[-7:] == "0000011":  
            state.EX["Rs"] = instruction[-20:-15]
            state.EX["Imm"] = instruction[-32:-20]
            state.EX["Wrt_reg_addr"] = instruction[-12:-7]

            rs1 = Utils.binary_to_decimal(state.EX["Rs"])   
            state.EX["Wrt_reg_addr"] = Utils.binary_to_decimal(state.EX["Wrt_reg_addr"])

            hazard_rs1 = Utils.detect_hazard(state, rs1)
            
            if hazard_rs1 == 3:
                return 

            if hazard_rs1 == 1:
                state.EX["Read_data1"] = state.MEM["ALUresult"]
            elif hazard_rs1 == 2:
                state.EX["Read_data1"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data1"] = register.readRF(rs1)

            state.EX["rd_mem"] = 1
            state.EX["wrt_enable"] = 1
            state.EX["is_I_type"] = True
            state.EX["alu_op"] = "lw"
            
        #Store-type ---------------------------------------------------------------------------------------

        elif instruction[-7:] == "0100011": 
            state.EX["Rs"] = instruction[-20:-15]
            state.EX["Imm"] = "".join((instruction[-32:-25], instruction[-12:-7]))
            state.EX["Rt"] = instruction[-25:-20]

            rs1 = Utils.binary_to_decimal(state.EX["Rs"])
            rs2 = Utils.binary_to_decimal(state.EX["Rt"])

            hazard_rs1 = Utils.detect_hazard(state, rs1)
            hazard_rs2 = Utils.detect_hazard(state, rs2)
            
            if hazard_rs1 == 3 or hazard_rs2 ==3:
                return 

            if hazard_rs1 == 1:
                state.EX["Read_data1"] = state.MEM["ALUresult"]
            elif hazard_rs1 == 2:
                state.EX["Read_data1"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data1"] = register.readRF(rs1)

            if hazard_rs2 == 1:
                state.EX["Read_data2"] = state.MEM["ALUresult"]
            elif hazard_rs2 == 2:
                state.EX["Read_data2"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data2"] = register.readRF(rs2) 

            state.EX["is_I_type"] = True
            state.EX["wrt_mem"] = 1
            state.EX["alu_op"] = "sw"

        #Branch-type --------------------------------------------------------------------

        elif instruction[-7:] == "1100011":

            state.EX["Rs"] = instruction[-20:-15]
            state.EX["Imm"] = "".join(
                (
                    instruction[-32],
                    instruction[-8],
                    instruction[-31:-25],
                    instruction[-12:-8],
                    "0",
                )
            )
            state.EX["Rt"] = instruction[-25:-20]

            rs1 = Utils.binary_to_decimal(state.EX["Rs"])
            rs2 = Utils.binary_to_decimal(state.EX["Rt"])

            hazard_rs1 = Utils.detect_hazard(state, rs1)
            hazard_rs2 = Utils.detect_hazard(state, rs2)

            if hazard_rs1 == 3 or hazard_rs2 ==3:
                return 

            if hazard_rs1 == 1:
                state.EX["Read_data1"] = state.MEM["ALUresult"]
            elif hazard_rs1 == 2:
                state.EX["Read_data1"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data1"] = register.readRF(rs1)

            if hazard_rs2 == 1:
                state.EX["Read_data2"] = state.MEM["ALUresult"]
            elif hazard_rs2 == 2:
                state.EX["Read_data2"] = state.WB["Wrt_data"]
            else:
                state.EX["Read_data2"] = register.readRF(rs2)        

            if instruction[-15:-12] == "000":
                # BEQ func
                state.EX["alu_op"] = "beq"

            elif instruction[-15:-12] == "001":
                # BNE
                state.EX["alu_op"] = "bne"
            
            result = abs(state.EX["Read_data1"] - state.EX["Read_data2"])
            if bool(result) == (state.EX["alu_op"] == "bne"):
                state.IF["PC"] += Utils.twos_complement(state.EX["Imm"]) - 4
                state.ID["nop"] = state.EX["nop"] = True
            else: 
                state.EX["nop"] = True

        #JAL-type ---------------------------------------------------------------------------------------------------------
        
        elif instruction[-7:] == "1101111":  
            state.EX["Imm"] = "".join((instruction[-32], instruction[-20:-12], instruction[-21],instruction[-31:-21],"0" ))
            state.EX["Wrt_reg_addr"] = instruction[-12:-7]
            state.EX["Wrt_reg_addr"] = Utils.binary_to_decimal(state.EX["Wrt_reg_addr"])
            state.EX["Read_data1"] = state.IF["PC"] - 4
            state.EX["Read_data2"] = 4
            state.EX["wrt_enable"] = 1
            state.EX["alu_op"] = "jal"
            state.IF["PC"] += Utils.twos_complement(state.EX["Imm"]) - 4
            state.ID["nop"] = True
        
        else:
            state.IF["nop"] = True

        if state.EX["is_I_type"]:
            state.EX["Imm"] = Utils.twos_complement(state.EX["Imm"])
            