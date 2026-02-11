"""
Port Scanner Module
Implements multithreaded TCP scanning for ports 1-1024
Optimized with high-performance settings and thread-safe operations
"""

import socket
import threading
from queue import Queue
from typing import List, Dict
import logging
import time

logger = logging.getLogger(__name__)


class PortScanner:
    """
    Multithreaded port scanner that identifies open ports and services
    """
    
    # Common service mappings for ports 1-1024
    COMMON_SERVICES = {
        20: 'FTP-DATA',
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        8080: 'HTTP-Proxy',
        8443: 'HTTPS-Alt'
    }
    
    def __init__(self, num_threads=200, timeout=0.5):
        """
        Initialize the port scanner with performance optimizations
        
        Args:
            num_threads: Number of concurrent scanning threads (default: 200 for optimal performance)
            timeout: Connection timeout in seconds (default: 0.5 for faster scanning)
        
        Note:
            High concurrency (200 threads) with aggressive timeout (0.5s) provides
            optimal scanning speed while maintaining thread safety through locking mechanism
        """
        self.num_threads = num_threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        self.queue = Queue()
    
    def scan_port(self, ip: str, port: int) -> bool:
        """
        Scan a single port using TCP connection
        
        Args:
            ip: Target IP address
            port: Port number to scan
            
        Returns:
            True if port is open, False otherwise
        """
        try:
            # Create a TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Attempt connection
            result = sock.connect_ex((ip, port))
            sock.close()
            
            # Result 0 means connection successful (port is open)
            return result == 0
            
        except socket.gaierror:
            logger.error(f"Hostname could not be resolved: {ip}")
            return False
        except socket.error as e:
            logger.debug(f"Could not connect to port {port}: {e}")
            return False
        except Exception as e:
            logger.debug(f"Unexpected error scanning port {port}: {e}")
            return False
    
    def get_service_name(self, port: int) -> str:
        """
        Get service name for a port number
        
        Args:
            port: Port number
            
        Returns:
            Service name or 'Unknown'
        """
        # Check common services dictionary first
        if port in self.COMMON_SERVICES:
            return self.COMMON_SERVICES[port]
        
        # Try to get service from socket library
        try:
            service = socket.getservbyport(port, 'tcp')
            return service.upper()
        except:
            return 'Unknown'
    
    def worker(self, ip: str):
        """
        Worker thread function to process ports from queue
        
        Args:
            ip: Target IP address
        """
        while True:
            port = self.queue.get()
            if port is None:
                break
            
            # Scan the port
            if self.scan_port(ip, port):
                service = self.get_service_name(port)
                
                # Thread-safe append to results
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'service': service
                    })
                    logger.info(f"Found open port: {port} ({service})")
            
            self.queue.task_done()
    
    def scan(self, ip: str, start_port: int = 1, end_port: int = 1024) -> List[Dict]:
        """
        Scan a range of ports on the target IP with performance monitoring
        
        Args:
            ip: Target IP address
            start_port: Starting port number (default: 1)
            end_port: Ending port number (default: 1024)
            
        Returns:
            List of dictionaries containing open ports and services
        """
        # Reset results
        self.open_ports = []
        
        # Record scan start time for duration measurement
        scan_start_time = time.time()
        
        logger.info(f"Starting scan of {ip} for ports {start_port}-{end_port}")
        logger.info(f"Using {self.num_threads} concurrent threads with {self.timeout}s timeout (optimized for performance)")
        
        # Create worker threads
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker, args=(ip,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Add all ports to queue
        for port in range(start_port, end_port + 1):
            self.queue.put(port)
        
        # Wait for all tasks to complete
        self.queue.join()
        
        # Stop worker threads
        for _ in range(self.num_threads):
            self.queue.put(None)
        
        for thread in threads:
            thread.join()
        
        # Calculate and log scan duration
        scan_duration = time.time() - scan_start_time
        ports_per_second = round((end_port - start_port + 1) / scan_duration, 2) if scan_duration > 0 else 0
        
        logger.info(f"Scan completed. Found {len(self.open_ports)} open ports")
        logger.info(f"Scan duration: {scan_duration:.2f} seconds | Performance: {ports_per_second} ports/sec")
        logger.info(f"Thread safety: Lock mechanism maintained for {len(self.open_ports)} concurrent port discoveries")
        
        # Sort results by port number
        self.open_ports.sort(key=lambda x: x['port'])
        
        return self.open_ports


if __name__ == '__main__':
    # Test the scanner
    logging.basicConfig(level=logging.INFO)
    scanner = PortScanner()
    
    print("Port Scanner Test")
    print("=" * 40)
    test_ip = input("Enter IP to scan (default: 127.0.0.1): ").strip() or '127.0.0.1'
    
    results = scanner.scan(test_ip)
    
    print(f"\nScan Results for {test_ip}:")
    print("-" * 40)
    if results:
        for result in results:
            print(f"Port {result['port']}: {result['service']}")
    else:
        print("No open ports found")
