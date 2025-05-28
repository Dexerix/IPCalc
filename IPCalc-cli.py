import os
import sys

def decimal_to_bin(decimal:int) -> str:
        """Converts a decimal number to binary format.

        Parameters:
            decimal (int): The decimal number to convert

        Returns:
            str: The binary representation of the decimal number
        """
        if decimal == 0:
            return '0'
        binary = ''
        while decimal > 0:
            binary = str(decimal % 2) + binary
            decimal //= 2
        return binary


def bin_to_decimal(binary:str) -> int:
        """Converts a binary number to decimal format.

        Parameters:
            binary (str): The binary number as a string

        Returns:
            int: The decimal representation of the binary number
        """
        decimal=0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        return decimal

class IPCalc:
    """A class to perform IP address calculations."""
    def __init__(self):
        """Initializes the IPCalc class."""
        pass
    
    def ip_dec_to_bin(self, ip:str) -> str:
        """Converts an IP address from decimal to binary format.

        Parameters:
            ip (str): The IP address in decimal format

        Returns:
            str: The IP address in binary format
        """
        ip_parts = ip.split('.')
        bin_parts = []
        for i in range(4):
            # Correction : utiliser ip_parts[i] et ajouter un padding à 8 bits
            part = decimal_to_bin(int(ip_parts[i])).zfill(8)
            bin_parts.append(part)
        ip_bin = '.'.join(bin_parts)
        return ip_bin

    def subnet_mask_calc(self, cidr: int) -> str:
        """Calculates the subnet mask based on the CIDR notation.

        Parameters:
            cidr (int): CIDR notation number (0-32)

        Returns:
            str: Subnet mask in decimal format (e.g. "255.255.255.0")
        """
        if not 0 <= cidr <= 32:
            raise ValueError("CIDR must be between 0 and 32")
        
        # Create binary mask based on CIDR
        binary_mask = '1' * cidr + '0' * (32 - cidr)
        
        # Split into octets
        octets = [
            binary_mask[0:8],
            binary_mask[8:16],
            binary_mask[16:24],
            binary_mask[24:32]
        ]
        
        # Convert each octet to decimal
        decimal_mask = []
        for octet in octets:
            decimal_mask.append(str(bin_to_decimal(octet)))
        
        # Join octets with dots
        return '.'.join(decimal_mask)

    def subnet_calc(self, ip: str, subnet_mask: str) -> tuple:
        """Calculates the address range according to the subnet mask.

        Parameters:
            ip (str): IP address in decimal format (e.g. "192.168.1.0")
            subnet_mask (str): Subnet mask in decimal format (e.g. "255.255.255.0")

        Returns:
            tuple: A tuple containing the first and last usable IP addresses in the range
        """
        # Convert IP and subnet mask to binary
        ip_binary = ''.join(self.ip_dec_to_bin(ip).split('.'))
        mask_binary = ''.join(self.ip_dec_to_bin(subnet_mask).split('.'))
    
        # Calculate network address (IP AND mask)
        network_binary = ''
        for i in range(32):
            network_binary += '1' if ip_binary[i] == '1' and mask_binary[i] == '1' else '0'
    
        # Calculate broadcast address (network OR NOT mask)
        broadcast_binary = ''
        for i in range(32):
            if mask_binary[i] == '1':
                broadcast_binary += network_binary[i]
            else:
                broadcast_binary += '1'
    
        # Convert network and broadcast to decimal format
        network_decimal = []
        broadcast_decimal = []
    
        for i in range(0, 32, 8):
            network_octet = network_binary[i:i+8]
            broadcast_octet = broadcast_binary[i:i+8]
            network_decimal.append(str(bin_to_decimal(network_octet)))
            broadcast_decimal.append(str(bin_to_decimal(broadcast_octet)))
    
        # First usable IP is network address + 1
        first_usable = network_decimal.copy()
        first_usable[3] = str(int(first_usable[3]) + 1)
    
        # Last usable IP is broadcast address - 1
        last_usable = broadcast_decimal.copy()
        last_usable[3] = str(int(last_usable[3]) - 1)
    
        return '.'.join(first_usable), '.'.join(last_usable)

    def broadcast_calc(self, ip: str, subnet_mask: str) -> tuple:
        """Calculates the broadcast and network address.
        
        Parameters:
            ip (str): IP address in decimal format (e.g. "192.168.1.0")
            subnet_mask (str): Subnet mask in decimal format (e.g. "255.255.255.0")
            
        Returns:
            tuple: A tuple containing the network address and broadcast address
        """
        # Convert IP and subnet mask to binary
        ip_binary = ''.join(self.ip_dec_to_bin(ip).split('.'))
        mask_binary = ''.join(self.ip_dec_to_bin(subnet_mask).split('.'))
        
        # Calculate network address (IP AND mask)
        network_binary = ''
        for i in range(32):
            network_binary += '1' if ip_binary[i] == '1' and mask_binary[i] == '1' else '0'
        
        # Calculate broadcast address (network OR NOT mask)
        broadcast_binary = ''
        for i in range(32):
            if mask_binary[i] == '1':
                broadcast_binary += network_binary[i]
            else:
                broadcast_binary += '1'
        
        # Convert network and broadcast to decimal format
        network_decimal = []
        broadcast_decimal = []
        
        for i in range(0, 32, 8):
            network_octet = network_binary[i:i+8]
            broadcast_octet = broadcast_binary[i:i+8]
            network_decimal.append(str(bin_to_decimal(network_octet)))
            broadcast_decimal.append(str(bin_to_decimal(broadcast_octet)))
        
        return '.'.join(network_decimal), '.'.join(broadcast_decimal)


def main():
    """Main function that provides a CLI interface for the IP calculator"""
    calc = IPCalc()
    
    while True:
        menu = "\nIP Calculator Menu:\n"
        menu+= "1. Calculate Subnet Mask from CIDR\n"
        menu+= "2. Calculate Network Range\n"
        menu+= "3. Calculate Network and Broadcast Addresses\n"
        menu+= "4. Convert IP to Binary\n"
        menu+= "0. Exit"
        print(menu)
        
        try:
            choice = input("\nEnter your choice (0-4): ")
            
            if choice == '0':
                print("Goodbye!")
                sys.exit(0)
                
            elif choice == '1':
                cidr = int(input("Enter CIDR (0-32): "))
                subnet_mask = calc.subnet_mask_calc(cidr)
                print(f"Subnet Mask: {subnet_mask}")
                
            elif choice == '2':
                ip = input("Enter IP address (e.g., 192.168.1.0): ")
                subnet_mask = input("Enter subnet mask (e.g., 255.255.255.0): ")
                first_ip, last_ip = calc.subnet_calc(ip, subnet_mask)
                print(f"First usable IP: {first_ip}")
                print(f"Last usable IP: {last_ip}")
                
            elif choice == '3':
                ip = input("Enter IP address (e.g., 192.168.1.0): ")
                subnet_mask = input("Enter subnet mask (e.g., 255.255.255.0): ")
                network, broadcast = calc.broadcast_calc(ip, subnet_mask)
                print(f"Network address: {network}")
                print(f"Broadcast address: {broadcast}")
                
            elif choice == '4':
                ip = input("Enter IP address (e.g., 192.168.1.0): ")
                binary = calc.ip_dec_to_bin(ip)
                print(f"Binary IP: {binary}")
                
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        input("\nPress Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen

# main
main()