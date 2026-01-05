#!/usr/bin/env python3
"""
Git Repository Analysis and Monitoring Script
Analyzes git commits, contributors, and project metrics
"""

import subprocess
import json
import datetime
from collections import defaultdict
import os

class GitAnalyzer:
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path
        self.results = {
            'analysis_date': datetime.datetime.now().isoformat(),
            'commits': [],
            'contributors': {},
            'files_changed': {},
            'summary': {}
        }

    def run_git_command(self, command):
        """Execute git command and return output"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=self.repo_path,
                capture_output=True, 
                text=True
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except Exception as e:
            print(f"Error running command '{command}': {e}")
            return ""

    def analyze_commits(self, days=30):
        """Analyze commits from last N days"""
        since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Get commit information
        cmd = f'git log --since="{since_date}" --pretty=format:"%H|%an|%ae|%ad|%s" --date=iso'
        output = self.run_git_command(cmd)
        
        commits = []
        contributors = defaultdict(int)
        
        for line in output.split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    commit_hash, author, email, date, message = parts
                    commits.append({
                        'hash': commit_hash,
                        'author': author,
                        'email': email,
                        'date': date,
                        'message': message
                    })
                    contributors[author] += 1
        
        self.results['commits'] = commits
        self.results['contributors'] = dict(contributors)
        return commits

    def analyze_file_changes(self, days=30):
        """Analyze file changes and activity"""
        since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Get file change statistics
        cmd = f'git log --since="{since_date}" --name-only --pretty=format:"" | sort | uniq -c | sort -nr'
        output = self.run_git_command(cmd)
        
        files_changed = {}
        for line in output.split('\n'):
            if line.strip():
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    count, filename = parts
                    files_changed[filename] = int(count)
        
        self.results['files_changed'] = files_changed
        return files_changed

    def generate_summary(self):
        """Generate analysis summary"""
        total_commits = len(self.results['commits'])
        total_contributors = len(self.results['contributors'])
        total_files_changed = len(self.results['files_changed'])
        
        most_active_contributor = max(
            self.results['contributors'].items(), 
            key=lambda x: x[1]
        ) if self.results['contributors'] else ('None', 0)
        
        most_changed_file = max(
            self.results['files_changed'].items(),
            key=lambda x: x[1]
        ) if self.results['files_changed'] else ('None', 0)
        
        summary = {
            'total_commits': total_commits,
            'total_contributors': total_contributors,
            'total_files_changed': total_files_changed,
            'most_active_contributor': most_active_contributor[0],
            'most_active_contributor_commits': most_active_contributor[1],
            'most_changed_file': most_changed_file[0],
            'most_changed_file_count': most_changed_file[1],
            'avg_commits_per_contributor': round(total_commits / max(total_contributors, 1), 2)
        }
        
        self.results['summary'] = summary
        return summary

    def run_full_analysis(self, days=30):
        """Run complete analysis"""
        print(f"Analyzing repository: {self.repo_path}")
        print(f"Analysis period: last {days} days")
        print("-" * 50)
        
        # Check if we're in a git repository
        if not self.run_git_command('git rev-parse --git-dir'):
            print("Error: Not a git repository")
            return None
        
        self.analyze_commits(days)
        self.analyze_file_changes(days)
        summary = self.generate_summary()
        
        # Print summary
        print(f"Total commits: {summary['total_commits']}")
        print(f"Contributors: {summary['total_contributors']}")
        print(f"Files changed: {summary['total_files_changed']}")
        print(f"Most active contributor: {summary['most_active_contributor']} ({summary['most_active_contributor_commits']} commits)")
        print(f"Most changed file: {summary['most_changed_file']} ({summary['most_changed_file_count']} changes)")
        print(f"Average commits per contributor: {summary['avg_commits_per_contributor']}")
        
        return self.results

    def save_results(self, filename='git_analysis.json'):
        """Save analysis results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\nResults saved to: {filename}")

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze Git repository metrics')
    parser.add_argument('--repo', default='.', help='Repository path (default: current directory)')
    parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    parser.add_argument('--output', default='git_analysis.json', help='Output file name')
    
    args = parser.parse_args()
    
    analyzer = GitAnalyzer(args.repo)
    results = analyzer.run_full_analysis(args.days)
    
    if results:
        analyzer.save_results(args.output)
        return results
    else:
        return None

if __name__ == '__main__':
    main()