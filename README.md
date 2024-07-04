#IP-Meister: Network Scanner


Introduction
IP-Meister is a cross-platform application designed to scan and list devices on a network, providing their IP and MAC addresses along with their device names. The tool is perfect for network administrators and tech enthusiasts who need a cost-effective and efficient solution for network management.

<img width="634" alt="Screenshot 2024-07-04 at 12 02 58" src="https://github.com/Kenny254/IP-Meister-Network-Scanner/assets/22868045/ba860ddd-7d50-4a21-bb42-c80eb7a00eac">


#How the Code Works

#1. Initialization and Privilege Check
Initializes the Pygame mixer for sound notifications.
Checks if the script is running with root privileges, exiting if not.

<img width="564" alt="Screenshot 2024-07-04 at 12 02 42" src="https://github.com/Kenny254/IP-Meister-Network-Scanner/assets/22868045/1f9db398-4573-4c8d-8604-7b051c832066">

Network Information

#2. Retrieves the local IP address using the netifaces library.
Resolves device names using DNS lookups with the socket library.
Network Scanning:

#3. Constructs ARP packets to scan the local network IP range using scapy.
Sends the ARP packets and receives responses to identify connected devices.
GUI Components:

#4. Uses Tkinter to create the main window, including a header, footer, and a Treeview table to display device information.
Displays a progress bar and label to indicate scanning status.
Adds a button to initiate the network scan in a separate thread.
Updating the GUI:

#5. Clears the existing device list in the Treeview.
Shows a loading indicator and updates the GUI with the scanned devices once the scan is complete.
Plays a sound notification upon completion.

#6. Requirements

-Python 3
-Tkinter
-Scapy
-Netifaces
-Pygame

#Future Modifications
Enhanced Device Details: Add more information about each device, such as operating system and manufacturer.
Export Options: Enable exporting the scanned results to a CSV or JSON file.
Scheduled Scans: Add functionality to schedule automatic network scans at specified intervals.
Notification Enhancements: Integrate email or SMS notifications for scan results.
Other Capabilities:

#Cross-Platform Compatibility: Runs on Windows, macOS, and Linux.
Real-Time Updates: Provides real-time updates on the network status and connected devices.
User-Friendly Interface: Simple and intuitive interface for easy navigation and usage.


7. How to Install

a. Clone the Repository

Copy code

git clone <GitHub Repository URL>
cd <Repository Directory>

b. Install Dependencies

Copy code

pip install -r requirements.txt

c.Run the Application:

Copy code

sudo python ip_meister.py


#NOTE
Ensure you have the necessary permissions and dependencies installed to run IP-Meister smoothly. Enjoy efficient and comprehensive network scanning with IP-Meister!
