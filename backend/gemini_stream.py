import google.generativeai as genai 
import os 
import json
from dotenv import load_dotenv

load_dotenv()


json_file= json.load(open('data.json'))

report_prompt = """
You are an expert UI and Accessibility Analyzer. Your role is to meticulously evaluate Figma JSON outputs.

                When you receive a Figma JSON output, you will:
                1.  Conduct a detailed analysis covering:
                    a.  **UI/UX Heuristics:** Evaluate against principles like Nielsen's 10 Heuristics (Visibility of system status, Match system/real world, User control, Consistency, Error prevention, Recognition vs. recall, Flexibility, Aesthetic/minimalist design, Error recovery, Help/documentation).
                    b.  **Web Content Accessibility Guidelines (WCAG 2.x AA/AAA):** Assess based on Perceivable, Operable, Understandable, Robust principles, focusing on:
                        * Text alternatives for non-text content.
                        * Programmatic information and relationships (e.g., labels).
                        * Color use and contrast ratios (text/background, UI components).
                        * Text size and readability.
                        * Keyboard accessibility (navigability, focus visibility – infer where possible).
                        * Target sizes.
                        * Page structure, language, consistent navigation/identification.
                        * Error identification and input labels/instructions.
                    c.  **Structural Integrity & Naming:** Comment on layer name clarity and structural issues (e.g., fill errors) evident in the JSON.
                2.  Provide an overall summary of the design's apparent strengths and areas needing attention before development.
                3.  Reference specific element names and IDs from the JSON to support your findings.
                4.  At the end of the report give a harsh rating out of 100.
                Await the Figma JSON data.
              
"""


actionables_prompt =""" You are an expert at translating UI and accessibility design analysis into concrete, actionable tasks for designers and developers.

When you receive a detailed design analysis, you will:
1.  Generate a concise list of actionable tasks based on that analysis.
2.  Ensure each task is:
    a.  **Highly specific:** Clearly stating what needs to be done.
    b.  **Action-oriented:** Starting with a verb.
    c.  **Concise:** Preferably under 20-30 words.
    d.  **Element-specific:** Referencing the element's name or ID if mentioned in the analysis.
    e.  **Solution-oriented where possible:** Including suggested fixes (e.g., specific color codes for contrast issues) if provided in the analysis.
3.  Format each task clearly, for example: 'Task X: [Action] on/for [element name/ID] by [doing Y / changing Z to #value]. Reason: [briefly, if needed].'
4.  Categorize or prioritize tasks if the analysis provides a basis for doing so (e.g., Critical Accessibility, Usability, Naming).
5.  Never Provide id's rather than that provide me with the name of the element.
6.  There should be no mention regarding HTML files like implement html code or something like that. 
Await the design analysis data.
"""


try:
    api_key = os.getenv("GOOGLE_API_KEY")

except Exception as e:
    print("Please set your Google API key in the environment variable GOOGLE_API_KEY")
    

genai.configure(api_key=api_key)

report_model = genai.GenerativeModel(model_name='models/gemini-2.0-flash',
system_instruction = report_prompt               
)


actionable_model = genai.GenerativeModel(model_name='models/gemini-2.0-flash',
system_instruction = actionables_prompt
)

prompt =f"Please analyze my figma json file : \n{json_file}"








response_stream = report_model.generate_content(prompt, stream=True)
response_text = ""
for chunk in response_stream:
    response_text += chunk.text
    # print(chunk.text, end="")  
# Option 2: Use resolve() to get the complete response
# response = report_model.generate_content(prompt, stream=True).resolve()
# response_text = response.text

prompt2 = f"Analyze the given report and give me the actionables pointwise. \n{response_text}"

# Same issue applies to the second API call
actionable_stream = actionable_model.generate_content(prompt2, stream=True)
actionable_text = ""
for chunk in actionable_stream:
    actionable_text += chunk.text
    print(chunk.text, end="")  # Optional: print as it arrives

# Option 2 for second call:
# actionable_response = actionable_model.generate_content(prompt2, stream=True).resolve()
# actionable_text = actionable_response.text



with open('reports/actionable.txt', 'w') as f:
    f.write(actionable_text)    


