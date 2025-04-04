# Fast RISC-V Vector Performance Analysis Script

import argparse
import os

from m5.objects import *
from m5 import stats

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires


class RVVCore(BaseCPUCore):
    """
    Custom CPU core with RISC-V Vector Extension support
    """
    def __init__(self, elen, vlen, cpu_id, cpu_type="atomic"):
        if cpu_type == "atomic":
            core = RiscvAtomicSimpleCPU(cpu_id=cpu_id)
        elif cpu_type == "timing":
            core = RiscvTimingSimpleCPU(cpu_id=cpu_id)
        else:
            # O3 is more detailed but slower
            core = RiscvO3CPU(cpu_id=cpu_id)
            
        super().__init__(core=core, isa=ISA.RISCV)
        self.core.isa[0].elen = elen
        self.core.isa[0].vlen = vlen


requires(isa_required=ISA.RISCV)

parser = argparse.ArgumentParser()
parser.add_argument(
    "binary", 
    type=str, 
    help="Path to the RISC-V binary to run"
)
parser.add_argument(
    "-c", "--cores", 
    required=False, 
    type=int, 
    default=1,
    help="Number of CPU cores"
)
parser.add_argument(
    "-v", "--vlen", 
    required=False, 
    type=int, 
    default=256,
    help="Vector register length in bits"
)
parser.add_argument(
    "-e", "--elen", 
    required=False, 
    type=int, 
    default=64,
    help="Maximum element width in bits"
)
parser.add_argument(
    "--debug-flags",
    type=str,
    default="",
    help="Debug flags to enable"
)
parser.add_argument(
    "--cpu-type",
    type=str,
    choices=["atomic", "timing", "o3"],
    default="atomic",
    help="CPU model to use (atomic=fastest, o3=most detailed)"
)
parser.add_argument(
    "--max-ticks",
    type=int,
    default=0,
    help="Maximum number of ticks to simulate (0=no limit)"
)
parser.add_argument(
    "--stats-file",
    type=str,
    default="m5out/vector_stats.txt",
    help="Path to save statistics"
)
parser.add_argument(
    "--stats-period",
    type=int,
    default=0,
    help="Period (in ticks) between statistics dumps (0=only at end)"
)

args = parser.parse_args()

# Create cache hierarchy
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB", l1i_size="32KiB", l2_size="512KiB"
)

# Create memory system with reduced size
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
memory = SingleChannelDDR3_1600(size='512MB')

# Create processor with RVV support
processor = BaseCPUProcessor(
    cores=[RVVCore(args.elen, args.vlen, i, args.cpu_type) for i in range(args.cores)]
)

# Create board
board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the binary to run
binary = CustomResource(args.binary)
board.set_se_binary_workload(binary)

# Create and run the simulation
simulator = Simulator(board=board, full_system=False)

# Ensure stats directory exists
stats_dir = os.path.dirname(args.stats_file)
if stats_dir and not os.path.exists(stats_dir):
    os.makedirs(stats_dir)

# Configure periodic stats if requested
if args.stats_period > 0:
    stats.periodicStatDump(args.stats_period)

print(f"Beginning simulation of {args.binary} with VLEN={args.vlen}, ELEN={args.elen}, CPU={args.cpu_type}")
print(f"Statistics will be saved to {args.stats_file}")

# Run simulation with optional max ticks
if args.max_ticks > 0:
    simulator.run(max_ticks=args.max_ticks)
else:
    simulator.run()

# Dump final stats
stats.dump()
print(f"Simulation complete. Statistics saved to {args.stats_file}")
