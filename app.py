"""
Adaptive Attack Surface Mapper - Flask Backend
Main application file with routes and API endpoints
"""

from flask import Flask, render_template, request, jsonify, send_file
from scanner import PortScanner
from risk_engine import RiskEngine
import logging
from datetime import datetime
from io import BytesIO
import json

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
port_scanner = PortScanner()
risk_engine = RiskEngine()


@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan():
    """
    API endpoint to scan an IP address and perform comprehensive security assessment
    
    Request JSON:
        {
            "ip": "192.168.1.1",
            "start_port": 1,           (optional, default: 1)
            "end_port": 1024           (optional, default: 1024)
        }
    
    Validation rules:
        - start_port >= 1
        - end_port <= 65535
        - start_port < end_port
    
    Response includes:
        - Scan results with port details and risk levels
        - Executive summary with ratings and priority actions
        - Security score (0-100)
        - Risk breakdown (HIGH/MEDIUM/LOW counts)
        - Port range information
    """
    try:
        # Get request data
        data = request.get_json()
        ip_address = data.get('ip', '').strip()
        
        # Validate IP address
        if not ip_address:
            return jsonify({
                'success': False,
                'error': 'IP address is required'
            }), 400
        
        # Basic IP validation
        parts = ip_address.split('.')
        if len(parts) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            return jsonify({
                'success': False,
                'error': 'Invalid IP address format'
            }), 400
        
        # Get port range parameters with defaults
        start_port = data.get('start_port', 1)
        end_port = data.get('end_port', 1024)
        
        # Validate port range parameters
        try:
            start_port = int(start_port)
            end_port = int(end_port)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'start_port and end_port must be valid integers'
            }), 400
        
        # Validate port range bounds
        if start_port < 1:
            return jsonify({
                'success': False,
                'error': 'start_port must be >= 1'
            }), 400
        
        if end_port > 65535:
            return jsonify({
                'success': False,
                'error': 'end_port must be <= 65535'
            }), 400
        
        if start_port >= end_port:
            return jsonify({
                'success': False,
                'error': f'start_port ({start_port}) must be less than end_port ({end_port})'
            }), 400
        
        logger.info(f"Starting scan for IP: {ip_address} (ports {start_port}-{end_port})")
        
        # Perform port scan (multithreaded) with specified port range
        open_ports = port_scanner.scan(ip_address, start_port, end_port)
        logger.info(f"Port scan completed. Found {len(open_ports)} open ports")
        
        # Perform risk assessment on all open ports
        risk_results = risk_engine.assess_risks(open_ports)
        logger.info(f"Risk assessment completed for {len(risk_results)} ports")
        
        # Calculate overall security score (0-100)
        security_score = risk_engine.calculate_security_score(risk_results)
        logger.info(f"Security score calculated: {security_score}/100")
        
        # Simulate realistic attack scenarios based on detected vulnerabilities
        try:
            attack_simulations = risk_engine.simulate_attack_scenarios(risk_results)
            logger.info(f"Attack scenario simulation completed: {len(attack_simulations)} scenarios generated")
        except Exception as simulation_error:
            logger.error(f"Error simulating attack scenarios: {str(simulation_error)}")
            # Fallback to empty scenarios if simulation fails
            attack_simulations = ['Unable to generate attack scenarios. Review risks manually.']
        
        # Generate executive summary with ratings and recommendations
        try:
            summary = risk_engine.generate_executive_summary(risk_results, security_score)
            logger.info(f"Executive summary generated: {summary['rating']} rating")
        except Exception as summary_error:
            logger.error(f"Error generating executive summary: {str(summary_error)}")
            # Fallback to minimal summary if generation fails
            summary = {
                'security_score': security_score,
                'rating': 'UNKNOWN',
                'rating_description': 'Unable to generate rating',
                'rating_color': '#808080',
                'total_open_ports': len(risk_results),
                'high_risk_count': sum(1 for r in risk_results if r['risk_level'] == 'HIGH'),
                'medium_risk_count': sum(1 for r in risk_results if r['risk_level'] == 'MEDIUM'),
                'low_risk_count': sum(1 for r in risk_results if r['risk_level'] == 'LOW'),
                'priority_actions': ['Error generating recommendations. Review results manually.']
            }
        
        # Prepare production-level response with comprehensive data
        total_ports_in_range = end_port - start_port + 1
        response = {
            'success': True,
            'ip': ip_address,
            
            # Scan metadata
            'scan_metadata': {
                'start_port': start_port,
                'end_port': end_port,
                'total_ports_scanned': total_ports_in_range,
                'open_ports_count': len(open_ports)
            },
            
            # Security assessment
            'security_score': security_score,
            'executive_summary': {
                'rating': summary['rating'],
                'rating_description': summary['rating_description'],
                'rating_color': summary['rating_color'],
                'high_risk_count': summary['high_risk_count'],
                'medium_risk_count': summary['medium_risk_count'],
                'low_risk_count': summary['low_risk_count'],
                'priority_actions': summary['priority_actions']
            },
            
            # Attack simulation and threat analysis
            'attack_simulation': attack_simulations,
            
            # Detailed results
            'scan_results': risk_results
        }
        
        logger.info(f"Scan completed for {ip_address} (ports {start_port}-{end_port}). "
                   f"Security score: {security_score}/100. Rating: {summary['rating']}")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error during scan: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Scan failed: {str(e)}'
        }), 500


@app.route('/export-report', methods=['POST'])
def export_report():
    """
    API endpoint to export scan results as a downloadable JSON report.
    
    Request JSON:
        Complete scan response data from the /scan endpoint
    
    Response:
        JSON file download containing comprehensive security assessment report
    """
    try:
        # Get the scan data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No scan data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['ip', 'security_score', 'executive_summary', 'scan_results']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Build comprehensive report
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'tool_name': 'Adaptive Attack Surface Mapper',
                'tool_version': '1.0',
                'report_type': 'Security Assessment Report'
            },
            
            'scan_information': {
                'target_ip': data.get('ip'),
                'port_range': {
                    'start': data.get('scan_metadata', {}).get('start_port', 1),
                    'end': data.get('scan_metadata', {}).get('end_port', 1024),
                    'total_ports_scanned': data.get('scan_metadata', {}).get('total_ports_scanned', 0)
                },
                'open_ports_found': data.get('scan_metadata', {}).get('open_ports_count', 0)
            },
            
            'security_assessment': {
                'security_score': data.get('security_score'),
                'score_scale': '0-100 (Higher is Better)',
                'rating': data.get('executive_summary', {}).get('rating'),
                'rating_description': data.get('executive_summary', {}).get('rating_description'),
                'risk_breakdown': {
                    'high_risk': data.get('executive_summary', {}).get('high_risk_count', 0),
                    'medium_risk': data.get('executive_summary', {}).get('medium_risk_count', 0),
                    'low_risk': data.get('executive_summary', {}).get('low_risk_count', 0)
                },
                'priority_actions': data.get('executive_summary', {}).get('priority_actions', [])
            },
            
            'threat_analysis': {
                'attack_scenarios': data.get('attack_simulation', []),
                'scenario_count': len(data.get('attack_simulation', []))
            },
            
            'detailed_findings': {
                'ports_and_services': data.get('scan_results', [])
            },
            
            'recommendations_summary': {
                'immediate_actions': [
                    'Review all HIGH risk services immediately',
                    'Implement network segmentation to isolate vulnerable services',
                    'Enable multi-factor authentication (MFA) on all remote access',
                    'Keep all systems and services patched and updated'
                ],
                'medium_term_actions': [
                    'Conduct a full security audit',
                    'Implement a Web Application Firewall (WAF)',
                    'Deploy intrusion detection/prevention systems (IDS/IPS)',
                    'Establish regular vulnerability scanning schedule'
                ],
                'long_term_strategy': [
                    'Develop comprehensive security hardening standards',
                    'Implement zero-trust network architecture',
                    'Establish security awareness training program',
                    'Create incident response and disaster recovery plans'
                ]
            },
            
            'report_footer': {
                'disclaimer': 'This report is for authorized security testing only. '
                             'Unauthorized network scanning is illegal.',
                'confidentiality': 'CONFIDENTIAL - Handle according to your organization\'s data policies',
                'validity': 'This report reflects system state at time of scan. '
                           'Changes to systems may affect validity of findings.'
            }
        }
        
        logger.info(f"Generating export report for {data.get('ip')}")
        
        # Convert report to JSON string
        report_json = json.dumps(report, indent=2)
        
        # Create BytesIO object for file download
        file_buffer = BytesIO(report_json.encode('utf-8'))
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"security_report_{data.get('ip')}_{timestamp}.json"
        
        logger.info(f"Report exported successfully: {filename}")
        
        # Return file as downloadable attachment
        return send_file(
            file_buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error exporting report: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Report export failed: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Adaptive Attack Surface Mapper")
    print("Professional Cybersecurity Tool")
    print("=" * 60)
    print("\nStarting Flask server on http://127.0.0.1:5000")
    print("\n⚠️  EDUCATIONAL USE ONLY")
    print("Only scan systems you own or have permission to test.\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
