"""
[ INSEIN UI - CYBERPUNK DASHBOARD ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

DESCRIPTION:
Implements a high-fidelity TUI (Text User Interface) using the Rich library.
Displays real-time scan metrics, detected ports, evasion status, and kernel 
activity visualization.
"""

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from datetime import datetime

class CyberpunkDashboard:
    def __init__(self, target_ip):
        self.console = Console()
        self.target = target_ip
        self.start_time = datetime.now()
        self.logs = []
        self.ports_found = []
        self.waf_status = "ANALYZING"
        self.decoy_count = 0
        self.layout = Layout()
        
        self._init_layout()

    def _init_layout(self):
        """Splits the terminal into sections: Header, Stats, Map, Logs."""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        self.layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right", ratio=2, minimum_size=60)
        )
        self.layout["left"].split(
            Layout(name="stats"),
            Layout(name="ports")
        )

    def _generate_header(self) -> Panel:
        """Creates the top status bar."""
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        
        title = Text("INSEIN // ADVANCED KERNEL SCANNER", style="bold magenta")
        author = Text("DEV: R H A Ashan Imalka (scxr-dev)", style="dim white")
        
        grid.add_row(title, author)
        return Panel(grid, style="magenta")

    def _generate_stats(self) -> Panel:
        """Creates the statistics panel."""
        table = Table(show_header=False, expand=True, box=None)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="bold white")
        
        duration = datetime.now() - self.start_time
        
        table.add_row("TARGET", self.target)
        table.add_row("UPTIME", str(duration).split('.')[0])
        table.add_row("WAF STATE", self.waf_status)
        table.add_row("DECOYS", f"{self.decoy_count} ACTIVE")
        table.add_row("MODE", "KERNEL_INJECTION (uid=0)")
        
        return Panel(table, title="[ SYSTEMS ]", border_style="cyan")

    def _generate_ports(self) -> Panel:
        """Creates the list of discovered open ports."""
        table = Table(show_header=True, expand=True, header_style="bold green")
        table.add_column("PORT", width=8)
        table.add_column("SERVICE")
        
        # Show last 10 ports found
        for port in self.ports_found[-10:]:
            table.add_row(str(port), "UNKNOWN/TCP") 
            
        return Panel(table, title="[ OPEN PORTS ]", border_style="green")

    def _generate_logs(self) -> Panel:
        """Creates the scrolling log window."""
        log_text = Text()
        for timestamp, msg, level in self.logs[-12:]:
            color = "white"
            if level == "INFO": color = "blue"
            elif level == "WARN": color = "yellow"
            elif level == "CRIT": color = "red bold"
            elif level == "SUCCESS": color = "green"
            
            log_text.append(f"[{timestamp}] {msg}\n", style=color)
            
        return Panel(log_text, title="[ KERNEL LOGS ]", border_style="white")

    def _generate_footer(self) -> Panel:
        """Creates a footer to fix the visual glitch."""
        text = Text("STATUS: SCANNING COMPLETE | PRESS CTRL+C TO EXIT", justify="center", style="bold red blinking")
        return Panel(text, style="red")

    def update_state(self, new_log=None, new_port=None, waf_status=None, decoy_count=None):
        """Updates internal state variables."""
        if new_log:
            time_str = datetime.now().strftime("%H:%M:%S")
            self.logs.append((time_str, new_log[0], new_log[1]))
        if new_port and new_port not in self.ports_found:
            self.ports_found.append(new_port)
        if waf_status:
            self.waf_status = waf_status
        if decoy_count is not None:
            self.decoy_count = decoy_count

    def render(self) -> Layout:
        """Compiles the layout for the Live display."""
        self.layout["header"].update(self._generate_header())
        self.layout["stats"].update(self._generate_stats())
        self.layout["ports"].update(self._generate_ports())
        self.layout["right"].update(self._generate_logs())
        self.layout["footer"].update(self._generate_footer())
        return self.layout