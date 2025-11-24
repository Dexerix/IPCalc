from os import system, name, _exit

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

    def get_ip_class(self, ip: str) -> tuple:
        """Determines the IP address class and its standard subnet mask.
        
        Parameters:
            ip (str): IP address in decimal format (e.g. "192.168.1.0")
            
        Returns:
            tuple: A tuple containing (class_name, default_cidr, default_mask)
        """
        first_octet = int(ip.split('.')[0])
        
        if 0 <= first_octet <= 127:
            return ('A', 8, '255.0.0.0')
        elif 128 <= first_octet <= 191:
            return ('B', 16, '255.255.0.0')
        elif 192 <= first_octet <= 223:
            return ('C', 24, '255.255.255.0')
        elif 224 <= first_octet <= 239:
            return ('D', None, None)  # Multicast
        else:
            return ('E', None, None)  # Reserved

    def calculate_all_subnets(self, ip: str, subnet_mask: str) -> dict:
        """Calculates complete subnet information including all subnets created by the mask.
        
        Parameters:
            ip (str): IP address in decimal format (e.g. "192.168.1.0")
            subnet_mask (str): Subnet mask in decimal format (e.g. "255.255.255.0")
            
        Returns:
            dict: Dictionary containing:
                - 'ip_class': The IP address class (A, B, C, D, or E)
                - 'default_mask': The default mask for this IP class
                - 'subnet_mask': The provided subnet mask
                - 'cidr': CIDR notation of the subnet mask
                - 'network_address': Network address for the given IP
                - 'broadcast_address': Broadcast address for the given IP
                - 'first_usable': First usable IP address
                - 'last_usable': Last usable IP address
                - 'total_hosts': Total number of usable hosts per subnet
                - 'subnets_count': Number of subnets created from the default class
                - 'subnet_info': List of all subnet ranges
        """
        # Get IP class information
        ip_class, default_cidr, default_mask = self.get_ip_class(ip)
        
        # Calculate CIDR from subnet mask
        mask_binary = ''.join(self.ip_dec_to_bin(subnet_mask).split('.'))
        cidr = mask_binary.count('1')
        
        # Calculate network and broadcast for the given IP
        network_address, broadcast_address = self.broadcast_calc(ip, subnet_mask)
        first_usable, last_usable = self.subnet_calc(ip, subnet_mask)
        
        # Calculate total hosts per subnet
        total_hosts = (2 ** (32 - cidr)) - 2 if cidr < 31 else 0
        
        # Calculate number of subnets created from default class
        subnets_count = 0
        if default_cidr is not None and cidr > default_cidr:
            subnets_count = 2 ** (cidr - default_cidr)
        
        # Calculate all subnet ranges if subnetting occurred
        subnet_list = []
        if subnets_count > 0 and default_mask is not None:
            # Get the network address of the entire class network
            class_network, _ = self.broadcast_calc(ip, default_mask)
            
            # Calculate subnet size
            subnet_size = 2 ** (32 - cidr)
            
            # Convert class network to integer for easier calculation
            octets = [int(o) for o in class_network.split('.')]
            base_ip = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
            
            # Generate all subnets
            for i in range(min(subnets_count, 100)):  # Limit to 100 subnets for display
                subnet_base = base_ip + (i * subnet_size)
                
                # Convert back to dotted decimal
                subnet_ip = f"{(subnet_base >> 24) & 0xFF}.{(subnet_base >> 16) & 0xFF}.{(subnet_base >> 8) & 0xFF}.{subnet_base & 0xFF}"
                
                # Calculate subnet details
                net_addr, bcast_addr = self.broadcast_calc(subnet_ip, subnet_mask)
                first_ip, last_ip = self.subnet_calc(subnet_ip, subnet_mask)
                
                subnet_list.append({
                    'subnet_number': i + 1,
                    'network_address': net_addr,
                    'first_usable': first_ip,
                    'last_usable': last_ip,
                    'broadcast_address': bcast_addr
                })
        
        return {
            'ip_class': ip_class,
            'default_mask': default_mask,
            'subnet_mask': subnet_mask,
            'cidr': cidr,
            'network_address': network_address,
            'broadcast_address': broadcast_address,
            'first_usable': first_usable,
            'last_usable': last_usable,
            'total_hosts': total_hosts,
            'subnets_count': subnets_count if subnets_count > 0 else 1,
            'subnet_info': subnet_list if subnet_list else [{
                'subnet_number': 1,
                'network_address': network_address,
                'first_usable': first_usable,
                'last_usable': last_usable,
                'broadcast_address': broadcast_address
            }]
        }

    def subnet_info_calc(self, ip: str, cidr: int) -> dict:
        """Calculates complete subnet information from IP address and CIDR.
        
        Parameters:
            ip (str): IP address in decimal format (e.g. "192.168.1.0")
            cidr (int): CIDR notation number (0-32)
            
        Returns:
            dict: Dictionary containing:
                - 'subnet_mask': Subnet mask in decimal format
                - 'network_address': Network address
                - 'broadcast_address': Broadcast address
                - 'first_usable': First usable IP address
                - 'last_usable': Last usable IP address
                - 'total_hosts': Total number of usable hosts
        """
        # Calculate subnet mask from CIDR
        subnet_mask = self.subnet_mask_calc(cidr)
        
        # Calculate network and broadcast addresses
        network_address, broadcast_address = self.broadcast_calc(ip, subnet_mask)
        
        # Calculate usable IP range
        first_usable, last_usable = self.subnet_calc(ip, subnet_mask)
        
        # Calculate total number of usable hosts (2^(32-cidr) - 2)
        total_hosts = (2 ** (32 - cidr)) - 2 if cidr < 31 else 0
        
        return {
            'subnet_mask': subnet_mask,
            'network_address': network_address,
            'broadcast_address': broadcast_address,
            'first_usable': first_usable,
            'last_usable': last_usable,
            'total_hosts': total_hosts
        }

def main():
    """Main function that provides a CLI interface for the IP calculator"""
    calc = IPCalc()
    
    is_loop_ok = True
    while is_loop_ok:
        system('cls' if name == 'nt' else 'clear')  # Clear screen
        menu = "\nIP Calculator Menu:\n"
        menu+= "1. Calculate Subnet Mask from CIDR\n"
        menu+= "2. Calculate Network Range\n"
        menu+= "3. Calculate Network and Broadcast Addresses\n"
        menu+= "4. Convert IP to Binary\n"
        menu+= "5. Calculate Complete Subnet Information\n"
        menu+= "6. Calculate All Subnets from IP Class\n"
        menu+= "0. Exit"
        print(menu)
        
        try:
            choice = input("\nEnter your choice (0-6): ")
            if choice == '0':
                print("Goodbye!")
                exit()
                
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

            elif choice == '5':
                ip = input("Enter IP address (e.g., 192.168.1.0): ")
                cidr = int(input("Enter CIDR (0-32): "))
                info = calc.subnet_info_calc(ip, cidr)
                print("\n=== Subnet Information ===")
                for key, value in info.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
                    
            elif choice == '6':
                ip = input("Enter IP address (e.g., 192.168.1.0): ")
                subnet_mask = input("Enter subnet mask (e.g., 255.255.255.192): ")
                result = calc.calculate_all_subnets(ip, subnet_mask)
                
                print("\n=== IP Class Information ===")
                print(f"IP Class: {result['ip_class']}")
                print(f"Default Mask: {result['default_mask']}")
                print(f"Subnet Mask: {result['subnet_mask']}")
                print(f"CIDR: /{result['cidr']}")
                print(f"\n=== Current Subnet ===")
                print(f"Network Address: {result['network_address']}")
                print(f"First Usable IP: {result['first_usable']}")
                print(f"Last Usable IP: {result['last_usable']}")
                print(f"Broadcast Address: {result['broadcast_address']}")
                print(f"Total Hosts per Subnet: {result['total_hosts']}")
                print(f"Number of Subnets: {result['subnets_count']}")
                
                if len(result['subnet_info']) > 1:
                    print(f"\n=== All Subnets (showing up to 100) ===")
                    for subnet in result['subnet_info']:
                        print(f"\nSubnet #{subnet['subnet_number']}:")
                        print(f"  Network: {subnet['network_address']}")
                        print(f"  Usable Range: {subnet['first_usable']} - {subnet['last_usable']}")
                        print(f"  Broadcast: {subnet['broadcast_address']}")
                
            else:
                print("Invalid choice. Please enter a number between 0 and 6.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        input("\nPress Enter to continue...")
        system('cls' if name == 'nt' else 'clear')  # Clear screen

# main
main()