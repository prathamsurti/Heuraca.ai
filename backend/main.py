from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict, Any
import json 
from dotenv import load_dotenv
import google.generativeai  as genai
import os 

# task 0 -> You're an expert UI/UX expert.
# task 1 -> Prompt Engineering no Unnecessary result.Clear result.No hallucination.No token wastage is required
# task 2 -> show it to Ui
# task 3 -> Apply the ruleset of UI/UX. Heuristics.
#step 2 : Action items for the users. Analysis as the prompt. now create actionable items pointwise. 
# next step for us :  Clear actionable items for user with status update.--> Impp
# create a temporary file where to store and track  the actionable items status.--> Imp  
# If checked and completed recommendations , then the audit data is updated and Re-audit.  Audit---> Re-Audit 
# First stage : Audit data and cancel , second stage : Audit Data --> re-audit data and cancel --> Done 

actionables = ""


report_instruction ="""
    You are a professional design analyst evaluating a JSON file extracted from a Figma design. Generate a structured, evidence-based report that identifies specific issues and opportunities for improvement.

The JSON may contain incomplete data, but provide the most thorough analysis possible with available information.

Begin your analysis with:

**DESIGN AUDIT REPORT:**  
[Two-line executive summary of the overall design quality and primary concerns]

Then provide a detailed analysis with these specific sections:

1. **Structural Overview**
   - Document hierarchy and component organization
   - Layout patterns and grid system usage
   - Identify design system elements (if present)

2. **Missing or Incomplete Data**
   - Identify gaps in design documentation
   - Note components with insufficient specifications
   - Flag areas where developer handoff information is inadequate

3. **UI/UX Issues**
   - Inconsistencies in spacing, sizing, or alignment (with exact measurements)
   - Deviations from established patterns
   - Usability concerns with specific interface elements
   - Information architecture and user flow problems

4. **Accessibility Compliance**
   - Color contrast issues (specify exact contrast ratios)
   - Text size and readability concerns (with measurements)
   - Focus state and keyboard navigation problems
   - Screen reader compatibility issues

5. **Improvement Recommendations**
   - Specific design refinements with clear rationale
   - Component consolidation opportunities
   - Consistency enhancements

Conclude with a prioritized summary of the 3-5 most critical issues requiring immediate attention.


"""



actionables_instruction = """

    No greetings. No html code. 
    You're UI/UX and WCAG2.x expert.
    Transform given analysis into a precise list of actionable tasks for the design and development team.

**# ACTIONABLES:**

For each component or design element requiring changes:

**## [Component/Element Name]**
- [Specific change with exact before/after values] (e.g., "Change primary button background from #5C6BC0 (current) to #3F51B5 (target) to achieve WCAG 2.1 AA contrast ratio of 4.5:1")
- [Another specific change with measurements] (e.g., "Increase text input field height from 36px to 44px to meet minimum touch target size requirements")

Requirements for actionable items:
1. Each item must include:
   - The exact current value/state
   - The specific target value/state
   - The measurable improvement this change provides
   - Reference to relevant design principle or accessibility standard (WCAG 2.1 AA, WCAG 2.1 AAA, or specific UI/UX principle)

2. Organize items by component or section for implementation efficiency

3. Prioritize changes that address:
   - Critical accessibility violations (WCAG 2.1 AA compliance minimum)
   - Significant usability barriers
   - Major visual inconsistencies

4. For each recommendation, include the specific measurement or value that represents the ideal implementation target

5. Use developer/designer-friendly language that translates directly to implementation tasks

6. Your Output structure should be : 
this is an example:
task1 : change 'Search' to 'Search News'
task2 : change the color of 'Search' text to #FFFFFF
task3 : Change the position of rectangle 15 to x:20 y:30
... taskn 
7. At the end give a detailed Score of the ui design. 

Be concise about the tasks they all should be one liner of at most 20 words. 
"""


report_model = genai.GenerativeModel(model_name='models/gemini-2.0-flash',system_instruction = report_instruction)

actionable_model = genai.GenerativeModel(model_name='models/gemini-2.0-flash',system_instruction = actionables_instruction)

report = ""

load_dotenv()
app = FastAPI()

try: 
    api_key = os.getenv("GOOGLE_API_KEY")
except Exception as e :
    print("Please set your Google API key in the environment variable GOOGLE_API_KEY")

# Configure CORS properly to handle preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["Content-Type", "Authorization"],
)

latest_audit_data = None

@app.get('/')
async def root():
    return {"message": "Heuraca.ai API is running"}

@app.post('/audit-data')
async def audit_data(request: Request):
    global latest_audit_data
    data = await request.json()
    
    print("Received data:", data)
    
    # Store the data in memory instead of saving to file
    if data:
        latest_audit_data = data
        return {
            "status": "success", 
            "message": "Data received and processed successfully", 
            "data_summary": data
        }
    return {"status": "error", "message": "No data received"}

@app.get('/read-audit')
async def read_audit() -> Dict[str, Any]:
    """
    Read the latest data received by the audit-data endpoint
    """
    global latest_audit_data
    
    return latest_audit_data
        
@app.get('/save-data')
def save_data():
    global latest_audit_data
    with open('data.json','w') as f : 
        json.dump(latest_audit_data, f)
    return {"status": "success", "message": "Data saved successfully"}


@app.post('/generate-recommendations')
async def generate_recommendations(): 
    global report 
    prompt=f"please analyze my figma json file : \n{latest_audit_data}"
    generate_recommendations = report_model.generate_content(prompt, stream = True)
    for chunk in generate_recommendations : 
        print(chunk.text, end= " ")
    report = generate_recommendations.text
    
    return {
        "status": "success",
        "message": "Recommendations generated successfully",
        "recommendations": report
    }
    

@app.post('/generate-actionables')
async def generate_actionables():
    global actionables
    global report
    prompt = f"Analyze the given report and give me the actionables pointwise. \n{report}"
    generate_actionables_response = actionable_model.generate_content(prompt, stream=True)
    
    # Collect the complete response by iterating through the stream
    response_text = ""
    for chunk in generate_actionables_response:
        print(chunk.text, end=" ")
        response_text += chunk.text
    
    # Now use the collected text
    actionables = response_text
    
    # Write actionables to file
    try:
        # Ensure the reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Write to the file
        with open('reports/actionables.txt', 'w') as f:
            f.write(response_text)
        print("Actionables saved to reports/actionables.txt")
    except Exception as e:
        print(f"Error saving actionables to file: {e}")
    
    return {
        "status": "success",
        "message": "Actionables generated successfully",
        "actionables": response_text
    }



with open('reports/actionables.txt','w') as f :
    f.writelines(actionables)
