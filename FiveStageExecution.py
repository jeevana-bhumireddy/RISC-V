from FiveStageDecode import FiveStageDecode

class FiveStageExecution(object):
    def __init__(self):
        pass

    def IF(self, state, imem):
        instruction = imem.readInstr(state.IF["PC"])
        if instruction == "1"*32:
            state.IF["nop"] = True
            state.ID["nop"] = True
        else:
            state.ID["Instr"] = instruction
            state.IF["PC"] += 4

    def ID(self, state, register):
        state.ID["is_hazard"] = False
        FiveStageDecode.FS_decode(state,register)

    def EX(self, state):
        state.MEM["wrt_enable"]=state.EX["wrt_enable"]
        state.MEM["Wrt_reg_addr"]=state.EX["Wrt_reg_addr"]
        state.MEM["rd_mem"]=state.EX["rd_mem"]
        state.MEM["wrt_mem"]=state.EX["wrt_mem"] 
        state.MEM["Rs"]=state.EX["Rs"] 
        state.MEM["Rt"]=state.EX["Rt"] 

        #R-type----------------------------------------------------------------------

        if (state.EX["alu_op"]=='add'):
            state.MEM["ALUresult"]=(state.EX["Read_data1"]) + (state.EX["Read_data2"])

        if (state.EX["alu_op"]=='sub'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] - state.EX["Read_data2"]

        if (state.EX["alu_op"]=='xor'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] ^ state.EX["Read_data2"]
            # 

        if (state.EX["alu_op"]=='or'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] | state.EX["Read_data2"]

        if (state.EX["alu_op"]=='and'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] & state.EX["Read_data2"]

        #I-type --------------------------------------------------------------------

        if (state.EX["alu_op"]=='addi'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] + state.EX["Imm"]

        if (state.EX["alu_op"]=='xori'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] ^ state.EX["Imm"]

        if (state.EX["alu_op"]=='ori'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] | state.EX["Imm"]  

        if (state.EX["alu_op"]=='andi'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] & state.EX["Imm"]  

        #Load --------------------------------------------------------------------

        if (state.EX["alu_op"]=='lw'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] + state.EX["Imm"]
            # 
            # 

        #Store --------------------------------------------------------------------

        if (state.EX["alu_op"]=='sw'):
            state.MEM["ALUresult"]=state.EX["Read_data1"] + state.EX["Imm"] 
            state.MEM["Store_data"]=state.EX["Read_data2"] 

        #B-type --------------------------------------------------------------------

        # if (state.EX["alu_op"]=='beq'):
        #     result=abs(state.EX["Read_data1"] - state.EX["Read_data2"])
        #     if result==0:
        #         state.IF["PC"]+= state.EX["Imm"]

        # if (state.EX["alu_op"]=='bne'):
        #     result=abs(state.EX["Read_data1"] - state.EX["Read_data2"])  
        #     if result!=0:
        #         state.IF["PC"]+= state.EX["Imm"]

        #JAL --------------------------------------------------------------------

        if (state.EX["alu_op"]=='jal'): 
            state.MEM["Wrt_reg_addr"]=state.EX["Wrt_reg_addr"]
            state.MEM["ALUresult"] = state.EX["Read_data1"] + state.EX["Read_data2"]
            # state.EX["PC"]+= state.EX["Imm"]

        # elif not take_Branch:
        # PC.IF["PC"] += 4

        #HALT --------------------------------------------------------------------

        else:
            None 

    def Mem(self, state,dataMem):
        state.WB["Rs"] = state.MEM["Rs"]
        state.WB["Rt"] = state.MEM["Rt"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]
        
        if(state.MEM["wrt_mem"]==1):
            # writing back to datamem with store
            dataMem.writeDataMem(state.MEM["ALUresult"] , state.MEM["Store_data"])
            
        elif(state.MEM["rd_mem"]==1):
            # reading from register with load
            state.WB["Wrt_data"] = dataMem.readDataMem(state.MEM["ALUresult"])
            # 
            
        elif(state.MEM["wrt_mem"]==0 & state.MEM["rd_mem"]==0):
            # any other branch/R-type instruction does not require memory
            state.WB["Wrt_data"] = state.MEM["ALUresult"]

        #HALT --------------------------------------------------------------------

        else:
            pass

        
        

    def WB(self, state, register):
        if (state.WB["wrt_enable"]==1):
            register.writeRF(state.WB["Wrt_reg_addr"], state.WB["Wrt_data"])

