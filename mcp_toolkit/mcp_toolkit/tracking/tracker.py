"""
Token Usage Tracking

Classes and utilities for tracking token usage
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class TokenUsage:
    """Track token usage for MCP operations"""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    operation: str = ""

    def __post_init__(self):
        if self.total_tokens == 0:
            self.total_tokens = self.input_tokens + self.output_tokens


@dataclass
class TokenTracker:
    """Global token usage tracker"""
    sessions: List[TokenUsage] = field(default_factory=list)

    def track(self, input_tokens: int, output_tokens: int, operation: str = ""):
        """Record token usage for an operation"""
        usage = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            operation=operation
        )
        self.sessions.append(usage)
        return usage

    def get_totals(self) -> Dict[str, int]:
        """Get cumulative token usage"""
        return {
            "total_input_tokens": sum(s.input_tokens for s in self.sessions),
            "total_output_tokens": sum(s.output_tokens for s in self.sessions),
            "total_tokens": sum(s.total_tokens for s in self.sessions),
            "session_count": len(self.sessions)
        }

    def get_summary(self) -> str:
        """Get formatted summary"""
        totals = self.get_totals()
        return f"""
📊 Token Usage Summary
{'='*60}
Total Sessions: {totals['session_count']}
Input Tokens:   {totals['total_input_tokens']:,}
Output Tokens:  {totals['total_output_tokens']:,}
Total Tokens:   {totals['total_tokens']:,}
{'='*60}
"""

    def compare_scenarios(self, without_filtering: int, with_filtering: int, operation: str = ""):
        """Compare token usage with and without code execution filtering"""
        savings = without_filtering - with_filtering
        savings_pct = (savings / without_filtering * 100) if without_filtering > 0 else 0

        print(f"
💡 Progressive Disclosure Benefits - {operation}")
        print("="*60)
        print(f"Without Code Execution: {without_filtering:,} tokens")
        print(f"With Code Execution:    {with_filtering:,} tokens")
        print(f"Tokens Saved:           {savings:,} tokens ({savings_pct:.1f}% reduction)")
        print("="*60)

        return {
            "without_filtering": without_filtering,
            "with_filtering": with_filtering,
            "tokens_saved": savings,
            "savings_percentage": savings_pct
        }

    def reset(self):
        """Clear all tracked sessions"""
        self.sessions.clear()


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of tokens (Claude uses ~4 chars per token on average)
    For more accurate counting, use tiktoken or anthropic's tokenizer
    """
    return len(text) // 4


# Global tracker instance
token_tracker = TokenTracker()
