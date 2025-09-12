import argparse
import json
from prompt_logger import PromptLogger

def show_prompt_history(args):
    """Show prompt history"""
    logger = PromptLogger()
    
    if args.last:
        prompts = logger.get_last_n_prompts(args.last)
        print(f"\n=== Last {args.last} Prompts ===")
    else:
        prompts = logger.get_all_prompts()
        print(f"\n=== All Prompts ({len(prompts)} total) ===")
    
    for i, entry in enumerate(prompts, 1):
        print(f"\n{i}. {entry['timestamp']}")
        print(f"   Prompt: {entry['prompt']}")
        print(f"   Mode: {entry['mode']}")
        print(f"   Score: {entry['score']}")
        print(f"   File: {entry['spec_file']}")



def show_system_stats(args):
    """Show system statistics"""
    logger = PromptLogger()
    prompts = logger.get_all_prompts()
    
    if not prompts:
        print("No prompts logged yet.")
        return
    
    total = len(prompts)
    avg_score = sum(p['score'] for p in prompts) / total
    modes = {}
    for p in prompts:
        modes[p['mode']] = modes.get(p['mode'], 0) + 1
    
    print(f"\n=== System Statistics ===")
    print(f"Total Prompts: {total}")
    print(f"Average Score: {avg_score:.2f}")
    print(f"Mode Distribution: {modes}")
    print(f"Latest: {prompts[-1]['timestamp']}")

def main():
    parser = argparse.ArgumentParser(description="CLI tools for prompt-to-json system")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show prompt history')
    history_parser.add_argument('--last', type=int, help='Show last N prompts')
    

    
    # Stats command
    subparsers.add_parser('stats', help='Show system statistics')
    
    # Database command
    subparsers.add_parser('db', help='Show database information')
    
    # Score command
    score_parser = subparsers.add_parser('score', help='Quick score a prompt')
    score_parser.add_argument('prompt', help='Prompt to score')
    
    # Examples command
    subparsers.add_parser('examples', help='Show sample outputs')
    
    args = parser.parse_args()
    
    if args.command == 'history':
        show_prompt_history(args)
    elif args.command == 'stats':
        show_system_stats(args)
    elif args.command == 'db':
        show_database_info(args)
    elif args.command == 'score':
        quick_score_prompt(args)
    elif args.command == 'examples':
        show_examples(args)
    else:
        print("Available commands: history, stats, db, score, examples")

def show_examples(args):
    """Show sample outputs from files"""
    import subprocess
    import sys
    
    # Use main.py examples function
    try:
        result = subprocess.run([sys.executable, 'main.py', '--examples'], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Failed to show examples: {e}")

def quick_score_prompt(args):
    """Quick score a prompt using data_scorer"""
    from main_agent import MainAgent
    from data_scorer import DataScorer
    
    agent = MainAgent()
    scorer = DataScorer()
    
    print(f"Quick scoring: '{args.prompt}'")
    spec = agent.generate_spec(args.prompt)
    
    overall = scorer.calculate_overall_score(spec)
    print(f"Score: {overall:.1f}/100")

def show_database_info(args):
    """Show database information"""
    try:
        import subprocess
        result = subprocess.run(['python', 'db_query.py'], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Database query failed: {e}")

if __name__ == "__main__":
    main()