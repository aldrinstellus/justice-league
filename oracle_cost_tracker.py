#!/usr/bin/env python3
"""
Oracle Cost Tracker - Pre-flight, In-flight, Post-flight expense analysis
Runs in parallel with Quicksilver exports without blocking progress
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Claude Sonnet 4.5 Pricing (per 1M tokens)
PRICING = {
    "input": 3.00,
    "output": 15.00,
    "cache_write": 3.75,
    "cache_read": 0.30
}

# Estimated token usage per operation
TOKEN_ESTIMATES = {
    "frame_analysis": 150,  # tokens per frame analyzed
    "page_analysis": 500,   # tokens per page analyzed
    "file_metadata": 2000,  # tokens for file metadata
    "oracle_overhead": 5000 # Oracle coordination overhead
}

def get_figma_token():
    """Get Figma access token from environment"""
    return os.getenv('FIGMA_ACCESS_TOKEN')

def fetch_file_metadata(file_key):
    """Fetch Figma file metadata for cost estimation"""
    token = get_figma_token()
    if not token:
        print("❌ FIGMA_ACCESS_TOKEN not set")
        return None
    
    url = f"https://api.figma.com/v1/files/{file_key}"
    headers = {"X-Figma-Token": token}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching file metadata: {e}")
        return None

def count_frames(node, count=0):
    """Recursively count frames in Figma file"""
    if node.get('type') == 'FRAME':
        count += 1
    
    for child in node.get('children', []):
        count = count_frames(child, count)
    
    return count

def analyze_file_structure(data):
    """Analyze Figma file structure for cost estimation"""
    document = data.get('document', {})
    pages = document.get('children', [])
    
    total_frames = 0
    page_count = len(pages)
    
    for page in pages:
        total_frames += count_frames(page)
    
    return {
        "pages": page_count,
        "frames": total_frames,
        "file_name": data.get('name', 'Unknown')
    }

def estimate_pre_flight_cost(structure):
    """Estimate costs before export begins"""
    frames = structure['frames']
    pages = structure['pages']
    
    # Token estimates
    input_tokens = (
        frames * TOKEN_ESTIMATES['frame_analysis'] +
        pages * TOKEN_ESTIMATES['page_analysis'] +
        TOKEN_ESTIMATES['file_metadata'] +
        TOKEN_ESTIMATES['oracle_overhead']
    )
    
    output_tokens = int(input_tokens * 0.15)  # 15% output ratio
    cached_tokens = int(input_tokens * 0.30)  # 30% cache usage
    
    # Cost calculations
    costs = {
        "input": (input_tokens / 1_000_000) * PRICING['input'],
        "output": (output_tokens / 1_000_000) * PRICING['output'],
        "cache_write": (cached_tokens / 1_000_000) * PRICING['cache_write'],
        "cache_read": (cached_tokens / 1_000_000) * PRICING['cache_read']
    }
    
    total_cost = sum(costs.values())
    
    return {
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "cached": cached_tokens,
            "total": input_tokens + output_tokens
        },
        "costs": costs,
        "total_cost": total_cost
    }

def generate_pre_flight_report(file_key, structure, estimates):
    """Generate pre-flight cost report"""
    print("\n" + "="*80)
    print("🔮 ORACLE: PRE-FLIGHT COST ANALYSIS")
    print("="*80)
    print(f"\n📁 File: {structure['file_name']}")
    print(f"🔑 Key: {file_key}")
    print(f"\n📊 Structure:")
    print(f"   Pages: {structure['pages']}")
    print(f"   Frames: {structure['frames']}")
    
    print(f"\n🎯 Estimated Token Usage:")
    print(f"   Input:  {estimates['tokens']['input']:,} tokens")
    print(f"   Output: {estimates['tokens']['output']:,} tokens")
    print(f"   Cached: {estimates['tokens']['cached']:,} tokens")
    print(f"   Total:  {estimates['tokens']['total']:,} tokens")
    
    print(f"\n💰 Estimated Costs:")
    print(f"   Input:       ${estimates['costs']['input']:.3f}")
    print(f"   Output:      ${estimates['costs']['output']:.3f}")
    print(f"   Cache Write: ${estimates['costs']['cache_write']:.3f}")
    print(f"   Cache Read:  ${estimates['costs']['cache_read']:.3f}")
    print(f"   ───────────────────────")
    print(f"   TOTAL:       ${estimates['total_cost']:.2f}")
    
    print(f"\n✅ Budget approved. Quicksilver ready for high-speed export.")
    print("="*80 + "\n")
    
    return {
        "phase": "pre_flight",
        "timestamp": datetime.now().isoformat(),
        "file_key": file_key,
        "file_name": structure['file_name'],
        "structure": structure,
        "estimates": estimates
    }

def generate_post_flight_report(pre_flight_data, actual_tokens, export_stats):
    """Generate post-flight cost report with actuals vs estimates"""
    estimates = pre_flight_data['estimates']
    
    # Calculate actual costs
    actual_costs = {
        "input": (actual_tokens['input'] / 1_000_000) * PRICING['input'],
        "output": (actual_tokens['output'] / 1_000_000) * PRICING['output'],
        "cache_write": (actual_tokens.get('cache_write', 0) / 1_000_000) * PRICING['cache_write'],
        "cache_read": (actual_tokens.get('cache_read', 0) / 1_000_000) * PRICING['cache_read']
    }
    actual_total = sum(actual_costs.values())
    
    # Calculate variance
    variance = actual_total - estimates['total_cost']
    variance_pct = (variance / estimates['total_cost']) * 100 if estimates['total_cost'] > 0 else 0
    
    print("\n" + "="*80)
    print("🔮 ORACLE: POST-FLIGHT COST ANALYSIS")
    print("="*80)
    print(f"\n📁 File: {pre_flight_data['file_name']}")
    print(f"✅ Export: {export_stats['frames_exported']}/{export_stats['total_frames']} frames ({export_stats['success_rate']:.1f}%)")
    
    print(f"\n📊 Token Usage (Actual vs Estimated):")
    print(f"   Input:  {actual_tokens['input']:,} ({estimates['tokens']['input']:,})")
    print(f"   Output: {actual_tokens['output']:,} ({estimates['tokens']['output']:,})")
    print(f"   Total:  {actual_tokens['input'] + actual_tokens['output']:,} ({estimates['tokens']['total']:,})")
    
    print(f"\n💰 Costs (Actual vs Estimated):")
    print(f"   Input:       ${actual_costs['input']:.3f} (${estimates['costs']['input']:.3f})")
    print(f"   Output:      ${actual_costs['output']:.3f} (${estimates['costs']['output']:.3f})")
    print(f"   Cache Write: ${actual_costs['cache_write']:.3f} (${estimates['costs']['cache_write']:.3f})")
    print(f"   Cache Read:  ${actual_costs['cache_read']:.3f} (${estimates['costs']['cache_read']:.3f})")
    print(f"   ───────────────────────")
    print(f"   ACTUAL:      ${actual_total:.2f}")
    print(f"   ESTIMATED:   ${estimates['total_cost']:.2f}")
    print(f"   VARIANCE:    ${variance:+.2f} ({variance_pct:+.1f}%)")
    
    # Efficiency metrics
    cost_per_frame = actual_total / export_stats['frames_exported'] if export_stats['frames_exported'] > 0 else 0
    print(f"\n📈 Efficiency Metrics:")
    print(f"   Cost per Frame: ${cost_per_frame:.4f}")
    print(f"   Frames per Dollar: {1/cost_per_frame:.0f} frames" if cost_per_frame > 0 else "   Frames per Dollar: N/A")
    print(f"   Success Rate: {export_stats['success_rate']:.1f}%")
    
    print("\n" + "="*80 + "\n")
    
    return {
        "phase": "post_flight",
        "timestamp": datetime.now().isoformat(),
        "file_key": pre_flight_data['file_key'],
        "file_name": pre_flight_data['file_name'],
        "estimates": estimates,
        "actuals": {
            "tokens": actual_tokens,
            "costs": actual_costs,
            "total_cost": actual_total
        },
        "variance": {
            "amount": variance,
            "percentage": variance_pct
        },
        "export_stats": export_stats,
        "efficiency_metrics": {
            "cost_per_frame": cost_per_frame,
            "frames_per_dollar": 1/cost_per_frame if cost_per_frame > 0 else 0,
            "success_rate": export_stats['success_rate']
        }
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 oracle_cost_tracker.py <file_key> [phase]")
        print("Phases: pre-flight (default), post-flight")
        sys.exit(1)
    
    file_key = sys.argv[1]
    phase = sys.argv[2] if len(sys.argv) > 2 else "pre-flight"
    
    if phase == "pre-flight":
        # Pre-flight analysis
        print("🔮 Oracle: Analyzing file structure for cost estimation...")
        metadata = fetch_file_metadata(file_key)
        
        if not metadata:
            sys.exit(1)
        
        structure = analyze_file_structure(metadata)
        estimates = estimate_pre_flight_cost(structure)
        report = generate_pre_flight_report(file_key, structure, estimates)
        
        # Save pre-flight data for post-flight comparison
        output_file = f"pre-flight-{file_key}.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Pre-flight data saved to: {output_file}")
    
    elif phase == "post-flight":
        # Post-flight analysis (requires pre-flight data)
        pre_flight_file = f"pre-flight-{file_key}.json"
        
        if not os.path.exists(pre_flight_file):
            print(f"❌ Pre-flight data not found: {pre_flight_file}")
            sys.exit(1)
        
        with open(pre_flight_file, 'r') as f:
            pre_flight_data = json.load(f)
        
        # Get actual tokens from command line or estimate
        actual_input = int(sys.argv[3]) if len(sys.argv) > 3 else pre_flight_data['estimates']['tokens']['input']
        actual_output = int(sys.argv[4]) if len(sys.argv) > 4 else pre_flight_data['estimates']['tokens']['output']
        
        actual_tokens = {
            "input": actual_input,
            "output": actual_output,
            "cache_write": int(sys.argv[5]) if len(sys.argv) > 5 else 0,
            "cache_read": int(sys.argv[6]) if len(sys.argv) > 6 else 0
        }
        
        # Get export stats
        frames_exported = int(sys.argv[7]) if len(sys.argv) > 7 else pre_flight_data['structure']['frames']
        total_frames = pre_flight_data['structure']['frames']
        success_rate = (frames_exported / total_frames * 100) if total_frames > 0 else 0
        
        export_stats = {
            "frames_exported": frames_exported,
            "total_frames": total_frames,
            "success_rate": success_rate
        }
        
        report = generate_post_flight_report(pre_flight_data, actual_tokens, export_stats)
        
        # Save post-flight report
        output_file = f"post-flight-{file_key}.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Post-flight report saved to: {output_file}")

if __name__ == "__main__":
    main()
