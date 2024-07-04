import os
import sys
import tkinter as tk
from tkinter import ttk
import threading
import socket
import netifaces
from scapy.all import ARP, Ether, srp
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Check for root privileges
if os.geteuid() != 0:
    print("This script requires root privileges. Please run it with sudo.")
    sys.exit(1)

# Function to get the local network IP address
def get_local_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo' or interface == 'lo0':
            continue
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for link in addresses[netifaces.AF_INET]:
                if 'addr' in link:
                    ip = link['addr']
                    if not ip.startswith("127."):
                        return ip
    return None

# Function to resolve device names using DNS lookup
def resolve_device_name(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror as e:
        print(f"DNS resolution error for {ip_address}: {e}")
        return "Unknown"

# Function to get devices on the network
def get_devices_on_network():
    local_ip = get_local_ip()
    if not local_ip:
        print("Could not find the local IP address.")
        return []
    
    ip_range = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
    print(f"Scanning IP range: {ip_range}")
    
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for idx, (sent, received) in enumerate(result, start=1):
        device_name = resolve_device_name(received.psrc)
        devices.append({'number': idx, 'name': device_name, 'ip': received.psrc, 'mac': received.hwsrc})
    
    print(f"Found devices: {devices}")
    return devices

# Function to scan network and update GUI
def scan_and_update():
    # Clear the Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Display loader
    progress_label.config(text="Scanning in progress...")
    progress_bar.start()

    # Scan the network in a separate thread
    devices = get_devices_on_network()

    # Stop loader
    progress_label.config(text="Scan complete.")
    progress_bar.stop()

    # Play sound when scan is complete
    pygame.mixer.music.load("done.mp3")
    pygame.mixer.music.play()

    # Update the Treeview with the scanned devices
    for device in devices:
        tree.insert("", "end", values=(device['number'], device['name'], device['ip'], device['mac']))

# Initialize the main window
root = tk.Tk()
root.title("IPMeister - Network Scanner")

# Set header and footer background color to yellow
header_frame = tk.Frame(root, bg="#ffc03d", height=50)
header_frame.pack(fill=tk.X)

# Header label
header_label = tk.Label(header_frame, text="IPMeister", font=("Helvetica", 20), bg="#ffc03d")
header_label.pack(pady=5)

# Set footer with developer info
footer_frame = tk.Frame(root, bg="#ffc03d", height=20)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

# Footer label
footer_label = tk.Label(footer_frame, text="GoHybrid Developers @ 2024", font=("Helvetica", 10), bg="#ffc03d")
footer_label.pack(pady=5)

# Create a Treeview to display the devices in a table format
style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 12))
style.configure("Treeview", font=("Helvetica", 10), rowheight=25)  # Adjust font and row height

columns = ("#", "Device Name", "IP Address", "MAC Address")
tree = ttk.Treeview(root, columns=columns, show="headings", style="Treeview")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, minwidth=50, width=150, anchor=tk.CENTER)  # Adjust column width and alignment

tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Progress bar and label for loader
progress_label = tk.Label(root, text="", font=("Helvetica", 12))
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack()

# Create a styled button for scanning
scan_button = tk.Button(root, text="Scan Devices", command=lambda: threading.Thread(target=scan_and_update).start(), bg="#ffc03d", fg="black", font=("Helvetica", 12))
scan_button.pack(pady=10)

# Run the application
root.mainloop()
