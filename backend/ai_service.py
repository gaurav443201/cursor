"""
VIT-ChainVote AI Service
Gemini AI integration for manifesto generation and election analysis
"""

import os
from typing import Dict, List
import google.generativeai as genai


class AIService:
    """
    Handles AI-powered features using Google Gemini
    """
    
    def __init__(self):
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_manifesto(self, candidate_name: str, department: str) -> str:
        """
        Generate a 2-sentence energetic manifesto for a candidate
        """
        prompt = f"""
        Generate a powerful, energetic 2-sentence election manifesto for {candidate_name}, 
        a candidate running for the {department} department representative position at VIT institute.
        
        The manifesto should be:
        - Exactly 2 sentences
        - Inspiring and action-oriented
        - Focused on student welfare and department improvement
        - Professional yet energetic
        - Unique and memorable
        
        Do not include any introductory text, just return the 2-sentence manifesto.
        """
        
        try:
            response = self.model.generate_content(prompt)
            manifesto = response.text.strip()
            
            # Ensure it's roughly 2 sentences
            sentences = manifesto.split('.')
            if len(sentences) > 3:
                manifesto = '. '.join(sentences[:2]) + '.'
            
            return manifesto
            
        except Exception as e:
            print(f"Error generating manifesto: {e}")
            return f"Committed to excellence in {department}. Together, we'll build a stronger future for our department!"
    
    def analyze_election_results(self, results: Dict[str, Dict]) -> str:
        """
        Generate AI-powered analysis of election results
        """
        # Prepare results summary for AI
        summary_text = "Election Results Summary:\n\n"
        
        total_votes = 0
        for dept, dept_results in results.items():
            summary_text += f"{dept} Department:\n"
            summary_text += f"  Winner: {dept_results['winner']['name']}\n"
            summary_text += f"  Votes: {dept_results['winner']['votes']}\n"
            summary_text += f"  Total Voters: {dept_results['total_votes']}\n"
            summary_text += f"  Margin: {dept_results.get('margin', 'N/A')}\n\n"
            total_votes += dept_results['total_votes']
        
        prompt = f"""
        Analyze the following VIT institute election results and provide a comprehensive audit summary.
        
        {summary_text}
        
        Provide:
        1. Overall voter turnout analysis
        2. Department-wise performance insights
        3. Margin of victory analysis (close races vs landslides)
        4. Key observations about voting patterns
        5. Brief congratulatory message for winners
        
        Keep the analysis professional, data-driven, and concise (maximum 250 words).
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating analysis: {e}")
            return f"Election completed successfully with {total_votes} total votes cast across all departments. Winners have been declared for each department."
    
    def verify_candidate_eligibility(self, candidate_name: str, department: str) -> Dict[str, any]:
        """
        AI-powered candidate name verification (basic validation)
        """
        prompt = f"""
        Verify if "{candidate_name}" is a valid, professional name for a student election candidate.
        
        Check for:
        - Appropriate length (not too short or too long)
        - No offensive content
        - Looks like a real name
        
        Respond with ONLY "VALID" or "INVALID" followed by a brief reason.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            is_valid = "VALID" in result.upper()
            
            return {
                "valid": is_valid,
                "reason": result
            }
            
        except Exception as e:
            print(f"Error verifying candidate: {e}")
            # Default to valid if AI fails
            return {
                "valid": True,
                "reason": "AI verification unavailable, proceeding with registration"
            }
