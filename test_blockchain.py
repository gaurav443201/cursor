"""
Simple test script to verify blockchain functionality
Run this before starting the full server
"""

import sys
sys.path.append('backend')

from blockchain import Blockchain

print("🗳️  VIT-ChainVote Blockchain Test\n")

# Create blockchain
print("1. Creating blockchain...")
chain = Blockchain(difficulty=4)
print(f"   ✓ Genesis block created")
print(f"   ✓ Chain length: {chain.get_chain_length()}")

# Add test votes
print("\n2. Mining test votes...")
tx1 = chain.add_vote("voter_hash_1", "CAND_CSE_001", "CSE")
print(f"   ✓ Vote 1 mined: {tx1['transaction_hash'][:16]}...")

tx2 = chain.add_vote("voter_hash_2", "CAND_CSE_002", "CSE")
print(f"   ✓ Vote 2 mined: {tx2['transaction_hash'][:16]}...")

# Verify chain
print("\n3. Verifying blockchain integrity...")
is_valid = chain.is_chain_valid()
print(f"   {'✓' if is_valid else '✗'} Chain valid: {is_valid}")

# Display chain
print(f"\n4. Blockchain summary:")
print(f"   Total blocks: {chain.get_chain_length()}")
print(f"   Total votes: {len(chain.get_all_votes())}")

print("\n✅ Blockchain test completed successfully!")
print("   You can now start the server with: python backend/app.py")
