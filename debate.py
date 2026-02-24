#!/usr/bin/env python3
"""
Multi-Agent Debate System - Main Orchestrator

This script orchestrates a debate between multiple AI agents.
Configuration is read from OBJECTIVE.md.
"""

import os
import sys
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

# Import our modules
from agents.debater import Debater
from utils.parser import ObjectiveParser


def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    
    required_vars = ['OPENROUTER_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print("ERROR: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nPlease create a .env file with your OpenRouter API credentials.")
        print("See .env.example for the required format.")
        sys.exit(1)
    
    return {
        'api_key': os.getenv('OPENROUTER_API_KEY'),
        'api_url': os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1'),
    }


def create_debaters(config: Dict[str, Any], env: Dict[str, str]) -> List[Debater]:
    """
    Create Debater instances from configuration.
    
    Args:
        config: Parsed configuration from OBJECTIVE.md
        env: Environment variables
        
    Returns:
        List of Debater instances
    """
    debaters = []
    topic = config['topic']
    params = config['parameters']
    
    print(f"\n🎭 Creating {len(config['debaters'])} debaters...")
    print(f"📋 Topic: {topic}\n")
    
    for debater_config in config['debaters']:
        alias = debater_config['alias']
        model = debater_config['model']
        language = debater_config['language'] or 'English'
        role = debater_config['role']
        stance = debater_config['stance']
        
        print(f"  🤖 {alias}")
        print(f"     Model: {model}")
        print(f"     Role: {role}")
        print(f"     Stance: {stance}")
        print()
        
        debater = Debater(
            alias=alias,
            model=model,
            language=language,
            role=role,
            stance=stance,
            topic=topic,
            api_key=env['api_key'],
            api_url=env['api_url'],
            words_per_speech=params.get('words_per_speech', 1000)
        )
        
        debaters.append(debater)
    
    return debaters


def conduct_research_phase(debaters: List[Debater], num_rounds: int):
    """
    Conduct the research phase where each debater gathers information.
    
    Args:
        debaters: List of Debater instances
        num_rounds: Number of research rounds
    """
    print(f"\n📚 RESEARCH PHASE ({num_rounds} rounds)\n")
    print("=" * 60)
    
    for round_num in range(1, num_rounds + 1):
        print(f"\n🔍 Research Round {round_num}/{num_rounds}")
        print("-" * 40)
        
        for debater in debaters:
            try:
                # Load previous research if available
                previous_research = []
                if round_num > 1:
                    previous_research = debater.load_research()
                
                debater.conduct_research(round_num, previous_research)
                
                # Small delay to avoid rate limits
                time.sleep(1)
                
            except Exception as e:
                print(f"  ERROR: Research failed for {debater.alias}: {e}")
                raise
    
    print("\n✅ Research phase completed!")
    print(f"   Research materials saved in memory/ folder")


def conduct_debate_phase(debaters: List[Debater], num_rounds: int):
    """
    Conduct the debate phase where debaters deliver speeches.
    
    Args:
        debaters: List of Debater instances
        num_rounds: Number of debate rounds
    """
    print(f"\n🗣️  DEBATE PHASE ({num_rounds} rounds)\n")
    print("=" * 60)
    
    # Load research for all debaters before debate starts
    print("\n📂 Loading research materials...")
    debater_research = {}
    for debater in debaters:
        research = debater.load_research()
        debater_research[debater.alias] = research
        print(f"  ✓ {debater.alias}: {len(research)} research document(s)")
    
    for round_num in range(1, num_rounds + 1):
        print(f"\n🎯 DEBATE ROUND {round_num}/{num_rounds}")
        print("-" * 60)
        
        # Rotate speaking order: Round 1: 0,1,2; Round 2: 1,2,0; Round 3: 2,0,1
        speaking_order = [(i + round_num - 1) % len(debaters) for i in range(len(debaters))]
        
        round_speeches = []  # Track speeches in this round
        
        for speaker_position, debater_index in enumerate(speaking_order, 1):
            debater = debaters[debater_index]
            
            try:
                # Get previous speeches in this round (excluding this debater's turn)
                previous_speeches = round_speeches.copy()
                
                # Get this debater's research
                research = debater_research[debater.alias]
                
                print(f"\n  🎤 Speaker {speaker_position}: {debater.alias}")
                
                speech = debater.deliver_speech(
                    round_num=round_num,
                    speaker_order=speaker_position,
                    previous_speeches=previous_speeches,
                    research_content=research
                )
                
                # Add to round speeches for subsequent speakers
                round_speeches.append(speech)
                
                # Delay between speeches
                if speaker_position < len(debaters):
                    print(f"  ⏳ Pausing before next speaker...")
                    time.sleep(2)
                
            except Exception as e:
                print(f"  ERROR: Speech failed for {debater.alias}: {e}")
                raise
        
        print(f"\n  ✅ Round {round_num} completed!")
        
        # Delay between rounds
        if round_num < num_rounds:
            print(f"\n  ⏳ Moving to next round...")
            time.sleep(3)
    
    print("\n✅ Debate phase completed!")
    print(f"   All speeches saved in speeches/ folder")


def print_summary(debaters: List[Debater], config: Dict[str, Any]):
    """Print a summary of the completed debate."""
    print("\n" + "=" * 60)
    print("📊 DEBATE SUMMARY")
    print("=" * 60)
    
    print(f"\n📋 Topic: {config['topic']}")
    print(f"\n🎭 Participants:")
    for debater in debaters:
        print(f"   • {debater.alias} ({debater.role})")
    
    print(f"\n📁 Output Files:")
    print(f"   • Research: memory/{{debater}}/research_round_{{n}}.md")
    print(f"   • Speeches: speeches/round_{{n}}/speaker_{{m}}_{{alias}}.md")
    
    print("\n✨ Debate completed successfully!")


def main():
    """Main entry point for the debate system."""
    print("=" * 60)
    print("🤖 Multi-Agent Debate System")
    print("=" * 60)
    
    # Load environment variables
    print("\n🔧 Loading configuration...")
    env = load_environment()
    print("  ✓ Environment loaded")
    
    # Parse OBJECTIVE.md
    parser = ObjectiveParser()
    try:
        config = parser.parse()
        print("  ✓ OBJECTIVE.md parsed")
    except FileNotFoundError as e:
        print(f"  ✗ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"  ✗ Error parsing OBJECTIVE.md: {e}")
        sys.exit(1)
    
    # Validate configuration
    if not config['debaters']:
        print("  ✗ No debaters found in OBJECTIVE.md")
        sys.exit(1)
    
    # Create debaters
    debaters = create_debaters(config, env)
    
    # Get parameters
    params = config['parameters']
    research_rounds = params.get('research_rounds', 2)
    debate_rounds = params.get('num_rounds', 3)
    
    try:
        # Research Phase
        conduct_research_phase(debaters, research_rounds)
        
        # Debate Phase
        conduct_debate_phase(debaters, debate_rounds)
        
        # Print Summary
        print_summary(debaters, config)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Debate interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Debate failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
