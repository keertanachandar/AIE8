# tools.py - CORRECTED VERSION
from typing import Any, Dict, List, Optional
import json
import re
from dataclasses import dataclass
from enum import Enum

class ToolCategory(Enum):
    """Categories of research tools"""
    PDF_ANALYSIS = "pdf_analysis"
    DATA_EXTRACTION = "data_extraction"
    STATISTICAL_ANALYSIS = "statistical_analysis"
    CITATION_MANAGEMENT = "citation_management"
    WEB_SEARCH = "web_search"

@dataclass
class ToolResult:
    """Result from a tool execution"""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict] = None

class ResearchTools:
    """Collection of research-specific tools"""
    
    @staticmethod
    def get_tool_definitions() -> List[Dict[str, Any]]:
        """Get all tool definitions for Anthropic API"""
        return [
            {
                "name": "extract_statistics",
                "description": "Extract statistical data, percentages, sample sizes, and p-values from text",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to extract statistics from"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "extract_key_findings",
                "description": "Extract main findings, conclusions, and key insights from research text",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The research text to analyze"
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific areas to focus on (optional)"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "categorize_use_cases",
                "description": "Categorize and rank use cases mentioned in the text",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text containing use case information"
                        },
                        "categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Predefined categories (optional)"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "analyze_trends",
                "description": "Identify temporal trends and patterns in the data",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text containing temporal data"
                        },
                        "time_period": {
                            "type": "string",
                            "description": "Time period to focus on (optional)"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "extract_citations",
                "description": "Extract academic citations and references from text",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to extract citations from"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "compare_metrics",
                "description": "Compare metrics across different sections or time periods",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "section1": {
                            "type": "string",
                            "description": "First section to compare"
                        },
                        "section2": {
                            "type": "string",
                            "description": "Second section to compare"
                        },
                        "metric_type": {
                            "type": "string",
                            "description": "Type of metric to compare"
                        }
                    },
                    "required": ["section1", "section2", "metric_type"]
                }
            }
        ]
    
    @staticmethod
    def extract_statistics(text: str) -> ToolResult:
        """Extract statistical data from text"""
        try:
            stats = {
                "percentages": re.findall(r'\d+(?:\.\d+)?%', text),
                "numbers": re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text),
                "dates": re.findall(r'\b(?:19|20)\d{2}\b', text),
                "sample_sizes": re.findall(r'[Nn]\s*=\s*(\d+(?:,\d{3})*)', text),
                "p_values": re.findall(r'[Pp]\s*[<>=]\s*(\d+\.\d+)', text),
            }
            
            return ToolResult(
                success=True,
                data=stats,
                metadata={"total_stats_found": sum(len(v) for v in stats.values())}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))
    
    @staticmethod
    def extract_key_findings(text: str, focus_areas: Optional[List[str]] = None) -> ToolResult:
        """Extract main findings from research text"""
        try:
            findings = []
            patterns = [
                r'(?:we find|we found|results show|findings indicate)[^.!?]*[.!?]',
                r'(?:significantly|notably|importantly)[^.!?]*[.!?]',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                findings.extend(matches)
            
            if focus_areas:
                findings = [f for f in findings if any(area.lower() in f.lower() for area in focus_areas)]
            
            return ToolResult(
                success=True,
                data={"findings": findings[:20], "count": len(findings)},
                metadata={"focus_areas": focus_areas}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))
    
    @staticmethod
    def categorize_use_cases(text: str, categories: Optional[List[str]] = None) -> ToolResult:
        """Categorize use cases from text"""
        try:
            default_categories = ["work", "education", "creative", "personal", "research"]
            cats = categories or default_categories
            use_cases = {cat: [] for cat in cats}
            
            sentences = re.split(r'[.!?]+', text)
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                for cat in cats:
                    if cat.lower() in sentence_lower:
                        use_cases[cat].append(sentence.strip())
            
            ranked = sorted(
                [(cat, len(cases)) for cat, cases in use_cases.items()],
                key=lambda x: x[1],
                reverse=True
            )
            
            return ToolResult(
                success=True,
                data={
                    "categorized_use_cases": use_cases,
                    "ranking": ranked,
                    "top_categories": [cat for cat, _ in ranked[:5]]
                },
                metadata={"categories_used": cats}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))
    
    @staticmethod
    def analyze_trends(text: str, time_period: Optional[str] = None) -> ToolResult:
        """Identify trends in the data"""
        try:
            trends = {
                "growth_indicators": [],
                "decline_indicators": [],
                "temporal_patterns": []
            }
            
            growth_patterns = [r'increas(?:e|ed|ing)', r'grow(?:th|ing|n)', r'ris(?:e|ing|en)']
            decline_patterns = [r'decreas(?:e|ed|ing)', r'declin(?:e|ed|ing)', r'fall(?:ing)?']
            
            sentences = re.split(r'[.!?]+', text)
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                
                if any(re.search(pattern, sentence_lower) for pattern in growth_patterns):
                    trends["growth_indicators"].append(sentence.strip())
                
                if any(re.search(pattern, sentence_lower) for pattern in decline_patterns):
                    trends["decline_indicators"].append(sentence.strip())
                
                if re.search(r'\b(?:19|20)\d{2}\b', sentence):
                    trends["temporal_patterns"].append(sentence.strip())
            
            return ToolResult(
                success=True,
                data=trends,
                metadata={
                    "time_period": time_period,
                    "growth_count": len(trends["growth_indicators"]),
                    "decline_count": len(trends["decline_indicators"])
                }
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))
    
    @staticmethod
    def extract_citations(text: str) -> ToolResult:
        """Extract citations from text"""
        try:
            author_year = re.findall(
                r'([A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?)\s*\((\d{4}[a-z]?)\)',
                text
            )
            numbered = re.findall(r'\[(\d+)\]', text)
            dois = re.findall(r'10\.\d{4,}/[^\s]+', text)
            
            return ToolResult(
                success=True,
                data={
                    "author_year_citations": [{"authors": auth, "year": year} for auth, year in author_year],
                    "numbered_citations": numbered,
                    "dois": dois,
                    "total_citations": len(author_year) + len(numbered)
                },
                metadata={"citation_styles": ["author-year", "numbered", "doi"]}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))
    
    @staticmethod
    def compare_metrics(section1: str, section2: str, metric_type: str) -> ToolResult:
        """Compare metrics between two sections"""
        try:
            nums1 = [float(n.replace(',', '')) for n in re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', section1)]
            nums2 = [float(n.replace(',', '')) for n in re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', section2)]
            
            comparison = {
                "section1_avg": sum(nums1) / len(nums1) if nums1 else 0,
                "section2_avg": sum(nums2) / len(nums2) if nums2 else 0,
                "section1_count": len(nums1),
                "section2_count": len(nums2)
            }
            
            if comparison["section1_avg"] and comparison["section2_avg"]:
                comparison["percent_change"] = (
                    (comparison["section2_avg"] - comparison["section1_avg"]) 
                    / comparison["section1_avg"] * 100
                )
            
            return ToolResult(
                success=True, 
                data=comparison, 
                metadata={"metric_type": metric_type}
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))
    
    @classmethod
    def execute_tool(cls, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name"""
        tool_methods = {
            "extract_statistics": cls.extract_statistics,
            "extract_key_findings": cls.extract_key_findings,
            "categorize_use_cases": cls.categorize_use_cases,
            "analyze_trends": cls.analyze_trends,
            "extract_citations": cls.extract_citations,
            "compare_metrics": cls.compare_metrics
        }
        
        if tool_name not in tool_methods:
            return ToolResult(success=False, data=None, error=f"Unknown tool: {tool_name}")
        
        try:
            return tool_methods[tool_name](**params)
        except Exception as e:
            return ToolResult(success=False, data=None, error=f"Error executing {tool_name}: {str(e)}")