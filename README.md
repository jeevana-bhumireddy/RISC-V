# ⚙️ RISC-V Single-Stage Processor

This project implements a **RISC-V single-stage processor** capable of executing **one instruction per clock cycle**.  
The design follows **RISC-V RV32I architecture** principles and focuses on simplicity, correctness, and efficiency — ideal for understanding the fundamentals of processor microarchitecture.

---

## 🧠 Overview

The processor executes **fetch, decode, execute, memory access, and write-back** within a single pipeline stage.  
It integrates all major components — **instruction memory**, **decoder**, **ALU**, **data memory**, and **register file** — into one clock-driven datapath, achieving one-instruction-per-cycle (OIPC) performance for supported instructions.

The project evaluates **CPI (Cycles Per Instruction)** and **IPC (Instructions Per Cycle)** across multiple test programs to verify efficiency and RISC-V compliance.

---

## 🧩 Key Features
- Single-cycle RISC-V RV32I processor core  
- Executes **one instruction per clock cycle**  
- Includes:
  - Instruction Memory  
  - Control and Decode Unit  
  - ALU (Arithmetic Logic Unit)  
  - Register File (32 general-purpose registers)  
  - Data Memory  
- Supports arithmetic, logical, load/store, and branch operations  
- Verilog testbench for simulation and waveform verification  
- Evaluated on performance metrics: **CPI** and **IPC**

---

## 🛠 Tools & Technologies
- **Hardware Description:** Verilog HDL  
- **Simulation:** ModelSim / Vivado Simulator  
- **FPGA (Optional):** Basys 3 or similar Xilinx board  
- **Synthesis Tool:** Xilinx Vivado 2022.2+  
- **Testbench:** Custom Verilog test programs for instruction validation  


