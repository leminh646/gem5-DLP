import m5
from m5.objects import *

# Define a simple system
system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())

# Use TimingSimpleCPU (basic simulation)
system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
# Define memory
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
# Add main memory
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect system to I/O and create process
system.system_port = system.membus.cpu_side_ports
binary = "/mnt/c/Users/minhh/gem5/SIMDvsScalar/scalar_vec_add"
process = Process()
process.executable = binary
process.cmd = [binary]
process.cwd = "/mnt/c/Users/minhh/gem5/SIMDvsScalar/"

system.workload = SEWorkload.init_compatible(binary)
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate and run
root = Root(full_system=False, system=system)
m5.instantiate()
print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
