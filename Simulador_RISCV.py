import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import webbrowser

R = [0] * 32
M = [0] * 1000
pipeline_registers = ["NOP"] * 5
executed_values = [None] * 5
pipeline_stages = ["IF", "ID", "EX", "MEM", "WB"]
PC = 0
program = []
labels = {}
cycle = 1
saida_path = "saida.out"


def reg_index(name):
    return int(name[1:])

def parse_asm_line(line):
    line = line.strip()
    if line == "" or line.upper() == "NOP":
        return {'op': 'NOP'}
    tokens = line.replace(',', '').replace('(', ' ').replace(')', '').split()
    op = tokens[0].upper()
    if op in ['ADD', 'SUB', 'MUL', 'DIV', 'REM', 'XOR', 'AND', 'OR', 'SLL', 'SRL']:
        return {'op': op, 'rd': tokens[1], 'rs1': tokens[2], 'rs2': tokens[3]}
    elif op in ['ADDI']:
        return {'op': op, 'rd': tokens[1], 'rs1': tokens[2], 'imm': int(tokens[3])}
    elif op in ['LW']:
        return {'op': op, 'rd': tokens[1], 'imm': int(tokens[2]), 'rs1': tokens[3]}
    elif op in ['SW']:
        return {'op': op, 'rs2': tokens[1], 'imm': int(tokens[2]), 'rs1': tokens[3]}
    else:
        return {'op': 'NOP'}

def execute_instruction(instr):
    if instr['op'] == 'NOP':
        return None
    op = instr['op']
    if op == 'ADD':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] + R[reg_index(instr['rs2'])]}
    elif op == 'SUB':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] - R[reg_index(instr['rs2'])]}
    elif op == 'MUL':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] * R[reg_index(instr['rs2'])]}
    elif op == 'DIV':
        rs2 = R[reg_index(instr['rs2'])]
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] // rs2 if rs2 != 0 else 0}
    elif op == 'REM':
        rs2 = R[reg_index(instr['rs2'])]
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] % rs2 if rs2 != 0 else 0}
    elif op == 'XOR':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] ^ R[reg_index(instr['rs2'])]}
    elif op == 'AND':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] & R[reg_index(instr['rs2'])]}
    elif op == 'OR':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] | R[reg_index(instr['rs2'])]}
    elif op == 'SLL':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] << R[reg_index(instr['rs2'])]}
    elif op == 'SRL':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] >> R[reg_index(instr['rs2'])]}
    elif op == 'ADDI':
        return {'rd': instr['rd'], 'val': R[reg_index(instr['rs1'])] + instr['imm']}
    elif op == 'LW':
        addr = R[reg_index(instr['rs1'])] + instr['imm']
        val = M[addr] if 0 <= addr < len(M) else 0
        return {'rd': instr['rd'], 'val': val}
    elif op == 'SW':
        addr = R[reg_index(instr['rs1'])] + instr['imm']
        if 0 <= addr < len(M):
            M[addr] = R[reg_index(instr['rs2'])]
        return None
    return None

def write_output():
    with open(saida_path, "a") as f:
        f.write(f"Cycle {cycle}\n")
        for i, stage in enumerate(pipeline_stages):
            f.write(f"{stage}: {pipeline_registers[i]}\n")
        f.write("\nRegisters:\n")
        for i in range(32):
            f.write(f"r{i}: {R[i]}\n")
        f.write("\nMemory (non-zero):\n")
        for i, val in enumerate(M):
            if val != 0:
                f.write(f"{i}: {hex(val)}\n")
        f.write("\n====================\n\n")

def abrir_saida():
    if os.path.exists(saida_path):
        webbrowser.open(saida_path)
    else:
        messagebox.showerror("Erro", "O arquivo saida.out ainda não foi gerado.")

def next_cycle():
    global PC, cycle
    if all(inst == "NOP" for inst in pipeline_registers) and PC >= len(program):
        messagebox.showinfo("Fim", "Simulação concluída.")
        return

    if executed_values[4]:
        rd = executed_values[4].get('rd')
        val = executed_values[4].get('val')
        if rd is not None:
            R[reg_index(rd)] = val
        executed_values[4] = None

    for i in range(4, 0, -1):
        pipeline_registers[i] = pipeline_registers[i-1]
        executed_values[i] = executed_values[i-1]

    if PC < len(program):
        pipeline_registers[0] = program[PC]
        PC += 1
    else:
        pipeline_registers[0] = "NOP"
    executed_values[0] = None

    if pipeline_registers[2] != "NOP":
        executed_values[2] = execute_instruction(parse_asm_line(pipeline_registers[2]))

    update_output()
    write_output()
    cycle += 1

def update_output():
    output.delete('1.0', tk.END)
    output.insert(tk.END, f"Cycle {cycle}\n")
    for i, stage in enumerate(pipeline_stages):
        output.insert(tk.END, f"{stage}: {pipeline_registers[i]}\n")
    output.insert(tk.END, "\nRegisters:\n")
    for i in range(32):
        output.insert(tk.END, f"r{i}: {R[i]}\n")
    output.insert(tk.END, "\nMemory:\n")
    for i, v in enumerate(M):
        if v != 0:
            output.insert(tk.END, f"Addr {i}: {hex(v)}\n")

def load_asm():
    global program, PC, pipeline_registers, executed_values, R, M, cycle
    filepath = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm")])
    if not filepath:
        return
    with open(filepath, "r") as f:
        lines = f.readlines()
        program = [line.strip() for line in lines if line.strip() != ""]
    PC = 0
    R = [0] * 32
    M = [0] * 1000
    pipeline_registers = ["NOP"] * 5
    executed_values = [None] * 5
    cycle = 1
    with open(saida_path, "w") as out:
        out.write("Saída da Simulação - RISC-V\n\n")
    update_output()
    messagebox.showinfo("Arquivo carregado", os.path.basename(filepath))

root = tk.Tk()
root.title("Simulador RISC-V (Pipeline)")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

load_btn = tk.Button(top_frame, text="Carregar .asm", command=load_asm)
load_btn.pack(side=tk.LEFT, padx=5)

next_btn = tk.Button(top_frame, text="Próximo ciclo", command=next_cycle)
next_btn.pack(side=tk.LEFT, padx=5)

open_btn = tk.Button(top_frame, text="Abrir saida.out", command=abrir_saida)
open_btn.pack(side=tk.LEFT, padx=5)

output = scrolledtext.ScrolledText(root, width=80, height=30)
output.pack(padx=10, pady=10)

update_output()
root.mainloop()
