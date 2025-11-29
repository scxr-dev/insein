" 🦊 INSEIN - The Shapeshifting Network Scanner
"Why use a door when you can become the wall?"
INSEIN is an advanced, kernel-level stealth network scanner designed for ethical hacking and red-teaming. Unlike traditional scanners, INSEIN uses raw socket injection (ctypes) to bypass standard OS networking overhead, making it faster and harder to detect.
⚡ Features

* 👻 Ghost Protocol: Uses raw TCP SYN packets (Half-Open Scan) to avoid completing handshakes, minimizing logs on the target.

* 🎭 Decoy Storm: Automatically spoofs random IP addresses to confuse firewalls and IDS/IPS systems.

* 🧠 Insane Brain AI: Analyzes packet loss in real-time. If a WAF blocks you, it switches evasion strategies automatically.

* ⏳ Time Travel (OSINT): If a port is closed, it queries historical archives to see what used to be running there.

* 💻 Cyberpunk Dashboard: A high-fidelity TUI (Text User Interface) for real-time monitoring.

📦 Installation
INSEIN is available on PyPI. You can install it directly on Kali Linux, Parrot OS, or Ubuntu.
Method 1: The Standard Way

```
pip install insein
```

Method 2: For Kali Linux (Externally Managed Environment)
If you see an error saying "This environment is externally managed", use this command to force the installation safely:

```
sudo pip install insein --break-system-packages
```

🚀 Usage
⚠️ ROOT PRIVILEGES REQUIRED: Because INSEIN uses raw sockets to craft packets manually, it must be run with sudo.
Basic Scan

```
sudo insein <TARGET_IP>
```

Example: sudo insein 8.8.8.8
Scan Specific Range

```
sudo insein 192.168.1.1 --ports 1-5000
```

🛠️ Troubleshooting
1. "ModuleNotFoundError: No module named 'insein_core'"
You are running an outdated version. Update immediately:

```
sudo pip install insein --upgrade --break-system-packages
```

2. "Permission Denied" or "Socket Error"
You forgot sudo. The kernel cannot inject packets without root access.
Wrong: insein 8.8.8.8
Right: sudo insein 8.8.8.8
3. The Dashboard disappears instantly
We fixed this in v1.0.2. Please update your tool. If it persists, press Ctrl+C only when you want to exit.
📜 License & Credits
OWNER & CREATOR: 👑 R H A Ashan Imalka (scxr-dev)
⚠️ TERMS OF USE

1. Open Source for Education: You are free to view and learn from this code for educational purposes.

2. Modifications: If you modify this code or use parts of it in your own project, you MUST give clear and visible credit to R H A Ashan Imalka.

3. Commercial Use: 🚫 STRICTLY PROHIBITED without payment. If you intend to use this tool for paid penetration testing, commercial security products, or any for-profit activity, you MUST contact the owner and pay a licensing fee.

   * Contact: itrandar@gmail.com

DISCLAIMER: This tool is for authorized security auditing only. The author is not responsible for any malicious use. Scanning targets without permission is illegal.
Built with ❤️ and ☕ by scxr-dev"
 
tun this into Raw markdown codes
