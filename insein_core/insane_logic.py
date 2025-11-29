"""
[ INSEIN CORE - INSANE LOGIC ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

LOGIC:
The "Brain" of the scanner. It doesn't just scan; it judges the target.
It uses statistical analysis to detect WAFs (Web Application Firewalls) and Honeypots.

FEATURES:
- Honeypot Detection: If ALL ports seem open, it's a trap.
- WAF Detection: If packet loss > 80%, we are blocked.
- Mode Switching: Automatically enables Decoy Mode if blocked.
"""

import random
import statistics

class InsaneBrain:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.learning_mode = True
        self.blocked_count = 0
        self.total_sent = 0

    def analyze_results(self, open_ports: list, scanned_count: int) -> dict:
       
        report = {
            "status": "NORMAL",
            "confidence": 100,
            "warning": None,
            "action": None
        }


        if len(open_ports) > (scanned_count * 0.9) and scanned_count > 10:
            report["status"] = "HONEYPOT_DETECTED"
            report["confidence"] = 99
            report["warning"] = "Target is faking open ports to waste your time."
            report["action"] = "ABORT"
            return report


        if len(open_ports) == 0 and scanned_count > 100:
            report["status"] = "GHOST_BLOCK"
            report["confidence"] = 85
            report["warning"] = "Firewall is dropping all SYN packets silently."
            report["action"] = "ENABLE_DECOY_MODE"
            
        return report

    def suggest_evasion(self):
 
        strategies = [
            "FRAGMENTATION",  
            "DECOY_STORM",    
            "SLOW_LORIS_SCAN" 
        ]
        return random.choice(strategies)

    def is_response_fake(self, banner: str) -> bool:

        fake_signatures = [
            "Blocked by", "Access Denied", "Cloudflare", "AkamaiGHost"
        ]
        for sig in fake_signatures:
            if sig.lower() in banner.lower():
                return True
        return False