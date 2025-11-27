"""
[ INSEIN - MAIN EXECUTABLE ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

DESCRIPTION:
Entry point for the INSEIN Advanced Stealth Scanner.
Orchestrates the kernel injection, logic engine, and UI.
Requires ROOT privileges to function (for raw socket access).

USAGE:
    sudo insein <TARGET_IP>
"""

import sys
import os
import subprocess
import time
import argparse
import asyncio
import traceback

# --- AUTO-INSTALLER REMOVED ---
# Why? Because 'setup.py' handles dependencies now. 
# Real packages don't auto-install inside the code.

from rich.live import Live
from core.ghost_engine import GhostScanner
from core.insane_logic import InsaneBrain
from ui.cyberpunk import CyberpunkDashboard
from modules.decoy import DecoyGenerator
from modules.time_travel import TimeTraveler

def check_root():
    if os.geteuid() != 0:
        print("\n[!] CRITICAL ERROR: INSEIN requires ROOT access.")
        print("    Please run with: sudo insein <TARGET>\n")
        sys.exit(1)

async def main_loop(target_ip, ports):
    # 1. Initialize
    dashboard = CyberpunkDashboard(target_ip)
    decoy_gen = DecoyGenerator()
    scanner = GhostScanner(target_ip, decoy_generator=decoy_gen)
    brain = InsaneBrain(target_ip)
    time_machine = TimeTraveler(target_ip)

    dashboard.update_state(new_log=("Initializing Kernel Injector...", "INFO"))

    # 2. Decoys
    active_decoys = decoy_gen.generate_batch(5)
    scanner.load_decoys(active_decoys)
    dashboard.update_state(new_log=(f"Generated {len(active_decoys)} Decoy IPs.", "INFO"))
    dashboard.update_state(decoy_count=len(active_decoys))

    # 3. Start UI with CRASH PROTECTION
    try:
        with Live(dashboard.render(), refresh_per_second=4, screen=True) as live:
            
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, scanner.sniff_responses)
            
            dashboard.update_state(new_log=("Ghost Protocol: ENGAGED.", "SUCCESS"))
            
            # 4. Scanning Loop
            chunk_size = 5 
            total_scanned = 0
            
            for i in range(0, len(ports), chunk_size):
                chunk = ports[i : i + chunk_size]
                await scanner.run_scan(chunk)
                total_scanned += len(chunk)
                
                new_open_ports = scanner.open_ports
                for p in new_open_ports:
                    if p not in dashboard.ports_found:
                        dashboard.update_state(new_port=p, new_log=(f"Port {p} OPEN", "SUCCESS"))
                
                analysis = brain.analyze_results(new_open_ports, total_scanned)
                if analysis["status"] == "GHOST_BLOCK":
                    dashboard.update_state(new_log=("FIREWALL DETECTED!", "CRIT"))
                    dashboard.update_state(waf_status="BLOCKING")
                    evasion = brain.suggest_evasion()
                    dashboard.update_state(new_log=(f"Switching Strategy: {evasion}", "WARN"))
                elif analysis["status"] == "HONEYPOT_DETECTED":
                    dashboard.update_state(new_log=("HONEYPOT DETECTED! Aborting.", "CRIT"))
                    break

                if 80 in chunk and 80 not in new_open_ports:
                    dashboard.update_state(new_log=("Port 80 closed. Checking History...", "INFO"))
                    try:
                        history = await time_machine.get_history()
                        if history['status'] == 'FOUND':
                            dashboard.update_state(new_log=(f"HISTORY: Was open on {history['last_seen']}", "WARN"))
                    except Exception as e:
                         dashboard.update_state(new_log=(f"OSINT Error: {str(e)}", "WARN"))

                live.update(dashboard.render())
                await asyncio.sleep(0.05)

            # --- INFINITE HOLD ---
            dashboard.update_state(new_log=("Scan Complete. SYSTEM HOLD.", "SUCCESS"))
            dashboard.update_state(new_log=("Press Ctrl+C to exit.", "INFO"))
            live.update(dashboard.render())
            
            stop_event = asyncio.Event()
            await stop_event.wait()

    except KeyboardInterrupt:
        pass 
    except Exception as e:
        raise e

def run():
    """Wrapper for setup.py entry point"""
    check_root()
    parser = argparse.ArgumentParser(description="INSEIN - Advanced Stealth Scanner")
    parser.add_argument("target", help="Target IP Address")
    parser.add_argument("--ports", help="Port range (e.g., 1-1000)", default="1-1000")
    args = parser.parse_args()

    try:
        start, end = map(int, args.ports.split('-'))
        target_ports = list(range(start, end + 1))
        asyncio.run(main_loop(args.target, target_ports))
    except KeyboardInterrupt:
        print("\n[!] User Aborted.")
    except ValueError:
        print("[!] Invalid port range.")
    except Exception:
        print("\n" + "="*50)
        print("[!] INSEIN CRASHED! REPORT THIS TO SCXR-DEV")
        print("="*50)
        traceback.print_exc()
        print("="*50)
        input("\n[PRESS ENTER TO CLOSE TERMINAL]")

if __name__ == "__main__":
    run()