import asyncio
import concurrent.futures
import logging
from crewai import Crew, Process
from brand_positioning.agents.agents import create_market_intelligence_agent
from brand_positioning.core.parallel_tasks import (
    create_competitor_analysis_task,
    create_customer_insights_task, 
    create_market_trends_task
)
from brand_positioning.core.tasks import create_positioning_strategy_task, create_strategic_action_task

logger = logging.getLogger(__name__)

class ParallelCrewsOrchestrator:
    """Orchestrate multiple crews running in parallel for maximum performance"""
    
    def __init__(self):
        # Create agents (can be reused across crews)
        self.market_intelligence_agent = create_market_intelligence_agent()
        logger.info("ParallelCrewsOrchestrator initialized")
    
    def create_competitor_crew(self, brand_info: dict):
        """Create crew focused on competitor analysis"""
        task = create_competitor_analysis_task(brand_info)
        task.agent = self.market_intelligence_agent
        
        return Crew(
            agents=[self.market_intelligence_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False  # Reduce noise with multiple crews
        )
    
    def create_customer_crew(self, brand_info: dict):
        """Create crew focused on customer insights"""
        task = create_customer_insights_task(brand_info)
        task.agent = self.market_intelligence_agent
        
        return Crew(
            agents=[self.market_intelligence_agent],
            tasks=[task], 
            process=Process.sequential,
            verbose=False
        )
    
    def create_trends_crew(self, brand_info: dict):
        """Create crew focused on market trends"""
        task = create_market_trends_task(brand_info)
        task.agent = self.market_intelligence_agent
        
        return Crew(
            agents=[self.market_intelligence_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
    
    def run_crew_sync(self, crew):
        """Run a single crew synchronously (for use in thread pool)"""
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            logger.error(f"Crew execution failed: {e}")
            return f"Error: {str(e)}"
    
    async def run_parallel_intelligence(self, brand_info: dict, status_callback=None):
        """Run market intelligence crews in parallel using thread pool"""
        
        if status_callback:
            status_callback("Creating parallel analysis crews...", 10)
        
        # Create three separate crews
        competitor_crew = self.create_competitor_crew(brand_info)
        customer_crew = self.create_customer_crew(brand_info)
        trends_crew = self.create_trends_crew(brand_info)
        
        if status_callback:
            status_callback("Starting parallel execution (3 crews running simultaneously)...", 20)
        
        # Run crews in parallel using thread pool
        loop = asyncio.get_event_loop()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all crews to thread pool
            futures = [
                loop.run_in_executor(executor, self.run_crew_sync, competitor_crew),
                loop.run_in_executor(executor, self.run_crew_sync, customer_crew),
                loop.run_in_executor(executor, self.run_crew_sync, trends_crew)
            ]
            
            if status_callback:
                status_callback("Executing parallel market intelligence (this may take 2-4 minutes)...", 30)
            
            # Wait for all crews to complete
            results = await asyncio.gather(*futures)
            
            if status_callback:
                status_callback("Parallel market intelligence completed!", 80)
        
        # Structure results
        return {
            "competitor_analysis": results[0],
            "customer_insights": results[1], 
            "market_trends": results[2]
        }
    
    async def run_complete_analysis(self, brand_info: dict, status_callback=None):
        """Run complete brand positioning analysis with parallel market intelligence"""
        
        try:
            if status_callback:
                status_callback("Starting comprehensive brand analysis...", 5)
            
            # Step 1: Run parallel market intelligence
            intelligence_results = await self.run_parallel_intelligence(brand_info, status_callback)
            
            if status_callback:
                status_callback("Generating positioning strategy...", 85)
            
            # Step 2: Generate positioning strategy (sequential, depends on intelligence)
            from brand_positioning.agents.agents import create_positioning_strategist_agent
            positioning_agent = create_positioning_strategist_agent()
            
            # Create positioning task with intelligence data embedded in description
            positioning_task = create_positioning_strategy_task(brand_info, intelligence_results)
            positioning_task.agent = positioning_agent
            
            positioning_crew = Crew(
                agents=[positioning_agent],
                tasks=[positioning_task],
                process=Process.sequential,
                verbose=False
            )
            
            positioning_result = positioning_crew.kickoff()
            
            if status_callback:
                status_callback("Generating strategic actions...", 90)
            
            # Step 3: Generate strategic actions (sequential, depends on positioning)
            from brand_positioning.agents.agents import create_strategic_advisor_agent
            advisor_agent = create_strategic_advisor_agent()
            
            # Create action task with positioning results embedded in description
            action_task = create_strategic_action_task(brand_info, str(positioning_result))
            action_task.agent = advisor_agent
            
            action_crew = Crew(
                agents=[advisor_agent],
                tasks=[action_task],
                process=Process.sequential,
                verbose=False
            )
            
            action_result = action_crew.kickoff()
            
            if status_callback:
                status_callback("Analysis completed successfully!", 100)
            
            # Return structured results
            return {
                "brand_info": brand_info,
                "market_intelligence": intelligence_results,
                "positioning_strategy": str(positioning_result),
                "strategic_actions": str(action_result),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Complete analysis failed: {e}")
            if status_callback:
                status_callback(f"Analysis failed: {str(e)}", 100)
            
            return {
                "brand_info": brand_info,
                "error": str(e),
                "success": False
            }

# Synchronous wrapper for Streamlit
def run_parallel_analysis_sync(brand_info: dict, status_callback=None):
    """Synchronous wrapper to run parallel analysis in Streamlit"""
    
    orchestrator = ParallelCrewsOrchestrator()
    
    # Run async function in new event loop
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.run_complete_analysis(brand_info, status_callback)
        )
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Parallel analysis wrapper failed: {e}")
        return {
            "brand_info": brand_info,
            "error": str(e),
            "success": False
        }

# Quick parallel intelligence only
def run_parallel_intelligence_sync(brand_info: dict, status_callback=None):
    """Synchronous wrapper for parallel market intelligence only"""
    
    orchestrator = ParallelCrewsOrchestrator()
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.run_parallel_intelligence(brand_info, status_callback)
        )
        loop.close()
        return {
            "brand_info": brand_info,
            "intelligence": result,
            "success": True
        }
    except Exception as e:
        logger.error(f"Parallel intelligence wrapper failed: {e}")
        return {
            "brand_info": brand_info,
            "error": str(e),
            "success": False
        }