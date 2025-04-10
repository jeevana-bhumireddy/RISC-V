class SingleStageDecode(object):
    @staticmethod
    def decode(instruction):
        decodedInst = {}
        rs1 = None
        rs2 = None
        rd = None
        imm = None

        if instruction[-7:] == "0110011":  # R-type
            rs1 = instruction[-20:-15]
            rs2 = instruction[-25:-20]
            rd = instruction[-12:-7]

            if instruction[-15:-12] == "000" and instruction[-32:-25] == "0000000":
                # add func
                decodedInst["type"] = "add"

            elif instruction[-15:-12] == "000" and instruction[-32:-25] == "0100000":
                # sub func
                decodedInst["type"] = "sub"

            elif instruction[-15:-12] == "100" and instruction[-32:-25] == "0000000":
                # xor func
                decodedInst["type"] = "xor"

            elif instruction[-15:-12] == "110" and instruction[-32:-25] == "0000000":
                # or func
                decodedInst["type"] = "or"

            elif instruction[-15:-12] == "111" and instruction[-32:-25] == "0000000":
                # AND func
                decodedInst["type"] = "and"

        elif instruction[-7:] == "0010011":  # I-type
            rs1 = instruction[-20:-15]
            imm = instruction[-32:-20]
            rd = instruction[-12:-7]

            if instruction[-15:-12] == "000":
                # Addi func
                decodedInst["type"] = "addi"

            elif instruction[-15:-12] == "100":
                # xori
                decodedInst["type"] = "xori"

            elif instruction[-15:-12] == "110":
                # ori
                decodedInst["type"] = "ori"

            elif instruction[-15:-12] == "111":
                # andi
                decodedInst["type"] = "andi"

        elif instruction[-7:] == "1100011":  # B-type

            rs1 = instruction[-20:-15]
            imm = "".join(
                (
                    instruction[-32],
                    instruction[-8],
                    instruction[-31:-25],
                    instruction[-12:-8],
                    "0",
                )
            )
            rs2 = instruction[-25:-20]

            if instruction[-15:-12] == "000":
                # BEQ func
                decodedInst["type"] = "beq"

            elif instruction[-15:-12] == "001":
                # BNE
                decodedInst["type"] = "bne"

        elif instruction[-7:] == "0000011":  # load
            rs1 = instruction[-20:-15]
            imm = instruction[-32:-20]
            rd = instruction[-12:-7]
            decodedInst["type"] = "lw"

        elif instruction[-7:] == "0100011":  # store
            rs1 = instruction[-20:-15]
            imm = "".join((instruction[-32:-25], instruction[-12:-7]))
            rs2 = instruction[-25:-20]
            decodedInst["type"] = "sw"
        
        elif instruction[-7:] == "1101111":  # JAL
            imm = "".join((instruction[-32], instruction[-20:-12], instruction[-21],instruction[-31:-21] ))
            rd = instruction[-12:-7]
            decodedInst["type"] = "jal"
        
        elif instruction[-7:] == "1111111":
            decodedInst["type"] = "HALT"

        decodedInst["rs1"] = rs1
        decodedInst["rs2"] = rs2
        decodedInst["rd"] = rd
        decodedInst["imm"] = imm

        

        return decodedInst