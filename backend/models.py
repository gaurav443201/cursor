"""
VIT-ChainVote Data Models
In-memory storage for candidates, voters, and election state
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ElectionState(Enum):
    """
    Election lifecycle states
    """
    WAITING = "waiting"  # Preparation phase, voters in waiting room
    LIVE = "live"        # Active voting period
    CLOSED = "closed"    # Election ended, results available


@dataclass
class Candidate:
    """
    Candidate data model
    """
    id: str
    name: str
    department: str
    manifesto: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class CandidateRegistry:
    """
    Manages candidate registration and retrieval
    """
    
    def __init__(self):
        self.candidates: Dict[str, Candidate] = {}
        self._id_counter = 1
    
    def add_candidate(self, name: str, department: str, manifesto: str) -> Candidate:
        """
        Register a new candidate
        """
        candidate_id = f"CAND_{department}_{self._id_counter:03d}"
        self._id_counter += 1
        
        candidate = Candidate(
            id=candidate_id,
            name=name,
            department=department.upper(),
            manifesto=manifesto
        )
        
        self.candidates[candidate_id] = candidate
        return candidate
    
    def remove_candidate(self, candidate_id: str) -> bool:
        """
        Remove a candidate from registry
        """
        if candidate_id in self.candidates:
            del self.candidates[candidate_id]
            return True
        return False
    
    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """
        Retrieve candidate by ID
        """
        return self.candidates.get(candidate_id)
    
    def get_candidates_by_department(self, department: str) -> List[Candidate]:
        """
        Get all candidates for a specific department
        """
        return [
            candidate for candidate in self.candidates.values()
            if candidate.department == department.upper()
        ]
    
    def get_all_candidates(self) -> List[Candidate]:
        """
        Get all registered candidates
        """
        return list(self.candidates.values())
    
    def clear(self) -> None:
        """
        Clear all candidates (used during election reset)
        """
        self.candidates = {}
        self._id_counter = 1


class VoterBlacklist:
    """
    Tracks voters who have already cast their vote
    Uses hashed emails for privacy
    """
    
    def __init__(self):
        self.voted_hashes: Set[str] = set()
    
    def has_voted(self, voter_hash: str) -> bool:
        """
        Check if voter has already voted
        """
        return voter_hash in self.voted_hashes
    
    def mark_as_voted(self, voter_hash: str) -> None:
        """
        Add voter to blacklist after voting
        """
        self.voted_hashes.add(voter_hash)
    
    def clear(self) -> None:
        """
        Clear blacklist (used during election reset)
        """
        self.voted_hashes = set()
    
    def get_voter_count(self) -> int:
        """
        Get total number of voters who have voted
        """
        return len(self.voted_hashes)


class ElectionManager:
    """
    Manages election state and lifecycle
    """
    
    def __init__(self):
        self.state = ElectionState.WAITING
        self.results: Optional[Dict] = None
    
    def start_election(self) -> bool:
        """
        Transition from WAITING to LIVE
        """
        if self.state == ElectionState.WAITING:
            self.state = ElectionState.LIVE
            return True
        return False
    
    def stop_election(self) -> bool:
        """
        Transition from LIVE to CLOSED
        """
        if self.state == ElectionState.LIVE:
            self.state = ElectionState.CLOSED
            return True
        return False
    
    def reset_election(self) -> None:
        """
        Reset to WAITING state
        """
        self.state = ElectionState.WAITING
        self.results = None
    
    def is_voting_open(self) -> bool:
        """
        Check if voting is currently allowed
        """
        return self.state == ElectionState.LIVE
    
    def get_state(self) -> str:
        """
        Get current election state as string
        """
        return self.state.value
    
    def set_results(self, results: Dict) -> None:
        """
        Store election results
        """
        self.results = results
    
    def get_results(self) -> Optional[Dict]:
        """
        Retrieve election results
        """
        return self.results
