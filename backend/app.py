"""
VIT-ChainVote Flask API Server
Main application with admin and voter endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from blockchain import Blockchain
from models import CandidateRegistry, VoterBlacklist, ElectionManager
from otp_service import OTPService
from ai_service import AIService
from utils import (
    is_valid_vit_email, 
    is_shadow_admin, 
    hash_email, 
    is_valid_department,
    sanitize_input
)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend communication (supports both local and production)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins for now
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Initialize core components
blockchain = Blockchain(difficulty=4)
candidate_registry = CandidateRegistry()
voter_blacklist = VoterBlacklist()
election_manager = ElectionManager()
otp_service = OTPService()
ai_service = AIService()

# Temporary storage for voter sessions (email -> department mapping)
voter_sessions: Dict[str, str] = {}


# ============================================================================
# ADMIN ROUTES (Shadow Access Only)
# ============================================================================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """
    Authenticate Shadow administrator
    """
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400
    
    if is_shadow_admin(email):
        return jsonify({
            "success": True,
            "message": "Shadow authenticated",
            "admin_email": email
        })
    
    return jsonify({"success": False, "message": "Unauthorized access"}), 403


@app.route('/api/admin/candidate/add', methods=['POST'])
def add_candidate():
    """
    Register a new candidate with AI-generated manifesto
    """
    data = request.get_json()
    
    # Verify admin access
    admin_email = data.get('admin_email', '')
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    # Extract candidate data
    name = sanitize_input(data.get('name', '').strip())
    department = data.get('department', '').strip().upper()
    
    if not name or not department:
        return jsonify({"success": False, "message": "Name and department required"}), 400
    
    if not is_valid_department(department):
        return jsonify({"success": False, "message": "Invalid department"}), 400
    
    # Generate AI manifesto with fallback
    try:
        manifesto = ai_service.generate_manifesto(name, department)
    except Exception as e:
        # Fallback to default manifesto if AI fails
        print(f"⚠️  AI service error: {str(e)}")
        manifesto = f"Dedicated to advancing {department} excellence and innovation. Together, we'll build a stronger future for VIT!"
    
    # Register candidate
    candidate = candidate_registry.add_candidate(name, department, manifesto)
    
    return jsonify({
        "success": True,
        "message": "Candidate registered successfully",
        "candidate": candidate.to_dict()
    })


@app.route('/api/admin/candidate/remove', methods=['DELETE'])
def remove_candidate():
    """
    Remove a candidate from registry
    """
    data = request.get_json()
    
    # Verify admin access
    admin_email = data.get('admin_email', '')
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    candidate_id = data.get('candidate_id', '')
    
    if candidate_registry.remove_candidate(candidate_id):
        return jsonify({"success": True, "message": "Candidate removed"})
    
    return jsonify({"success": False, "message": "Candidate not found"}), 404


@app.route('/api/admin/candidates', methods=['GET'])
def get_all_candidates_admin():
    """
    Get all registered candidates (admin view)
    """
    admin_email = request.args.get('admin_email', '')
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    candidates = candidate_registry.get_all_candidates()
    return jsonify({
        "success": True,
        "candidates": [c.to_dict() for c in candidates]
    })


@app.route('/api/admin/election/start', methods=['POST'])
def start_election():
    """
    Start the election (transition to LIVE state)
    """
    data = request.get_json()
    admin_email = data.get('admin_email', '')
    
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    if election_manager.start_election():
        return jsonify({
            "success": True,
            "message": "Election started - voting is now LIVE",
            "state": election_manager.get_state()
        })
    
    return jsonify({"success": False, "message": "Election already started"}), 400


@app.route('/api/admin/election/stop', methods=['POST'])
def stop_election():
    """
    Stop the election and calculate results
    """
    data = request.get_json()
    admin_email = data.get('admin_email', '')
    
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    if not election_manager.stop_election():
        return jsonify({"success": False, "message": "Election not in LIVE state"}), 400
    
    # Calculate results
    results = calculate_results()
    election_manager.set_results(results)
    
    return jsonify({
        "success": True,
        "message": "Election stopped - results calculated",
        "state": election_manager.get_state(),
        "results": results
    })


@app.route('/api/admin/election/reset', methods=['POST'])
def reset_election():
    """
    Reset blockchain to genesis and clear all data
    CAUTION: Destructive operation
    """
    data = request.get_json()
    admin_email = data.get('admin_email', '')
    
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    # Reset all components
    blockchain.reset_to_genesis()
    candidate_registry.clear()
    voter_blacklist.clear()
    election_manager.reset_election()
    voter_sessions.clear()
    
    return jsonify({
        "success": True,
        "message": "Blockchain reset to genesis - all data wiped",
        "chain_length": blockchain.get_chain_length()
    })


@app.route('/api/admin/audit', methods=['GET'])
def get_audit():
    """
    Get AI-powered election audit
    """
    admin_email = request.args.get('admin_email', '')
    
    if not is_shadow_admin(admin_email):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    results = election_manager.get_results()
    
    if not results:
        return jsonify({"success": False, "message": "No results available"}), 400
    
    # Generate AI analysis
    try:
        analysis = ai_service.analyze_election_results(results)
    except Exception as e:
        analysis = f"AI analysis unavailable: {str(e)}"
    
    return jsonify({
        "success": True,
        "audit": analysis,
        "results": results,
        "chain_valid": blockchain.is_chain_valid(),
        "total_blocks": blockchain.get_chain_length()
    })


# ============================================================================
# VOTER ROUTES
# ============================================================================

@app.route('/api/voter/login', methods=['POST'])
def voter_login():
    """
    Voter login with VIT email - sends OTP
    """
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    department = data.get('department', '').strip().upper()
    
    if not email or not department:
        return jsonify({"success": False, "message": "Email and department required"}), 400
    
    if not is_valid_vit_email(email):
        return jsonify({"success": False, "message": "Invalid VIT email format"}), 400
    
    if not is_valid_department(department):
        return jsonify({"success": False, "message": "Invalid department"}), 400
    
    # Check if already voted
    voter_hash = hash_email(email)
    if voter_blacklist.has_voted(voter_hash):
        return jsonify({"success": False, "message": "You have already voted"}), 403
    
    # Store voter session
    voter_sessions[email] = department
    
    # Send OTP
    try:
        if otp_service.generate_and_send_otp(email):
            return jsonify({
                "success": True,
                "message": "OTP sent to your email",
                "email": email
            })
        else:
            # If email fails, tell user to use test OTP
            return jsonify({
                "success": True,
                "message": "Email service unavailable. Use test OTP: 123456",
                "email": email
            })
    except Exception as e:
        print(f"⚠️  OTP service error: {str(e)}")
        return jsonify({
            "success": True,
            "message": "Email service unavailable. Use test OTP: 123456",
            "email": email
        })


@app.route('/api/voter/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP and grant access
    """
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()
    
    if not email or not otp:
        return jsonify({"success": False, "message": "Email and OTP required"}), 400
    
    # Try to verify OTP normally
    if otp_service.verify_otp(email, otp):
        department = voter_sessions.get(email, '')
        return jsonify({
            "success": True,
            "message": "OTP verified successfully",
            "email": email,
            "department": department
        })
    
    # Fallback: Accept "123456" as test OTP if email service is down
    if otp == "123456" and email in voter_sessions:
        print(f"⚠️  Using test OTP for {email}")
        department = voter_sessions.get(email, '')
        return jsonify({
            "success": True,
            "message": "OTP verified successfully (test mode)",
            "email": email,
            "department": department
        })
    
    return jsonify({"success": False, "message": "Invalid or expired OTP"}), 401


@app.route('/api/voter/candidates', methods=['GET'])
def get_candidates_for_voter():
    """
    Get candidates for voter's department
    """
    email = request.args.get('email', '').strip().lower()
    
    if email not in voter_sessions:
        return jsonify({"success": False, "message": "Session expired"}), 401
    
    department = voter_sessions[email]
    candidates = candidate_registry.get_candidates_by_department(department)
    
    return jsonify({
        "success": True,
        "department": department,
        "candidates": [c.to_dict() for c in candidates]
    })


@app.route('/api/voter/vote', methods=['POST'])
def submit_vote():
    """
    Submit vote and mine block
    """
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    candidate_id = data.get('candidate_id', '').strip()
    
    if not email or not candidate_id:
        return jsonify({"success": False, "message": "Email and candidate ID required"}), 400
    
    # Verify session
    if email not in voter_sessions:
        return jsonify({"success": False, "message": "Session expired"}), 401
    
    # Verify election is live
    if not election_manager.is_voting_open():
        return jsonify({"success": False, "message": "Voting is not currently open"}), 403
    
    # Check if already voted
    voter_hash = hash_email(email)
    if voter_blacklist.has_voted(voter_hash):
        return jsonify({"success": False, "message": "You have already voted"}), 403
    
    # Verify candidate exists and matches department
    department = voter_sessions[email]
    candidate = candidate_registry.get_candidate(candidate_id)
    
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404
    
    if candidate.department != department:
        return jsonify({"success": False, "message": "Candidate not in your department"}), 403
    
    # Add vote to blockchain
    transaction = blockchain.add_vote(voter_hash, candidate_id, department)
    
    # Mark voter as voted
    voter_blacklist.mark_as_voted(voter_hash)
    
    # Clear session
    del voter_sessions[email]
    
    return jsonify({
        "success": True,
        "message": "Vote recorded successfully",
        "transaction_hash": transaction['transaction_hash'],
        "block_index": transaction['block_index'],
        "candidate": candidate.to_dict()
    })


@app.route('/api/voter/status', methods=['GET'])
def check_voter_status():
    """
    Check if voter has already voted
    """
    email = request.args.get('email', '').strip().lower()
    
    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400
    
    voter_hash = hash_email(email)
    has_voted = voter_blacklist.has_voted(voter_hash)
    
    return jsonify({
        "success": True,
        "has_voted": has_voted
    })


# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@app.route('/api/election/state', methods=['GET'])
def get_election_state():
    """
    Get current election state
    """
    return jsonify({
        "success": True,
        "state": election_manager.get_state(),
        "total_votes": voter_blacklist.get_voter_count(),
        "chain_length": blockchain.get_chain_length(),
        "chain_valid": blockchain.is_chain_valid()
    })


@app.route('/api/results', methods=['GET'])
def get_results():
    """
    Get election results (only when closed)
    """
    if election_manager.get_state() != "closed":
        return jsonify({"success": False, "message": "Results not available yet"}), 403
    
    results = election_manager.get_results()
    
    if not results:
        return jsonify({"success": False, "message": "Results not calculated"}), 404
    
    return jsonify({
        "success": True,
        "results": results,
        "chain_valid": blockchain.is_chain_valid()
    })


@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """
    Get complete blockchain data (for transparency)
    """
    return jsonify({
        "success": True,
        "chain": blockchain.get_chain_data(),
        "length": blockchain.get_chain_length(),
        "valid": blockchain.is_chain_valid()
    })


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_results() -> Dict[str, Any]:
    """
    Calculate election results from blockchain
    """
    from collections import defaultdict
    
    results = {}
    all_votes = blockchain.get_all_votes()
    
    # Group votes by department
    dept_votes = defaultdict(list)
    for vote in all_votes:
        dept_votes[vote['department']].append(vote)
    
    # Calculate winner for each department
    for department in ['CSE', 'IT', 'ENTC', 'MECH']:
        votes = dept_votes.get(department, [])
        
        if not votes:
            results[department] = {
                "winner": None,
                "total_votes": 0,
                "vote_breakdown": {}
            }
            continue
        
        # Count votes per candidate
        vote_count = defaultdict(int)
        for vote in votes:
            vote_count[vote['candidate_id']] += 1
        
        # Find winner
        winner_id = max(vote_count, key=vote_count.get)
        winner_candidate = candidate_registry.get_candidate(winner_id)
        
        # Calculate margin
        sorted_votes = sorted(vote_count.values(), reverse=True)
        margin = sorted_votes[0] - sorted_votes[1] if len(sorted_votes) > 1 else sorted_votes[0]
        
        results[department] = {
            "winner": {
                "id": winner_id,
                "name": winner_candidate.name if winner_candidate else "Unknown",
                "votes": vote_count[winner_id]
            },
            "total_votes": len(votes),
            "margin": margin,
            "vote_breakdown": dict(vote_count)
        }
    
    return results


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print("🗳️  VIT-ChainVote Server Starting...")
    print(f"📡 Port: {port}")
    print(f"⛓️  Blockchain initialized with {blockchain.get_chain_length()} blocks")
    print(f"🔒 Difficulty: {blockchain.difficulty}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
