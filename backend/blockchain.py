"""
VIT-ChainVote Blockchain Core
Implements a secure blockchain with Proof-of-Work consensus mechanism
"""

import hashlib
import json
import time
from typing import List, Dict, Any


class Block:
    """
    Represents a single block in the blockchain
    Contains transaction data, timestamp, and cryptographic hash
    """
    
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Generate SHA-256 hash of block contents
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Proof-of-Work mining: Find nonce that produces hash with leading zeros
        """
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block to dictionary for JSON serialization
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    """
    Manages the complete blockchain ledger
    Handles block creation, mining, and validation
    """
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """
        Initialize blockchain with genesis block
        """
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data={"type": "genesis", "message": "VIT-ChainVote Genesis Block"},
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """
        Retrieve the most recent block in the chain
        """
        return self.chain[-1]
    
    def add_vote(self, voter_id_hash: str, candidate_id: str, 
                 department: str) -> Dict[str, Any]:
        """
        Add a new vote transaction to the blockchain
        Returns transaction details including hash
        """
        latest_block = self.get_latest_block()
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data={
                "type": "vote",
                "voter_id_hash": voter_id_hash,
                "candidate_id": candidate_id,
                "department": department
            },
            previous_hash=latest_block.hash
        )
        
        # Mine the block (Proof-of-Work)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        return {
            "transaction_hash": new_block.hash,
            "block_index": new_block.index,
            "timestamp": new_block.timestamp
        }
    
    def is_chain_valid(self) -> bool:
        """
        Verify blockchain integrity
        Checks hash linkage and Proof-of-Work for all blocks
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify hash calculation
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Verify Proof-of-Work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def get_votes_by_department(self, department: str) -> List[Dict[str, Any]]:
        """
        Extract all votes for a specific department
        """
        votes = []
        for block in self.chain[1:]:  # Skip genesis block
            if block.data.get("type") == "vote" and \
               block.data.get("department") == department:
                votes.append(block.data)
        return votes
    
    def get_all_votes(self) -> List[Dict[str, Any]]:
        """
        Extract all vote transactions from the blockchain
        """
        votes = []
        for block in self.chain[1:]:  # Skip genesis block
            if block.data.get("type") == "vote":
                votes.append(block.data)
        return votes
    
    def reset_to_genesis(self) -> None:
        """
        Wipe the blockchain and reset to genesis block
        CAUTION: This is a destructive operation
        """
        self.chain = []
        self.create_genesis_block()
    
    def get_chain_data(self) -> List[Dict[str, Any]]:
        """
        Get complete blockchain as list of dictionaries
        """
        return [block.to_dict() for block in self.chain]
    
    def get_chain_length(self) -> int:
        """
        Get total number of blocks in the chain
        """
        return len(self.chain)
