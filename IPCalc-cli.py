import os
import sys

def decimal_to_bin(decimal:int) -> str:
        '''Converts a decimal number to binary format.
        
        Parameters:
            decimal (int): The decimal number to convert
            
        Returns:
            str: The binary representation of the decimal number
        '''
        if decimal == 0:
            return '0'
        binary = ''
        while decimal > 0:
            binary = str(decimal % 2) + binary
            decimal //= 2
        return binary


def bin_to_decimal(binary:str) -> int:
        '''Converts a binary number to decimal format.
        
        Parameters:
            binary (str): The binary number as a string
            
        Returns:
            int: The decimal representation of the binary number
        '''
        decimal=0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        return decimal

class IPCalc:
    '''A class to perform IP address calculations.'''
    def __init__(self):
        '''Initializes the IPCalc class.'''
        pass
    
    def ipDecToBin(self, ip:str) -> str:
        '''Converts an IP address from decimal to binary format.
        
        Parameters:
            ip (str): The IP address in decimal format
            
        Returns:
            str: The IP address in binary format
        '''
        ip_parts = ip.split('.')
        ip_bin = ''
        bin_parts = []
        for i in range(4):
            part = decimal_to_bin(int(ip_parts[i-1]))
            bin_parts.append(part)
        ip_bin = '.'.join(bin_parts)   
        return ip_bin

    def subnetMaskCalc(self):
        '''Calculates the subnet mask based on the CIDR notation.
        
        Parameters:
            
            
        Returns:
            
        '''
        pass

    def subnetCalc(self):
        '''Calculates the adress range according to the subnet mask.
        
        Parameters:
            
            
        Returns:
            '''
        pass

    def broadcastCalc(self):
        '''Calculates the broadcast and network address.
        
        Parameters:
            
            
        Returns:
            '''
        pass


def main():
    pass


# Main
<<<<<<< HEAD
=======
lol=IPCalc()
lol.ipDecToBin(ip='192.168.1.1')
>>>>>>> 1d76b2a (Implement ipDecToBin method in IPCalc class for converting decimal IP addresses to binary format)
