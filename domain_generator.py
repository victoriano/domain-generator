#!/usr/bin/env python3

import random
import socket
import itertools
import time
import urllib.parse
import subprocess
import re
import json
import os
from typing import List, Set, Optional, Union
import requests

# Try to import python-dotenv for .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass

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
        self.partial_words = []
        self.compulsory_word = None
        self.use_startup_endings = False
        self.startup_endings = ['fy', 'ly', 'io', 'ai', 'app', 'hub', 'lab', 'co', 'go', 'do', 'up', 'kit', 'box', 'zen', 'wave', 'flow', 'spark', 'boost', 'shift', 'leap', 'rush', 'dash', 'zoom', 'sync', 'flex', 'edge', 'mint', 'glow', 'vibe', 'nova', 'pulse', 'peak', 'beam', 'bolt', 'wrap', 'flip', 'snap', 'drop', 'link', 'ping', 'buzz', 'loop', 'grid', 'lens', 'core', 'base', 'stack', 'trace', 'chain', 'nest', 'pod', 'dock', 'spot', 'node', 'cast', 'stream', 'cloud', 'deck', 'forge', 'space', 'ship', 'verse', 'scope', 'view', 'sense', 'mind', 'gear', 'tool', 'path', 'road', 'bridge', 'port', 'gate', 'door', 'star', 'moon', 'sun', 'sky', 'earth', 'sea', 'wind', 'fire', 'ice', 'stone', 'wood', 'steel', 'gold', 'silver', 'blue', 'red', 'green', 'black', 'white']
        
        self.connectors = ['', 'and', 'for', 'the', 'of', 'in', 'on', 'at', 'by', 'with']
        self.suffixes = ['ly', 'hub', 'lab', 'pro', 'max', 'ai', 'io', 'app', 'sys', 'net']
        
    def set_custom_words(self, words_input: str):
        self.custom_words = [word.strip().lower() for word in words_input.split(',') if word.strip()]
    
    def set_partial_words(self, words_input: str):
        self.partial_words = [word.strip().lower() for word in words_input.split(',') if word.strip()]
    
    def set_compulsory_word(self, word: str):
        self.compulsory_word = word.strip().lower() if word.strip() else None
    
    def set_startup_endings(self, use_endings: bool):
        self.use_startup_endings = use_endings
    
    def get_word_list(self, categories: List[str]) -> List[str]:
        all_words = []
        
        # Add category words
        for category in categories:
            if category in self.base_words:
                all_words.extend(self.base_words[category])
        
        # Add custom words
        if self.custom_words:
            all_words.extend(self.custom_words)
        
        # Add partial words
        if self.partial_words:
            all_words.extend(self.partial_words)
        
        return list(set(all_words))
    
    def get_endings(self) -> List[str]:
        if self.use_startup_endings:
            return self.startup_endings
        return self.suffixes
    
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
    
    def whois_check(self, domain: str) -> Optional[bool]:
        """Check domain availability using WHOIS. Returns True if available, False if taken, None if unclear."""
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
    
    def generate_ai_domains(self, context: str, num_domains: int = 20) -> List[str]:
        """Generate domain names using AI via OpenRouter"""
        
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        if not openrouter_key:
            print("⚠️  OPENROUTER_API_KEY environment variable not set")
            print("💡 Setup instructions:")
            print("   1. Get your API key from: https://openrouter.ai/keys")
            print("   2. Set environment variable:")
            print("      export OPENROUTER_API_KEY='your-api-key-here'")
            print("   3. Or create a .env file with: OPENROUTER_API_KEY=your-api-key-here")
            return []
        
        prompt = f"""Generate {num_domains} creative domain name ideas for: {context}

Requirements:
- Domain names should be memorable and brandable
- Maximum 2-3 words combined
- No hyphens or special characters
- Suitable for .com domains
- Mix of abstract and descriptive names
- Consider modern startup naming trends

Return only the domain names, one per line, without .com extension.

Example format:
optimizeflow
dataspring
insightforge
analyticswave"""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "google/gemini-2.5-flash-preview",  # Confirmed working in test
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 300
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse domain names from response
                domains = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('Example'):
                        # Clean up the line
                        domain = re.sub(r'[^a-zA-Z0-9]', '', line.lower())
                        if domain and len(domain) > 2:
                            domains.append(domain)
                
                return domains[:num_domains]
            elif response.status_code == 402:
                print("⚠️  OpenRouter API error: 402 (Payment Required)")
                print("💡 This means your API key is valid but you need to add credits:")
                print("   1. Go to: https://openrouter.ai/credits")
                print("   2. Add credits to your account ($5-10 is plenty)")
                print("   3. Try running the script again")
                return []
            elif response.status_code == 404:
                print("⚠️  OpenRouter API error: 404 (Model Not Found)")
                print("💡 The model name might be incorrect or unavailable. Current model:")
                print(f"   google/gemini-2.5-flash-preview")
                print("💡 Alternative models you can try:")
                print("   - google/gemini-2.0-flash-001 (Gemini 2.0 Flash)")
                print("   - google/gemini-2.5-flash-preview-05-20 (Newer version)")
                return []
            else:
                print(f"⚠️  OpenRouter API error: {response.status_code}")
                if response.status_code == 401:
                    print("💡 This means your API key is invalid or expired")
                return []
                
        except requests.RequestException as e:
            print(f"⚠️  Request failed: {e}")
            return []
        except Exception as e:
            print(f"⚠️  AI generation error: {e}")
            return []

def main():
    generator = DomainGenerator()
    
    print("🌐 Advanced Domain Name Generator")
    print("=" * 45)
    
    # AI Context Input
    print("\n🤖 AI-Powered Domain Generation (Optional)")
    print("Describe your business/project for AI-generated domain suggestions:")
    ai_context = input("\n💭 Business context (press Enter to skip): ").strip()
    
    ai_domains = []
    if ai_context:
        print("\n🔮 Generating AI domain suggestions...")
        ai_domains = generator.generate_ai_domains(ai_context, 15)
        if ai_domains:
            print(f"✨ Generated {len(ai_domains)} AI suggestions")
            print("\n🎯 AI-generated domains:")
            for i, domain in enumerate(ai_domains[:5], 1):
                print(f"  {i}. {domain}.com")
            if len(ai_domains) > 5:
                print(f"  ... and {len(ai_domains) - 5} more")
        else:
            print("⚠️  AI generation failed, continuing with manual generation")
    
    # Manual Generation Setup
    print("\n📝 Manual Domain Generation Setup")
    print("Configure your domain generation preferences:")
    
    # Show available categories
    print("\n📦 Available word categories:")
    categories = list(generator.base_words.keys())
    for i, category in enumerate(categories, 1):
        print(f"  {i}. {category.title()}")
    
    # Get category selection (now optional)
    category_input = input("\n🎯 Select categories (numbers separated by commas, or press Enter to skip): ").strip()
    selected_categories = []
    
    if category_input:
        try:
            category_nums = [int(x.strip()) for x in category_input.split(',')]
            selected_categories = [categories[i-1] for i in category_nums if 1 <= i <= len(categories)]
        except ValueError:
            pass
    
    # Get custom words
    custom_words = input("\n🔤 Add custom words (comma-separated, optional): ").strip()
    if custom_words:
        generator.set_custom_words(custom_words)
    
    # Get partial words
    partial_words = input("\n🧩 Add partial words/stems (e.g., 'octo' from octopus, comma-separated): ").strip()
    if partial_words:
        generator.set_partial_words(partial_words)
    
    # Get compulsory word
    compulsory_word = input("\n🎯 Compulsory word (must appear in all domains, optional): ").strip()
    if compulsory_word:
        generator.set_compulsory_word(compulsory_word)
    
    # Startup endings option
    use_startup_endings = input("\n🚀 Use startup-style endings (fy, ly, io, etc.)? (y/n): ").lower().startswith('y')
    generator.set_startup_endings(use_startup_endings)
    
    # Summary
    print("\n📋 Generation Configuration:")
    if selected_categories:
        print(f"🎨 Categories: {', '.join(selected_categories)}")
    else:
        print("🎨 Categories: None (using custom words only)")
    
    if generator.custom_words:
        print(f"🔤 Custom words: {', '.join(generator.custom_words)}")
    
    if generator.partial_words:
        print(f"🧩 Partial words: {', '.join(generator.partial_words)}")
    
    if generator.compulsory_word:
        print(f"🎯 Compulsory word: {generator.compulsory_word}")
    
    if generator.use_startup_endings:
        print("🚀 Using startup-style endings")
    
    # Check if we have any words to work with
    if not selected_categories and not generator.custom_words and not generator.partial_words:
        print("\n⚠️  No word sources selected. Using default tech + business categories.")
        selected_categories = ['tech', 'business']
    
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
    manual_domains = []
    if selected_categories or generator.custom_words or generator.partial_words:
        manual_domains = generator.generate_combinations(selected_categories, max_words, include_numbers)
    
    # Combine AI and manual domains
    all_domains = list(set(ai_domains + manual_domains))
    
    if not all_domains:
        print("\n⚠️  No domains generated. Please check your configuration.")
        return
    
    selected_domains = random.sample(all_domains, min(max_domains, len(all_domains)))
    
    print(f"✅ Generated {len(selected_domains)} unique domain combinations")
    if ai_domains:
        print(f"  🤖 AI-generated: {len([d for d in selected_domains if d in ai_domains])}")
    if manual_domains:
        print(f"  🔧 Manual combinations: {len([d for d in selected_domains if d in manual_domains])}")
    
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
                source_icon = "🤖" if result['domain'] in ai_domains else "🔧"
                print(f"  ✅ {result['full_domain']} {verification_icon}{source_icon}")
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
    print("\n🔍 Icons guide:")
    print("  🔍 = WHOIS verified")
    print("  📡 = DNS only")
    print("  🤖 = AI generated")
    print("  🔧 = Manual combination")
    
    if not ai_domains and ai_context:
        print("\n💡 Tip: Set OPENROUTER_API_KEY environment variable for AI domain generation")
        print("   Get your key at: https://openrouter.ai/keys")

if __name__ == "__main__":
    main()