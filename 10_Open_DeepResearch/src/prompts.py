# prompts.py - Custom prompts for different research types

from typing import Dict, List, Optional
from enum import Enum

class ResearchType(Enum):
    """Types of research supported"""
    ACADEMIC = "academic"
    MARKET = "market"
    TECHNICAL = "technical"
    COMPETITIVE = "competitive"
    USER_RESEARCH = "user_research"
    LITERATURE_REVIEW = "literature_review"
    DATA_ANALYSIS = "data_analysis"
    TREND_ANALYSIS = "trend_analysis"

class CustomPrompts:
    """Custom prompts for different research types"""
    
    @staticmethod
    def get_system_prompt(research_type: ResearchType) -> str:
        """Get system prompt based on research type"""
        
        prompts = {
            ResearchType.ACADEMIC: """You are an expert academic research assistant specializing in rigorous analysis.
            
Your responsibilities:
- Extract and analyze research findings with academic rigor
- Identify methodologies, sample sizes, and statistical significance
- Evaluate the quality and validity of research claims
- Extract and properly format citations
- Compare findings across multiple studies
- Identify gaps in the literature
- Assess the strength of evidence presented

Focus on:
- Peer-reviewed sources and academic credibility
- Proper citation of all claims
- Critical evaluation of methodologies
- Statistical significance and effect sizes
- Reproducibility and research quality""",

            ResearchType.MARKET: """You are a market research analyst focused on business intelligence and market dynamics.

Your responsibilities:
- Analyze market size, growth rates, and trends
- Identify key players and competitive positioning
- Extract pricing information and business models
- Understand customer segments and demographics
- Identify market opportunities and threats
- Analyze industry dynamics and disruption factors

Focus on:
- Quantitative metrics (market size, growth %, revenue)
- Competitive landscape and market share
- Customer behavior and preferences
- Industry trends and forecasts
- Business model innovation
- Geographic and demographic segmentation""",

            ResearchType.TECHNICAL: """You are a technical research specialist with deep expertise in technology analysis.

Your responsibilities:
- Analyze technical architectures and implementations
- Evaluate technical specifications and capabilities
- Compare technical approaches and trade-offs
- Identify technical requirements and constraints
- Assess performance metrics and benchmarks
- Understand technical debt and scalability issues

Focus on:
- Technical accuracy and precision
- Architecture patterns and best practices
- Performance characteristics and benchmarks
- Integration points and dependencies
- Security and compliance considerations
- Scalability and maintainability""",

            ResearchType.COMPETITIVE: """You are a competitive intelligence analyst focused on strategic positioning.

Your responsibilities:
- Map competitive landscape and positioning
- Analyze competitor strengths and weaknesses
- Identify differentiators and unique value propositions
- Track competitor moves and strategies
- Assess market positioning and messaging
- Identify opportunities for competitive advantage

Focus on:
- SWOT analysis for key competitors
- Feature and capability comparison
- Pricing and positioning strategies
- Market share and growth trajectories
- Strategic moves and partnerships
- Competitive threats and opportunities""",

            ResearchType.USER_RESEARCH: """You are a user research specialist focused on understanding user behavior and needs.

Your responsibilities:
- Analyze user behaviors, needs, and pain points
- Identify usage patterns and trends
- Understand user demographics and segments
- Extract insights about user satisfaction and feedback
- Identify usability issues and opportunities
- Understand user journeys and workflows

Focus on:
- User-centered insights and empathy
- Behavioral patterns and motivations
- Pain points and friction areas
- User satisfaction metrics (NPS, CSAT, etc.)
- Usage frequency and engagement metrics
- Qualitative feedback and sentiment""",

            ResearchType.LITERATURE_REVIEW: """You are an expert at synthesizing academic literature and research papers.

Your responsibilities:
- Systematically review and categorize research papers
- Identify common themes and findings across studies
- Map the evolution of research over time
- Identify seminal works and key contributors
- Highlight consensus and disagreements in the field
- Identify research gaps and future directions

Focus on:
- Comprehensive coverage of relevant literature
- Chronological and thematic organization
- Critical synthesis of findings
- Identification of research methodologies used
- Quality assessment of sources
- Clear articulation of research gaps""",

            ResearchType.DATA_ANALYSIS: """You are a data analyst focused on extracting insights from quantitative and qualitative data.

Your responsibilities:
- Extract and analyze statistical data and metrics
- Identify patterns, trends, and correlations
- Perform comparative analysis across data points
- Calculate growth rates and key performance indicators
- Visualize data trends and relationships
- Draw actionable insights from data

Focus on:
- Statistical rigor and accuracy
- Clear data visualization and presentation
- Trend identification and forecasting
- Correlation vs. causation
- Data quality and limitations
- Actionable recommendations based on data""",

            ResearchType.TREND_ANALYSIS: """You are a trend analyst focused on identifying and forecasting market and technology trends.

Your responsibilities:
- Identify emerging trends and patterns
- Analyze historical trends and trajectories
- Forecast future developments
- Identify leading and lagging indicators
- Understand drivers and barriers to trends
- Assess trend adoption curves

Focus on:
- Early identification of emerging trends
- Historical context and evolution
- Growth trajectories and adoption rates
- Drivers, enablers, and barriers
- Geographic and demographic variations
- Implications and future scenarios"""
        }
        
        return prompts.get(research_type, prompts[ResearchType.ACADEMIC])
    
    @staticmethod
    def get_clarification_prompt(research_type: ResearchType) -> str:
        """Get clarification prompt based on research type"""
        
        base = "I'll help you with your research request. Let me understand what you need:"
        
        clarifications = {
            ResearchType.ACADEMIC: """
Let me ensure I understand your academic research needs:

1. What specific research question or hypothesis are you investigating?
2. What time period should the research cover?
3. Are there specific journals, authors, or institutions I should prioritize?
4. What level of evidence are you looking for (systematic reviews, RCTs, observational studies)?
5. Do you need specific types of analysis (meta-analysis, statistical tests, etc.)?
""",
            
            ResearchType.MARKET: """
Let me understand your market research objectives:

1. Which market or industry are you analyzing?
2. What geographic regions are relevant?
3. What time period should the analysis cover?
4. Are you interested in specific segments or customer groups?
5. What business decisions will this research inform?
""",
            
            ResearchType.TECHNICAL: """
Let me clarify your technical research requirements:

1. What technology stack or domain are you researching?
2. Are you comparing specific solutions or approaches?
3. What are your key evaluation criteria (performance, cost, scalability)?
4. What is your current technical context or constraints?
5. Are there specific technical metrics you need to analyze?
""",
            
            ResearchType.COMPETITIVE: """
Let me understand your competitive analysis needs:

1. Who are your primary competitors to analyze?
2. What aspects of competition are most important (features, pricing, positioning)?
3. What is your current market position?
4. What time frame should the analysis cover?
5. What strategic decisions will this inform?
""",
            
            ResearchType.USER_RESEARCH: """
Let me clarify your user research objectives:

1. Who is your target user population?
2. What specific user behaviors or needs are you investigating?
3. Are you looking for quantitative data, qualitative insights, or both?
4. What product or service context is relevant?
5. What decisions will these user insights inform?
""",
            
            ResearchType.LITERATURE_REVIEW: """
Let me understand your literature review scope:

1. What is your research topic or question?
2. What time period should the review cover?
3. Are there specific databases or sources to prioritize?
4. What types of studies should be included/excluded?
5. Are you following a specific review methodology (systematic, narrative, scoping)?
""",
            
            ResearchType.DATA_ANALYSIS: """
Let me clarify your data analysis requirements:

1. What data sources or datasets are available?
2. What specific questions or hypotheses should the analysis address?
3. What types of analysis are you interested in (descriptive, predictive, causal)?
4. Are there specific metrics or KPIs to focus on?
5. What format would be most useful for the results?
""",
            
            ResearchType.TREND_ANALYSIS: """
Let me understand your trend analysis needs:

1. What domain or industry trends are you interested in?
2. What time horizon are you analyzing (historical, current, future)?
3. Are there specific trends or technologies you want to focus on?
4. What geographic or demographic scope is relevant?
5. What strategic planning will this trend analysis support?
"""
        }
        
        return base + clarifications.get(research_type, clarifications[ResearchType.ACADEMIC])
    
    @staticmethod
    def get_research_brief_prompt(research_type: ResearchType, user_query: str) -> str:
        """Generate research brief prompt based on type"""
        
        templates = {
            ResearchType.ACADEMIC: """Based on the user's query: "{query}"

Create a detailed research brief for academic analysis that includes:

1. **Research Question**: Clearly articulated research question or hypothesis
2. **Literature Scope**: Types of sources needed (peer-reviewed journals, books, preprints)
3. **Methodology Focus**: Research designs and methods to prioritize
4. **Key Variables**: Main variables, constructs, or phenomena to investigate
5. **Quality Criteria**: Standards for evaluating research quality
6. **Analysis Requirements**: Statistical or analytical methods needed
7. **Citation Requirements**: Citation style and reference management needs

The brief should guide rigorous academic research with emphasis on evidence quality and methodological soundness.""",

            ResearchType.MARKET: """Based on the user's query: "{query}"

Create a comprehensive market research brief that includes:

1. **Market Definition**: Specific market, industry, or segment to analyze
2. **Key Metrics**: Market size, growth rates, and key performance indicators
3. **Competitive Landscape**: Key players and competitive dynamics to investigate
4. **Customer Analysis**: Target segments, behaviors, and preferences
5. **Geographic Scope**: Relevant regions and markets
6. **Time Frame**: Historical data and forecast period
7. **Business Context**: Strategic questions this research will answer

The brief should enable actionable market intelligence gathering.""",

            ResearchType.TECHNICAL: """Based on the user's query: "{query}"

Create a detailed technical research brief that includes:

1. **Technical Domain**: Specific technologies, architectures, or systems to research
2. **Evaluation Criteria**: Performance, scalability, security, cost factors
3. **Technical Requirements**: Constraints, dependencies, and specifications
4. **Comparison Needs**: Alternative solutions or approaches to evaluate
5. **Implementation Context**: Current systems, team capabilities, timeline
6. **Benchmark Requirements**: Performance metrics and testing criteria
7. **Documentation Needs**: Technical specifications and integration guides

The brief should guide thorough technical evaluation and decision-making.""",

            ResearchType.COMPETITIVE: """Based on the user's query: "{query}"

Create a strategic competitive analysis brief that includes:

1. **Competitor Identification**: Primary and secondary competitors to analyze
2. **Analysis Dimensions**: Features, pricing, positioning, strategy
3. **Market Context**: Industry dynamics and market forces
4. **Differentiation Factors**: Unique value propositions and competitive advantages
5. **Strategic Timeline**: Historical moves and future predictions
6. **Intelligence Sources**: Where to find competitive information
7. **Strategic Questions**: Key decisions this analysis will inform

The brief should enable comprehensive competitive intelligence gathering.""",

            ResearchType.USER_RESEARCH: """Based on the user's query: "{query}"

Create a user research brief that includes:

1. **Research Objectives**: Specific user insights needed
2. **User Population**: Target users and relevant segments
3. **Research Methods**: Appropriate qualitative and quantitative approaches
4. **Key Questions**: Specific questions about user behavior and needs
5. **Context**: Product, service, or experience being researched
6. **Data Sources**: User feedback, analytics, interviews, surveys
7. **Insight Requirements**: Types of insights and their application

The brief should guide empathetic, user-centered research.""",

            ResearchType.LITERATURE_REVIEW: """Based on the user's query: "{query}"

Create a systematic literature review brief that includes:

1. **Review Scope**: Topic boundaries and inclusion/exclusion criteria
2. **Search Strategy**: Keywords, databases, and search terms
3. **Time Period**: Date range for literature coverage
4. **Source Types**: Journals, conferences, books, grey literature
5. **Quality Assessment**: Criteria for evaluating source quality
6. **Synthesis Approach**: How findings will be organized and synthesized
7. **Gap Identification**: Areas where literature is lacking

The brief should enable systematic and comprehensive literature coverage.""",

            ResearchType.DATA_ANALYSIS: """Based on the user's query: "{query}"

Create a data analysis brief that includes:

1. **Data Sources**: Available datasets and data collection needs
2. **Analysis Objectives**: Specific questions to answer with data
3. **Analytical Methods**: Statistical tests, models, or techniques needed
4. **Variables of Interest**: Key metrics, dimensions, and relationships
5. **Visualization Needs**: Charts, graphs, and dashboards required
6. **Quality Considerations**: Data cleaning and validation requirements
7. **Deliverables**: Reports, insights, and recommendations format

The brief should guide rigorous and insightful data analysis.""",

            ResearchType.TREND_ANALYSIS: """Based on the user's query: "{query}"

Create a trend analysis brief that includes:

1. **Trend Domain**: Industries, technologies, or markets to analyze
2. **Time Horizon**: Historical context and forecast period
3. **Trend Indicators**: Leading and lagging indicators to monitor
4. **Drivers Analysis**: Forces accelerating or hindering trends
5. **Geographic Scope**: Regional variations and adoption patterns
6. **Impact Assessment**: Implications and consequences of trends
7. **Scenario Planning**: Alternative future scenarios to consider

The brief should enable forward-looking trend identification and forecasting."""
        }
        
        template = templates.get(research_type, templates[ResearchType.ACADEMIC])
        return template.format(query=user_query)
    
    @staticmethod
    def get_supervisor_prompt(research_type: ResearchType) -> str:
        """Get supervisor planning prompt based on research type"""
        
        prompts = {
            ResearchType.ACADEMIC: """As the research supervisor for academic research:

1. Prioritize peer-reviewed and scholarly sources
2. Ensure proper statistical analysis and methodology evaluation
3. Focus on research quality indicators (sample size, p-values, effect sizes)
4. Verify citation accuracy and academic credibility
5. Compare findings across multiple studies for robustness
6. Identify methodological strengths and limitations

Delegate research tasks that ensure comprehensive academic coverage.""",

            ResearchType.MARKET: """As the research supervisor for market research:

1. Gather quantitative market metrics (size, growth, share)
2. Map competitive landscape and key players
3. Analyze customer segments and behaviors
4. Identify pricing and business model information
5. Track industry trends and forecasts
6. Assess market opportunities and threats

Delegate tasks that build complete market intelligence.""",

            ResearchType.TECHNICAL: """As the research supervisor for technical research:

1. Evaluate technical specifications and capabilities
2. Compare architectures and implementation approaches
3. Gather performance benchmarks and metrics
4. Assess scalability and security considerations
5. Identify integration requirements and dependencies
6. Review technical documentation and best practices

Delegate tasks that enable informed technical decisions.""",

            ResearchType.COMPETITIVE: """As the research supervisor for competitive analysis:

1. Map competitor landscape and positioning
2. Analyze strengths, weaknesses, and strategies
3. Compare features, pricing, and value propositions
4. Track competitive moves and market share
5. Identify differentiation opportunities
6. Assess strategic threats and opportunities

Delegate tasks that provide actionable competitive intelligence.""",

            ResearchType.USER_RESEARCH: """As the research supervisor for user research:

1. Gather insights about user behaviors and needs
2. Analyze usage patterns and engagement metrics
3. Identify pain points and satisfaction drivers
4. Segment users and understand demographics
5. Extract qualitative feedback and sentiment
6. Map user journeys and workflows

Delegate tasks that develop deep user understanding.""",

            ResearchType.LITERATURE_REVIEW: """As the research supervisor for literature review:

1. Systematically search across relevant databases
2. Apply inclusion/exclusion criteria consistently
3. Organize papers by theme and chronology
4. Identify seminal works and key contributors
5. Synthesize findings and highlight consensus/disagreement
6. Map research gaps and future directions

Delegate tasks that ensure comprehensive literature coverage.""",

            ResearchType.DATA_ANALYSIS: """As the research supervisor for data analysis:

1. Extract relevant quantitative data and statistics
2. Calculate key metrics and growth rates
3. Identify patterns, trends, and correlations
4. Perform comparative analysis across dimensions
5. Validate data quality and address limitations
6. Generate actionable insights and recommendations

Delegate tasks that transform data into insights.""",

            ResearchType.TREND_ANALYSIS: """As the research supervisor for trend analysis:

1. Identify emerging and established trends
2. Analyze historical trajectories and evolution
3. Assess drivers, enablers, and barriers
4. Track adoption rates and diffusion patterns
5. Forecast future developments and scenarios
6. Understand geographic and demographic variations

Delegate tasks that reveal trend dynamics and implications."""
        }
        
        return prompts.get(research_type, prompts[ResearchType.ACADEMIC])
    
    @staticmethod
    def get_final_report_prompt(research_type: ResearchType) -> str:
        """Get final report formatting prompt based on research type"""
        
        prompts = {
            ResearchType.ACADEMIC: """Generate an academic research report with:

## Executive Summary
Brief overview of research question, methods, and key findings

## Research Question & Objectives
Clear articulation of what was investigated

## Methodology
- Literature search strategy
- Inclusion/exclusion criteria
- Quality assessment approach

## Findings
Organized by theme with proper citations:
- **Main Finding 1** (Author, Year)
- Statistical evidence and effect sizes
- Methodological notes

## Discussion
- Synthesis of findings
- Consistency across studies
- Methodological considerations
- Research quality assessment

## Limitations
- Gaps in literature
- Methodological limitations
- Areas of uncertainty

## Conclusions & Future Research
- Summary of evidence
- Research implications
- Suggested future studies

## References
Complete list of cited works in academic format""",

            ResearchType.MARKET: """Generate a market research report with:

## Executive Summary
Key market findings and strategic recommendations

## Market Overview
- Market definition and scope
- Total addressable market (TAM)
- Market growth rates and forecasts

## Competitive Landscape
- Key players and market share
- Competitive positioning map
- Recent competitive moves

## Customer Analysis
- Target segments and demographics
- Customer needs and behaviors
- Buying patterns and preferences

## Market Trends
- Emerging trends and drivers
- Technology disruption factors
- Regulatory and policy impacts

## Opportunities & Threats
- Market opportunities
- Competitive threats
- Entry barriers and challenges

## Strategic Recommendations
Actionable insights for decision-making

## Data Sources
List of sources and their credibility""",

            ResearchType.TECHNICAL: """Generate a technical research report with:

## Executive Summary
Technical findings and recommendations

## Technical Overview
- Problem statement
- Requirements and constraints
- Evaluation criteria

## Solution Analysis
For each evaluated option:
- Architecture and design
- Key capabilities and features
- Performance characteristics
- Scalability considerations

## Comparative Analysis
- Feature comparison matrix
- Performance benchmarks
- Cost-benefit analysis
- Trade-off analysis

## Technical Recommendations
- Recommended approach with justification
- Implementation considerations
- Risk assessment
- Migration strategy

## Next Steps
- Proof of concept requirements
- Timeline and milestones
- Resource requirements

## Technical References
Documentation and source materials""",

            ResearchType.COMPETITIVE: """Generate a competitive analysis report with:

## Executive Summary
Competitive landscape and strategic implications

## Market Position Map
Visual representation of competitive positioning

## Competitor Profiles
For each major competitor:
- Company overview
- Product/service offerings
- Strengths and weaknesses (SWOT)
- Market share and growth
- Pricing and positioning

## Feature Comparison Matrix
Side-by-side feature comparison

## Competitive Dynamics
- Recent competitive moves
- Strategic partnerships
- Market consolidation trends

## Differentiation Analysis
- Our unique value propositions
- Competitor advantages
- Market gaps and opportunities

## Strategic Recommendations
- Defensive strategies
- Offensive opportunities
- Positioning refinements

## Threat Assessment
- Emerging competitors
- Disruptive technologies
- Market shifts

## Intelligence Sources
Where this information was gathered""",

            ResearchType.USER_RESEARCH: """Generate a user research report with:

## Executive Summary
Key user insights and recommendations

## Research Objectives & Methods
- Research questions
- Methodology used
- User sample characteristics

## User Segments
- Primary user personas
- Demographic breakdown
- Behavioral segments

## Key Findings
### User Behaviors
- Usage patterns and frequency
- Feature adoption
- User workflows

### User Needs & Pain Points
- Primary needs and motivations
- Current frustrations
- Unmet needs

### User Satisfaction
- Satisfaction metrics (NPS, CSAT)
- What users love
- What needs improvement

## Usage Analytics
- Engagement metrics
- Retention and churn
- Feature usage data

## Qualitative Insights
- User quotes and feedback
- Sentiment analysis
- Behavioral observations

## Recommendations
- Product improvements
- Feature prioritization
- UX enhancements

## Next Steps
Further research needed""",

            ResearchType.LITERATURE_REVIEW: """Generate a literature review report with:

## Executive Summary
Overview of literature landscape and key themes

## Introduction
- Research topic and scope
- Review methodology
- Search strategy and criteria

## Literature Landscape
- Number of papers reviewed
- Publication timeline
- Key journals and venues

## Thematic Analysis
For each major theme:
### Theme 1: [Name]
- Key findings across studies
- Representative papers (Author, Year)
- Consensus and disagreements
- Methodological approaches used

## Historical Evolution
How the research has evolved over time

## Seminal Works
Most influential papers and their contributions

## Methodological Review
- Common research designs
- Popular analytical methods
- Strengths and limitations

## Research Gaps
- Understudied areas
- Methodological gaps
- Conflicting findings needing resolution

## Future Directions
Promising areas for future research

## Complete Bibliography
Organized list of all reviewed papers""",

            ResearchType.DATA_ANALYSIS: """Generate a data analysis report with:

## Executive Summary
Key data insights and actionable recommendations

## Analysis Objectives
Questions the analysis addresses

## Data Overview
- Data sources and collection
- Time period covered
- Data quality and limitations

## Descriptive Statistics
- Summary metrics
- Distributions and ranges
- Key data points

## Key Findings
For each finding:
### Finding 1: [Title]
- Supporting data and visualizations
- Statistical significance
- Confidence intervals
- Trend direction and magnitude

## Comparative Analysis
- Segment comparisons
- Time period comparisons
- Benchmark comparisons

## Correlation & Patterns
- Identified relationships
- Causal vs correlational
- Predictive indicators

## Visualizations
[Data charts and graphs throughout]

## Limitations & Caveats
- Data quality issues
- Sample size considerations
- Analytical limitations

## Recommendations
Data-driven action items

## Technical Appendix
- Methodology details
- Statistical tests used
- Data processing steps""",

            ResearchType.TREND_ANALYSIS: """Generate a trend analysis report with:

## Executive Summary
Major trends and strategic implications

## Trend Landscape
Overview of identified trends

## Major Trends
For each significant trend:
### Trend 1: [Name]
- Description and evidence
- Historical context
- Current state
- Growth trajectory
- Adoption curve stage

## Drivers & Enablers
- Technology enablers
- Economic factors
- Social and cultural drivers
- Regulatory influences

## Barriers & Challenges
- Adoption barriers
- Technical challenges
- Market resistance
- Regulatory constraints

## Geographic Variations
Regional adoption patterns and differences

## Demographic Patterns
Adoption across different user groups

## Forecast & Scenarios
- Base case scenario
- Optimistic scenario
- Pessimistic scenario
- Timeline for developments

## Strategic Implications
- Opportunities to capitalize
- Threats to mitigate
- Required capabilities
- Investment priorities

## Leading Indicators
Signals to monitor going forward

## Recommendations
Strategic actions to take"""
        }
        
        return prompts.get(research_type, prompts[ResearchType.ACADEMIC])


# Convenience function to get all prompts for a research type
def get_research_prompts(research_type: ResearchType) -> Dict[str, str]:
    """Get all prompts for a specific research type"""
    return {
        "system": CustomPrompts.get_system_prompt(research_type),
        "clarification": CustomPrompts.get_clarification_prompt(research_type),
        "supervisor": CustomPrompts.get_supervisor_prompt(research_type),
        "final_report": CustomPrompts.get_final_report_prompt(research_type)
    }