"""
Risk Engine Module
Implements risk assessment, scoring, and mitigation recommendations
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Risk assessment engine that evaluates open ports and provides mitigation strategies
    """
    
    # Risk level definitions and scoring
    RISK_LEVELS = {
        'HIGH': {'score': 30, 'color': '#dc3545'},
        'MEDIUM': {'score': 15, 'color': '#ffc107'},
        'LOW': {'score': 5, 'color': '#28a745'}
    }
    
    # Service risk profiles with detailed information
    SERVICE_RISKS = {
        # HIGH RISK SERVICES
        'Telnet': {
            'risk': 'HIGH',
            'reason': 'Unencrypted protocol transmitting credentials in plaintext',
            'mitigation': 'Replace with SSH. Disable Telnet service immediately.'
        },
        'FTP': {
            'risk': 'HIGH',
            'reason': 'Unencrypted file transfer with plaintext authentication',
            'mitigation': 'Use SFTP or FTPS. Configure with strong authentication.'
        },
        'SMB': {
            'risk': 'HIGH',
            'reason': 'Vulnerable to ransomware and lateral movement attacks',
            'mitigation': 'Restrict access with firewall rules. Keep SMB version updated. Enable SMB signing.'
        },
        'RDP': {
            'risk': 'HIGH',
            'reason': 'Common target for brute-force attacks and exploitation',
            'mitigation': 'Use VPN for access. Enable Network Level Authentication. Implement MFA.'
        },
        'VNC': {
            'risk': 'HIGH',
            'reason': 'Often configured with weak passwords or no encryption',
            'mitigation': 'Use SSH tunneling. Implement strong authentication. Consider alternatives.'
        },
        'MySQL': {
            'risk': 'HIGH',
            'reason': 'Database exposed to internet increases attack surface',
            'mitigation': 'Bind to localhost only. Use firewall rules. Implement strong passwords.'
        },
        'PostgreSQL': {
            'risk': 'HIGH',
            'reason': 'Database service should not be publicly accessible',
            'mitigation': 'Restrict to internal network. Use pg_hba.conf properly. Enable SSL.'
        },
        
        # MEDIUM RISK SERVICES
        'HTTP': {
            'risk': 'MEDIUM',
            'reason': 'Unencrypted web traffic vulnerable to interception',
            'mitigation': 'Implement HTTPS with valid SSL/TLS certificates. Redirect HTTP to HTTPS.'
        },
        'HTTP-Proxy': {
            'risk': 'MEDIUM',
            'reason': 'Proxy service may allow unauthorized access',
            'mitigation': 'Implement authentication. Restrict access by IP whitelist.'
        },
        'HTTPS-Alt': {
            'risk': 'MEDIUM',
            'reason': 'Non-standard HTTPS port may be misconfigured',
            'mitigation': 'Ensure proper SSL/TLS configuration. Use standard ports when possible.'
        },
        'SMTP': {
            'risk': 'MEDIUM',
            'reason': 'Mail server can be abused for spam or relay attacks',
            'mitigation': 'Configure SPF, DKIM, DMARC. Disable open relay. Use authentication.'
        },
        'POP3': {
            'risk': 'MEDIUM',
            'reason': 'Unencrypted email retrieval protocol',
            'mitigation': 'Use POP3S (SSL/TLS). Consider IMAP with encryption instead.'
        },
        'IMAP': {
            'risk': 'MEDIUM',
            'reason': 'Email protocol without encryption',
            'mitigation': 'Use IMAPS (SSL/TLS). Enforce strong authentication.'
        },
        'DNS': {
            'risk': 'MEDIUM',
            'reason': 'DNS server may be vulnerable to amplification attacks',
            'mitigation': 'Restrict recursive queries. Implement rate limiting. Use DNSSEC.'
        },
        
        # LOW RISK SERVICES
        'HTTPS': {
            'risk': 'LOW',
            'reason': 'Encrypted web service (validate certificate and configuration)',
            'mitigation': 'Keep SSL/TLS updated. Use strong ciphers. Monitor certificate expiration.'
        },
        'SSH': {
            'risk': 'LOW',
            'reason': 'Secure but requires proper configuration',
            'mitigation': 'Disable password auth. Use key-based authentication. Change default port.'
        },
        'FTP-DATA': {
            'risk': 'LOW',
            'reason': 'FTP data channel (assess based on FTP configuration)',
            'mitigation': 'Secure if using FTPS. Otherwise follow FTP mitigation strategies.'
        },
        
        # UNKNOWN SERVICES (default to medium risk)
        'Unknown': {
            'risk': 'MEDIUM',
            'reason': 'Unidentified service requires investigation',
            'mitigation': 'Investigate service identity. Close if unnecessary. Ensure proper security.'
        }
    }
    
    def get_risk_profile(self, service: str) -> Dict:
        """
        Get risk profile for a service
        
        Args:
            service: Service name
            
        Returns:
            Dictionary with risk level, reason, and mitigation
        """
        # Return specific profile or default to Unknown
        return self.SERVICE_RISKS.get(service, self.SERVICE_RISKS['Unknown'])
    
    def assess_risks(self, open_ports: List[Dict]) -> List[Dict]:
        """
        Assess risks for all open ports
        
        Args:
            open_ports: List of dictionaries with port and service information
            
        Returns:
            List of dictionaries with port, service, risk level, and recommendations
        """
        risk_results = []
        
        for port_info in open_ports:
            port = port_info['port']
            service = port_info['service']
            
            # Get risk profile
            risk_profile = self.get_risk_profile(service)
            
            # Build result
            result = {
                'port': port,
                'service': service,
                'risk_level': risk_profile['risk'],
                'risk_color': self.RISK_LEVELS[risk_profile['risk']]['color'],
                'reason': risk_profile['reason'],
                'mitigation': risk_profile['mitigation']
            }
            
            risk_results.append(result)
            logger.info(f"Port {port} ({service}): {risk_profile['risk']} risk")
        
        return risk_results
    
    def calculate_security_score(self, risk_results: List[Dict]) -> int:
        """
        Calculate overall security score (0-100)
        Higher score = Better security
        
        Args:
            risk_results: List of risk assessment results
            
        Returns:
            Security score from 0 to 100
        """
        if not risk_results:
            # No open ports = perfect score
            return 100
        
        # Calculate total risk points
        total_risk = 0
        for result in risk_results:
            risk_level = result['risk_level']
            total_risk += self.RISK_LEVELS[risk_level]['score']
        
        # Convert to score (0-100 scale)
        # More open ports and higher risk = lower score
        # Formula: 100 - (total_risk_points)
        # Cap at 0 minimum
        security_score = max(0, 100 - total_risk)
        
        logger.info(f"Security Score Calculation: {len(risk_results)} ports, {total_risk} risk points = {security_score}/100")
        
        return security_score
    
    def get_security_rating(self, score: int) -> Dict:
        """
        Get security rating based on score
        
        Args:
            score: Security score (0-100)
            
        Returns:
            Dictionary with rating and description
        """
        if score >= 90:
            return {
                'rating': 'EXCELLENT',
                'description': 'Very secure configuration with minimal attack surface',
                'color': '#28a745'
            }
        elif score >= 70:
            return {
                'rating': 'GOOD',
                'description': 'Secure with minor improvements needed',
                'color': '#20c997'
            }
        elif score >= 50:
            return {
                'rating': 'FAIR',
                'description': 'Moderate security concerns require attention',
                'color': '#ffc107'
            }
        elif score >= 30:
            return {
                'rating': 'POOR',
                'description': 'Significant security vulnerabilities present',
                'color': '#fd7e14'
            }
        else:
            return {
                'rating': 'CRITICAL',
                'description': 'Severe security issues requiring immediate action',
                'color': '#dc3545'
            }
    
    def generate_executive_summary(self, risk_results: List[Dict], security_score: int) -> Dict:
        """
        Generate executive summary of the security assessment
        
        Args:
            risk_results: List of risk assessment results
            security_score: Overall security score
            
        Returns:
            Dictionary with summary statistics and recommendations
        """
        # Count risks by level
        high_count = sum(1 for r in risk_results if r['risk_level'] == 'HIGH')
        medium_count = sum(1 for r in risk_results if r['risk_level'] == 'MEDIUM')
        low_count = sum(1 for r in risk_results if r['risk_level'] == 'LOW')
        
        # Get security rating
        rating = self.get_security_rating(security_score)
        
        # Priority recommendations
        priority_actions = []
        if high_count > 0:
            priority_actions.append(f"Address {high_count} HIGH risk service(s) immediately")
        if medium_count > 0:
            priority_actions.append(f"Review {medium_count} MEDIUM risk service(s)")
        if not priority_actions:
            priority_actions.append("Continue monitoring and maintain security posture")
        
        return {
            'security_score': security_score,
            'rating': rating['rating'],
            'rating_description': rating['description'],
            'rating_color': rating['color'],
            'total_open_ports': len(risk_results),
            'high_risk_count': high_count,
            'medium_risk_count': medium_count,
            'low_risk_count': low_count,
            'priority_actions': priority_actions
        }
    
    def simulate_attack_scenarios(self, risk_results: List[Dict]) -> List[str]:
        """
        Simulate realistic attacker behavior based on detected open ports.
        Generates professional, security-focused descriptions of possible exploitation paths
        and attack scenarios based on detected vulnerabilities.
        
        Args:
            risk_results: List of risk assessment results with port, service, and risk level
            
        Returns:
            List of strings describing possible exploitation paths and attack scenarios
        """
        attack_scenarios = []
        
        if not risk_results:
            return ['No open ports detected. Current attack surface is minimal.']
        
        # Categorize ports by risk level
        high_risk_ports = [r for r in risk_results if r['risk_level'] == 'HIGH']
        medium_risk_ports = [r for r in risk_results if r['risk_level'] == 'MEDIUM']
        low_risk_ports = [r for r in risk_results if r['risk_level'] == 'LOW']
        
        # HIGH RISK SCENARIOS - Exploitation and Lateral Movement
        if high_risk_ports:
            high_services = ', '.join([f"{r['service']}({r['port']})" for r in high_risk_ports])
            
            if any(r['service'] in ['RDP', 'SSH', 'Telnet'] for r in high_risk_ports):
                attack_scenarios.append(
                    f"CRITICAL: Remote Access Exploitation - Detected remote access services "
                    f"({high_services}). Attackers could exploit weak credentials or protocol vulnerabilities "
                    f"to gain initial system access. Implement MFA, use VPN, and enforce strong password policies."
                )
            
            if any(r['service'] in ['SMB', 'FTP'] for r in high_risk_ports):
                attack_scenarios.append(
                    f"CRITICAL: Lateral Movement Vector - Detected file sharing/transfer protocols "
                    f"({high_services}). Successfully compromised systems could leverage these services "
                    f"to move laterally across the network and exfiltrate sensitive data."
                )
            
            if any(r['service'] in ['MySQL', 'PostgreSQL'] for r in high_risk_ports):
                attack_scenarios.append(
                    f"CRITICAL: Database Compromise - Exposed database services ({high_services}) "
                    f"are prime targets. Direct database access bypasses application security controls "
                    f"and could lead to complete data breach. Implement network segmentation immediately."
                )
            
            if any(r['service'] == 'Telnet' for r in high_risk_ports):
                attack_scenarios.append(
                    f"CRITICAL: Credential Interception - Telnet transmits all data including credentials "
                    f"in plaintext. Network-based attackers can intercept login credentials without any special tools. "
                    f"This service must be disabled and replaced with SSH."
                )
            
            if any(r['service'] == 'VNC' for r in high_risk_ports):
                attack_scenarios.append(
                    f"CRITICAL: Remote Desktop Hijacking - VNC services often have weak or default passwords. "
                    f"Attackers can gain interactive desktop access for reconnaissance, data theft, or deploying malware. "
                    f"Enforce encryption and multi-factor authentication."
                )
        
        # MEDIUM RISK SCENARIOS - Information Gathering and Misconfiguration
        if medium_risk_ports:
            medium_services = ', '.join([f"{r['service']}({r['port']})" for r in medium_risk_ports])
            
            if any(r['service'] in ['HTTP', 'HTTP-Proxy', 'HTTPS-Alt'] for r in medium_risk_ports):
                attack_scenarios.append(
                    f"HIGH: Web Service Exploitation - Detected web services ({medium_services}). "
                    f"These are common attack vectors for credential harvesting, session hijacking, or application exploits. "
                    f"Ensure all web services use HTTPS, apply security patches, and implement Web Application Firewalls."
                )
            
            if any(r['service'] in ['SMTP', 'POP3', 'IMAP'] for r in medium_risk_ports):
                attack_scenarios.append(
                    f"HIGH: Email Service Abuse - Detected email services ({medium_services}). "
                    f"Misconfigured mail servers can be exploited as open relays for spam, phishing campaigns, or credential attacks. "
                    f"Enforce authentication, disable unnecessary protocols, and implement email filtering."
                )
            
            if any(r['service'] == 'DNS' for r in medium_risk_ports):
                attack_scenarios.append(
                    f"HIGH: DNS Infrastructure Abuse - Exposed DNS services can be exploited for cache poisoning, "
                    f"DNS amplification attacks, or unauthorized zone transfers. Implement access controls, rate limiting, and DNSSEC."
                )
        
        # LOW RISK SCENARIOS - Monitoring and Defense Recommendations
        if low_risk_ports:
            low_services = ', '.join([f"{r['service']}({r['port']})" for r in low_risk_ports])
            
            attack_scenarios.append(
                f"RECOMMENDED: Maintain Vigilance - Detected low-risk services ({low_services}). "
                f"While these services have proper security controls, continuous monitoring is essential. "
                f"Keep systems patched, monitor logs for suspicious activity, and maintain security awareness."
            )
        
        # Overall attack surface summary
        if len(high_risk_ports) > 0:
            attack_scenarios.append(
                f"⚠️  ATTACK SURFACE SUMMARY: System has {len(high_risk_ports)} critical vulnerabilities. "
                f"This represents a HIGH risk of compromise. Prioritize immediate remediation of all HIGH risk services "
                f"to prevent unauthorized access and data breach."
            )
        elif len(medium_risk_ports) > 0:
            attack_scenarios.append(
                f"ATTACK SURFACE SUMMARY: System has {len(medium_risk_ports)} moderate vulnerabilities. "
                f"These should be addressed within your regular patch and hardening cycle. Implement layered defenses."
            )
        else:
            attack_scenarios.append(
                f"ATTACK SURFACE SUMMARY: System shows minimal attack surface with only low-risk services detected. "
                f"Maintain current security posture through regular monitoring and updates."
            )
        
        logger.info(f"Generated {len(attack_scenarios)} attack scenarios")
        return attack_scenarios



if __name__ == '__main__':
    # Test the risk engine
    logging.basicConfig(level=logging.INFO)
    engine = RiskEngine()
    
    print("Risk Engine Test")
    print("=" * 60)
    
    # Sample test data
    test_ports = [
        {'port': 22, 'service': 'SSH'},
        {'port': 23, 'service': 'Telnet'},
        {'port': 80, 'service': 'HTTP'},
        {'port': 443, 'service': 'HTTPS'},
        {'port': 3389, 'service': 'RDP'}
    ]
    
    # Assess risks
    results = engine.assess_risks(test_ports)
    
    # Calculate score
    score = engine.calculate_security_score(results)
    
    # Generate summary
    summary = engine.generate_executive_summary(results, score)
    
    print(f"\nSecurity Score: {score}/100")
    print(f"Rating: {summary['rating']}")
    print(f"\nRisk Breakdown:")
    print(f"  HIGH: {summary['high_risk_count']}")
    print(f"  MEDIUM: {summary['medium_risk_count']}")
    print(f"  LOW: {summary['low_risk_count']}")
