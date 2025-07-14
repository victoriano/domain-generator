#!/usr/bin/env python3

import random
import socket
import itertools
import time
import urllib.parse
import subprocess
import re
from typing import List, Set

class DomainGenerator:
    def __init__(self):
        self.base_words = {
            'data': ['data', 'analytics', 'insight', 'metrics', 'stats', 'info', 'intelligence',
                    'knowledge', 'facts', 'records', 'database', 'warehouse', 'mart', 'lake',
                    'stream', 'flow', 'pipeline', 'etl', 'transform', 'process', 'analyze',
                    'compute', 'calculate', 'measure', 'track', 'monitor', 'observe', 'report',
                    'dashboard', 'visual', 'chart', 'graph', 'trend', 'pattern', 'model',
                    'algorithm', 'machine', 'learning', 'ai', 'neural', 'deep', 'smart',
                    'intelligent', 'automated', 'digital', 'tech', 'cloud', 'big', 'fast',
                    'real', 'time', 'instant', 'quick', 'rapid', 'speed', 'agile', 'lean',
                    'efficient', 'optimal', 'max', 'super', 'ultra', 'mega', 'pro', 'plus',
                    'hub', 'lab', 'works', 'studio', 'forge', 'craft', 'build', 'make',
                    'create', 'generate', 'produce', 'deliver', 'serve', 'provide', 'offer',
                    'solution', 'platform', 'system', 'framework', 'engine', 'core', 'base',
                    'foundation', 'structure', 'architecture', 'design', 'plan', 'strategy'],
            'tech': ['tech', 'technology', 'digital', 'software', 'code', 'dev', 'developer',
                    'programming', 'app', 'application', 'web', 'mobile', 'cloud', 'saas',
                    'api', 'system', 'platform', 'framework', 'tool', 'service', 'solution',
                    'innovation', 'startup', 'venture', 'product', 'build', 'create', 'develop'],
            'business': ['business', 'company', 'corp', 'enterprise', 'venture', 'startup',
                        'solutions', 'services', 'consulting', 'strategy', 'growth', 'success',
                        'profit', 'revenue', 'sales', 'market', 'brand', 'professional', 'expert',
                        'leader', 'management', 'executive', 'global', 'international', 'premium'],
            'health': ['health', 'medical', 'healthcare', 'wellness', 'fitness', 'care', 'clinic',
                      'hospital', 'doctor', 'patient', 'treatment', 'therapy', 'medicine', 'pharma',
                      'biotech', 'life', 'living', 'healthy', 'vital', 'strong', 'active', 'energy'],
            'finance': ['finance', 'financial', 'money', 'invest', 'investment', 'capital', 'fund',
                       'wealth', 'rich', 'profit', 'revenue', 'banking', 'credit', 'loan', 'payment',
                       'crypto', 'blockchain', 'trading', 'market', 'stock', 'portfolio', 'asset'],
            'education': ['education', 'learning', 'school', 'university', 'college', 'course',
                         'training', 'teach', 'student', 'knowledge', 'skill', 'academy', 'institute',
                         'study', 'research', 'science', 'academic', 'scholar', 'expert', 'master'],
            'creative': ['creative', 'design', 'art', 'artist', 'studio', 'agency', 'media',
                        'content', 'brand', 'marketing', 'advertising', 'visual', 'graphic',
                        'digital', 'web', 'ui', 'ux', 'experience', 'innovative', 'original']
        }
        self.custom_words = []
        
        self.connectors = ['', 'and', 'for', 'the', 'of', 'in', 'on', 'at', 'by', 'with']
        self.suffixes = ['ly', 'hub', 'lab', 'pro', 'max', 'ai', 'io', 'app', 'sys', 'net']
        
    def set_custom_words(self, words_input: str):
        self.custom_words = [word.strip().lower() for word in words_input.split(',') if word.strip()]
    
    def get_word_list(self, categories: List[str]) -> List[str]:
        all_words = []
        for category in categories:
            if category in self.base_words:
                all_words.extend(self.base_words[category])
        
        if self.custom_words:
            all_words.extend(self.custom_words)
        
        return list(set(all_words))
    
    def generate_combinations(self, categories: List[str], num_words: int, include_numbers: bool = False) -> List[str]:
        word_list = self.get_word_list(categories)
        domains = set()
        
        # Two-word combinations
        if num_words >= 2:
            for word1, word2 in itertools.combinations(word_list, 2):
                domains.add(f"{word1}{word2}")
                
        # Three-word combinations with connectors
        if num_words >= 3:
            sample_words = random.sample(word_list, min(20, len(word_list)))
            for word1, connector, word2 in itertools.product(
                sample_words, self.connectors[:3], sample_words
            ):
                if word1 != word2:
                    if connector:
                        domains.add(f"{word1}{connector}{word2}")
                    else:
                        domains.add(f"{word1}{word2}")
        
        # Add suffixes
        base_words = random.sample(word_list, min(10, len(word_list)))
        for word in base_words:
            for suffix in self.suffixes:
                domains.add(f"{word}{suffix}")
        
        # Add numbers if requested
        if include_numbers:
            for word in random.sample(word_list, min(15, len(word_list))):
                for num in [1, 2, 3, 24, 7, 360, 100, 200, 500, 1000]:
                    domains.add(f"{word}{num}")
                    domains.add(f"{num}{word}")
        
        return list(domains)
    
    def check_domain_availability(self, domain: str) -> bool:
        try:
            socket.gethostbyname(f"{domain}.com")
            return False  # Domain exists
        except socket.gaierror:
            return True   # Domain might be available
    
    def whois_check(self, domain: str) -> bool:
        """Check domain availability using WHOIS. Returns True if available."""
        try:
            result = subprocess.run(
                ['whois', f"{domain}.com"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return True  # Likely available if whois fails
            
            whois_output = result.stdout.lower()
            
            # Check for common "not found" or "available" indicators
            not_found_patterns = [
                'no match',
                'not found',
                'no entries found',
                'no data found',
                'domain not found',
                'no matching record',
                'available for registration'
            ]
            
            for pattern in not_found_patterns:
                if pattern in whois_output:
                    return True  # Domain appears to be available
            
            # Check for registration indicators
            registered_patterns = [
                'creation date',
                'created',
                'registrar',
                'expiration date',
                'expires',
                'name server',
                'nameserver'
            ]
            
            for pattern in registered_patterns:
                if pattern in whois_output:
                    return False  # Domain is registered
            
            return True  # Default to available if unclear
            
        except subprocess.TimeoutExpired:
            return None  # Timeout - unclear status
        except Exception:
            return None  # Error - unclear status
    
    def batch_check_domains(self, domains: List[str], show_progress: bool = True) -> List[dict]:
        results = []
        total = len(domains)
        
        # Stage 1: DNS checking
        dns_available = []
        for i, domain in enumerate(domains):
            if show_progress:
                print(f"\rDNS check... {i+1}/{total} ({(i+1)/total*100:.1f}%)", end='', flush=True)
            
            is_dns_available = self.check_domain_availability(domain)
            godaddy_url = f"https://www.godaddy.com/domainsearch/find?domainToCheck={domain}.com"
            
            result = {
                'domain': domain,
                'dns_available': is_dns_available,
                'whois_available': None,
                'available': is_dns_available,
                'full_domain': f"{domain}.com",
                'godaddy_url': godaddy_url,
                'verification_method': 'DNS only'
            }
            
            results.append(result)
            
            if is_dns_available:
                dns_available.append(result)
            
            time.sleep(0.1)
        
        if show_progress:
            print("\n")
        
        # Stage 2: WHOIS verification for DNS-available domains
        if dns_available:
            if show_progress:
                print(f"\nVerifying {len(dns_available)} potentially available domains with WHOIS...")
            
            for i, result in enumerate(dns_available):
                if show_progress:
                    print(f"\rWHOIS check... {i+1}/{len(dns_available)} ({(i+1)/len(dns_available)*100:.1f}%)", end='', flush=True)
                
                whois_result = self.whois_check(result['domain'])
                result['whois_available'] = whois_result
                
                if whois_result is not None:
                    result['available'] = whois_result
                    result['verification_method'] = 'DNS + WHOIS'
                else:
                    result['verification_method'] = 'DNS + WHOIS (timeout)'
                
                time.sleep(0.5)  # Longer delay for WHOIS to be respectful
            
            if show_progress:
                print("\n")
        
        return results

def main():
    generator = DomainGenerator()
    
    print("🌐 Custom Domain Name Generator")
    print("=" * 40)
    
    # Get user preferences for word types
    print("\n📝 Tell us about your business/project:")
    print("What type of words should compose your domain names?")
    print("(e.g., 'technology and innovation', 'health and wellness', 'finance and investment')")
    
    user_description = input("\n💬 Describe your domain theme: ").strip()
    
    # Show available categories
    print("\n📦 Available word categories:")
    categories = list(generator.base_words.keys())
    for i, category in enumerate(categories, 1):
        print(f"  {i}. {category.title()}")
    
    # Get category selection
    category_input = input("\n🎯 Select categories (numbers separated by commas, e.g., 1,2,3): ").strip()
    selected_categories = []
    
    if category_input:
        try:
            category_nums = [int(x.strip()) for x in category_input.split(',')]
            selected_categories = [categories[i-1] for i in category_nums if 1 <= i <= len(categories)]
        except ValueError:
            selected_categories = ['tech', 'business']  # Default fallback
    
    if not selected_categories:
        selected_categories = ['tech', 'business']  # Default fallback
    
    # Get custom words
    custom_words = input("\n🔤 Add custom words (comma-separated, optional): ").strip()
    if custom_words:
        generator.set_custom_words(custom_words)
    
    print(f"\n🎨 Selected categories: {', '.join(selected_categories)}")
    if generator.custom_words:
        print(f"🔤 Custom words: {', '.join(generator.custom_words)}")
    
    # Get other preferences
    print("\n📋 Generation settings:")
    
    try:
        max_words = int(input("Maximum number of words per domain (2-3): ") or "2")
        max_words = max(2, min(3, max_words))
    except ValueError:
        max_words = 2
    
    include_numbers = input("Include numbers in domain names? (y/n): ").lower().startswith('y')
    
    try:
        max_domains = int(input("Maximum domains to generate (default 50): ") or "50")
        max_domains = max(10, min(500, max_domains))
    except ValueError:
        max_domains = 50
    
    print(f"\n🔧 Generating up to {max_domains} domains with {max_words} words...")
    
    # Generate domains
    all_domains = generator.generate_combinations(selected_categories, max_words, include_numbers)
    selected_domains = random.sample(all_domains, min(max_domains, len(all_domains)))
    
    print(f"✅ Generated {len(selected_domains)} unique domain combinations")
    
    # Show some examples
    print(f"\n📝 Sample domains:")
    for domain in selected_domains[:5]:
        print(f"  • {domain}.com")
    
    # Ask if user wants to check availability
    check_availability = input(f"\n🔍 Check availability for all {len(selected_domains)} domains? (y/n): ").lower().startswith('y')
    
    if check_availability:
        print("\n🔍 Checking domain availability...")
        results = generator.batch_check_domains(selected_domains)
        
        # Filter available domains
        available_domains = [r for r in results if r['available']]
        taken_domains = [r for r in results if not r['available']]
        
        print(f"\n📊 Results Summary:")
        print(f"  • Total checked: {len(results)}")
        print(f"  • Available: {len(available_domains)}")
        print(f"  • Taken: {len(taken_domains)}")
        
        if available_domains:
            print(f"\n🎉 Available domains ({len(available_domains)}):")
            for result in available_domains[:20]:  # Show first 20
                verification_icon = "🔍" if result['verification_method'] == 'DNS + WHOIS' else "📡"
                print(f"  ✅ {result['full_domain']} {verification_icon}")
                print(f"     🔗 GoDaddy: {result['godaddy_url']}")
                print(f"     📋 Verified with: {result['verification_method']}")
            
            if len(available_domains) > 20:
                print(f"  ... and {len(available_domains) - 20} more")
        
        # Ask if user wants to see taken domains
        if taken_domains:
            show_taken = input(f"\n👀 Show taken domains? (y/n): ").lower().startswith('y')
            if show_taken:
                print(f"\n❌ Taken domains (first 10):")
                for result in taken_domains[:10]:
                    print(f"  ❌ {result['full_domain']}")
                    print(f"     🔗 GoDaddy: {result['godaddy_url']}")
    
    else:
        print(f"\n📋 Generated domains (first 20):")
        for domain in selected_domains[:20]:
            print(f"  • {domain}.com")
        
        if len(selected_domains) > 20:
            print(f"  ... and {len(selected_domains) - 20} more")
    
    print(f"\n✨ Domain generation complete!")

if __name__ == "__main__":
    main()