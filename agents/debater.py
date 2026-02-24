"""
Debater Agent - Represents a single debate participant
"""

import os
import re
from typing import List, Dict, Optional
from openai import OpenAI
from datetime import datetime


class Debater:
    """
    A debate participant that can conduct research and deliver speeches.
    """
    
    def __init__(
        self,
        alias: str,
        model: str,
        language: str,
        role: str,
        stance: str,
        topic: str,
        api_key: str,
        api_url: str = "https://openrouter.ai/api/v1",
        words_per_speech: int = 1000
    ):
        """
        Initialize a debater agent.
        
        Args:
            alias: Name of the debater (e.g., "Peter")
            model: LLM model name (e.g., "openai/gpt-4o")
            language: Language for responses (e.g., "English")
            role: Debater's role/perspective
            stance: Debater's position on the topic
            topic: The debate topic
            api_key: OpenRouter API key
            api_url: OpenRouter API URL
            words_per_speech: Target word count for speeches
        """
        self.alias = alias
        self.model = model
        self.language = language
        self.role = role
        self.stance = stance
        self.topic = topic
        self.words_per_speech = words_per_speech
        
        # Initialize OpenAI client for OpenRouter
        self.client = OpenAI(
            base_url=api_url,
            api_key=api_key,
        )
        
        # Create memory directory for this debater
        self.memory_dir = os.path.join("memory", alias.lower())
        os.makedirs(self.memory_dir, exist_ok=True)
        
    def conduct_research(self, round_num: int, previous_research: List[str] = None) -> str:
        """
        Conduct research on the debate topic.
        
        Args:
            round_num: Current research round number
            previous_research: Content from previous research rounds
            
        Returns:
            The research content
        """
        print(f"  {self.alias}: Conducting research round {round_num}...")
        
        # Build research prompt
        system_prompt = f"""You are {self.alias}, a knowledgeable research assistant. 
Your role: {self.role}
Your stance: {self.stance}
Language: {self.language}

Conduct thorough research on the debate topic. Your research should be:
1. Well-structured with clear sections
2. Based on established theories, historical precedents, and logical reasoning
3. Organized for easy reference during the debate
4. Human-readable with markdown formatting"""

        if round_num == 1:
            user_prompt = f"""Research Round 1: Foundation Building

Topic: {self.topic}

Please research and document:
1. **Key Concepts** - Define important terms and frameworks related to this topic
2. **Historical Context** - Similar situations from history and how they were addressed
3. **Current State** - Present situation regarding this issue
4. **Key Arguments for Your Stance** - Evidence and reasoning supporting {self.stance}
5. **Potential Counter-arguments** - What opponents might say and how to address them
6. **Expert Opinions** - Notable thinkers and their perspectives on this topic

Format your response in clear markdown with headers, bullet points, and organized sections."""
        else:
            previous_content = "\n\n".join(previous_research) if previous_research else "No previous research."
            user_prompt = f"""Research Round {round_num}: Deepening Understanding

Topic: {self.topic}

Previous Research Summary:
{previous_content}

Based on your previous research, please now focus on:
1. **Refining Your Arguments** - Strengthen key points with additional evidence and reasoning
2. **Case Studies** - Specific examples that illustrate your position
3. **Policy/Practical Solutions** - Concrete proposals aligned with {self.stance}
4. **Addressing Weaknesses** - Identify and shore up potential vulnerabilities in your position
5. **Rhetorical Strategies** - Effective ways to present your arguments persuasively
6. **Synthesis** - Connect different aspects of the research into a coherent framework

Format your response in clear markdown building upon but not repeating previous research."""

        # Call LLM for research
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                extra_headers={
                    "HTTP-Referer": os.getenv("YOUR_SITE_URL", ""),
                    "X-Title": os.getenv("YOUR_SITE_NAME", "Debate System")
                }
            )
            
            research_content = response.choices[0].message.content
            
            # Save research to file
            research_file = os.path.join(self.memory_dir, f"research_round_{round_num}.md")
            with open(research_file, 'w', encoding='utf-8') as f:
                f.write(f"# Research Round {round_num} - {self.alias}\n\n")
                f.write(f"**Topic:** {self.topic}\n\n")
                f.write(f"**Role:** {self.role}\n\n")
                f.write(f"**Stance:** {self.stance}\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(research_content)
            
            print(f"  {self.alias}: Research round {round_num} saved to {research_file}")
            return research_content
            
        except Exception as e:
            print(f"  ERROR: {self.alias} research round {round_num} failed: {e}")
            raise

    def deliver_speech(
        self,
        round_num: int,
        speaker_order: int,
        previous_speeches: List[str],
        research_content: List[str]
    ) -> str:
        """
        Deliver a speech in the debate.
        
        Args:
            round_num: Current debate round number
            speaker_order: Position in speaking order (1, 2, or 3)
            previous_speeches: Content of previous speeches in this round
            research_content: All research content from this debater
            
        Returns:
            The speech content
        """
        print(f"  {self.alias}: Preparing speech for Round {round_num}...")
        
        # Build speech prompt
        system_prompt = f"""You are {self.alias}, participating in a formal debate.
Your role: {self.role}
Your stance: {self.stance}
Language: {self.language}

You are a skilled debater who:
- Presents arguments clearly and persuasively
- Engages respectfully with opponents' points
- Uses evidence to support claims
- Maintains a professional, thoughtful tone
- Adapts arguments based on what others have said

Target speech length: Approximately {self.words_per_speech} words."""

        # Build context from previous speeches
        previous_speeches_text = ""
        if previous_speeches:
            previous_speeches_text = "\n\n---\n\n".join([
                f"Speech from opponent:\n{speech}" 
                for speech in previous_speeches
            ])
        
        # Build context from research
        research_text = "\n\n---\n\n".join([
            f"Your research (Round {i+1}):\n{content}"
            for i, content in enumerate(research_content)
        ])

        if speaker_order == 1:
            user_prompt = f"""Round {round_num}, Speaker 1 - Opening Statement

Topic: {self.topic}

You speak first in this round. Your task:

1. **Frame the Discussion** - Set the stage with your perspective
2. **Present Core Arguments** - Articulate your main points clearly
3. **Use Your Research** - Draw from the following research materials:

{research_text}

4. **Look Ahead** - Acknowledge potential counter-arguments proactively
5. **Call to Action** - What should we do or believe?

Requirements:
- Approximately {self.words_per_speech} words
- Professional, persuasive tone
- Well-structured with clear sections
- Grounded in your research

Format your response as a formal speech."""

        else:
            user_prompt = f"""Round {round_num}, Speaker {speaker_order} - Response

Topic: {self.topic}

Previous speeches in this round:

{previous_speeches_text}

Your research materials:

{research_text}

Your task:

1. **Acknowledge Previous Speakers** - Briefly summarize key points from opponents
2. **Address Their Arguments** - Respond to specific claims with counter-evidence
3. **Advance Your Position** - Strengthen your stance with additional arguments
4. **Find Common Ground** - Acknowledge valid points while distinguishing your view
5. **Strategic Positioning** - Set up for future rounds

Requirements:
- Approximately {self.words_per_speech} words
- Engage respectfully but critically with opponents
- Use evidence from your research
- Maintain professional tone

Format your response as a formal speech."""

        # Call LLM for speech
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=4000,
                extra_headers={
                    "HTTP-Referer": os.getenv("YOUR_SITE_URL", ""),
                    "X-Title": os.getenv("YOUR_SITE_NAME", "Debate System")
                }
            )
            
            speech_content = response.choices[0].message.content
            
            # Extract key points for summary
            key_points = self._extract_key_points(speech_content)
            
            # Save speech to file
            speeches_dir = os.path.join("speeches", f"round_{round_num}")
            os.makedirs(speeches_dir, exist_ok=True)
            
            speech_file = os.path.join(speeches_dir, f"speaker_{speaker_order}_{self.alias.lower()}.md")
            with open(speech_file, 'w', encoding='utf-8') as f:
                f.write(f"# Round {round_num}, Speaker {speaker_order} - {self.alias}\n\n")
                f.write(f"**Topic:** {self.topic}\n\n")
                f.write(f"**Role:** {self.role}\n\n")
                f.write(f"**Stance:** {self.stance}\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write("## Speech\n\n")
                f.write(speech_content)
                f.write("\n\n---\n\n")
                f.write("## Key Points Summary\n\n")
                for i, point in enumerate(key_points, 1):
                    f.write(f"{i}. {point}\n")
            
            print(f"  {self.alias}: Speech saved to {speech_file}")
            return speech_content
            
        except Exception as e:
            print(f"  ERROR: {self.alias} speech failed: {e}")
            raise

    def _extract_key_points(self, speech: str, max_points: int = 5) -> List[str]:
        """
        Extract key points from a speech for the summary.
        
        Args:
            speech: The speech content
            max_points: Maximum number of points to extract
            
        Returns:
            List of key point strings
        """
        # Simple extraction: look for bullet points, numbered lists, or key sentences
        points = []
        
        # Try to find bullet points or numbered items
        bullet_pattern = r'^[\s]*[-•*\d]+[.)]?\s*(.+)$'
        matches = re.findall(bullet_pattern, speech, re.MULTILINE)
        
        if matches:
            points = matches[:max_points]
        else:
            # Fall back to extracting sentences that look like main arguments
            sentences = speech.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                # Look for sentences with argumentative keywords
                if any(keyword in sentence.lower() for keyword in 
                       ['believe', 'argue', 'therefore', 'conclusion', 'key', 'important', 'crucial', 'essential']):
                    if len(sentence) > 20 and len(sentence) < 200:
                        points.append(sentence)
                        if len(points) >= max_points:
                            break
        
        # If still no points, take first few substantial sentences
        if not points:
            sentences = speech.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 30:
                    points.append(sentence)
                    if len(points) >= max_points:
                        break
        
        return points if points else ["Key point extraction failed"]

    def load_research(self) -> List[str]:
        """
        Load all research content from memory folder.
        
        Returns:
            List of research content strings
        """
        research_content = []
        
        if not os.path.exists(self.memory_dir):
            return research_content
        
        # Find all research files and sort by round number
        research_files = []
        for filename in os.listdir(self.memory_dir):
            if filename.startswith("research_round_") and filename.endswith(".md"):
                try:
                    round_num = int(filename.split("_")[-1].split(".")[0])
                    research_files.append((round_num, filename))
                except ValueError:
                    continue
        
        research_files.sort(key=lambda x: x[0])
        
        for _, filename in research_files:
            filepath = os.path.join(self.memory_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    research_content.append(content)
            except Exception as e:
                print(f"  Warning: Could not load {filename}: {e}")
        
        return research_content
