class Utils(object):
    @staticmethod
    def decimal_to_binary(n, n_bits=32):
        """Convert a decimal number to binary with a fixed number of bits."""
        binary_n = bin(int(n) & (2**n_bits - 1))[2:]
        return "0" * (n_bits - len(binary_n)) + binary_n

    @staticmethod
    def binary_to_decimal(n):
        """Convert a binary string to a decimal number."""
        return int(n, 2)

    @staticmethod
    def twos_complement(n):
        """Calculate the two's complement of a binary string."""
        if n[0] == "0":
            return(int("0b" + n, 2))
        else:
            return -(
                -int(
                    "0b" + n,
                    2,
                )
                & 0b11111111111
            )

    @staticmethod
    def reset(state):
        """Reset the state of the EX stage."""
        if state.EX["nop"]: 
            return
        state.EX["Read_data1"] = 0
        state.EX["Read_data2"] = 0
        state.EX["Imm"] = 0
        state.EX["Rs"] = 0
        state.EX["Rt"] = 0
        state.EX["Wrt_reg_addr"] = -1
        state.EX["is_I_type"] = False
        state.EX["rd_mem"] = 0
        state.EX["wrt_mem"] = 0
        state.EX["alu_op"] = 0
        state.EX["wrt_enable"] = 0

    @staticmethod
    def detect_hazard(state, rs):
        """Detect hazards in the pipeline."""
        if rs == state.MEM["Wrt_reg_addr"] and state.MEM["rd_mem"]==0:
            # EX to 1st (state.MEM["ALUresult"])
            return 1
        elif rs == state.WB["Wrt_reg_addr"] and state.WB["wrt_enable"]:
            # EX to 2nd
            # MEM to 2nd (state.WB["Wrt_data"])
            return 2
        elif rs == state.MEM["Wrt_reg_addr"] and state.MEM["rd_mem"] != 0:
            # MEM to 1st (state.WB["Wrt_data"])
            state.EX["nop"] = True
            state.ID["is_hazard"] = True
            return 3
        else:
            return 0
