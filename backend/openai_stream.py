from openai import OpenAI
import json 
model = "meta-llama/llama-4-maverick:free"

report = ""
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

 
actionables = ""

json_file= json.load(open('data.json')) 


try:
    print("Generating Analysis")
    # Set up the API request
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": "https://heuraca.ai", # Replace with your actual site URL
        "X-Title": "Heuraca AI", # Replace with your actual site name
      },
      model=model,
      max_tokens=1000,  # Limit token usage to stay within free tier limits
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": """
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
              
              """,
              
            },
            {
              "type": "text",
              "text": f"Please Analyze my figma json file{json_file}."
            }
          ]
        }
      ]
    )

    # Check if completion has the expected structure
    if hasattr(completion, 'choices') and completion.choices:
        print("Successfully Generated Analysis")
        report = completion.choices[0].message.content  
    else:
        print("\nError: Unexpected response structure")
        print("API Response:", completion)

        # Check if there's an error field in the response
        if hasattr(completion, 'error') and completion.error:
            print(f"\nAPI Error: {completion.error}")
            
    # Generate actionables based on the report        
    if report:
        completion2 = client.chat.completions.create(
          extra_headers={
            "HTTP-Referer": "https://heuraca.ai",
            "X-Title": "Heuraca AI",
          },
          model=model,
          max_tokens=1000,
          messages=[
            {
              "role": "system",
              "content": [
                {
                  "type": "text",
                  "text": """
                    You are an expert at translating UI and accessibility design analysis into concrete, actionable tasks for designers and developers.

                    When you receive a detailed design analysis, you will:
                    1.  Generate a concise list of actionable tasks based on that analysis.
                    2.  Ensure each task is:
                        a.  **Highly specific:** Clearly stating what needs to be done.
                        b.  **Action-oriented:** Starting with a verb.
                        c.  **Concise:** Preferably under 20-30 words.
                        d.  **Element-specific:** Referencing the element's name or ID if mentioned in the analysis. Be really specific I don't want generic answer I need element specific answers It's fine if you give me 100 task but i need element specific answers.
                        e.  **Solution-oriented where possible:** Including suggested fixes (e.g., specific color codes for contrast issues) if provided in the analysis.
                    3.  Format each task clearly, for example: 'Task X: [Action] on/for [element name/ID] by [doing Y / changing Z to #value]. Reason: [briefly, if needed].'
                    4.  Prioritize the tasks in a descending order don't write it as high priority task or anything just write the tasks in a descending order.
                    5.  I don't need more then tasks no bonus task or reasons or anything just a concise task to what to change. 
                    Await the design analysis data.
                    6.  Treat me as a human who doesn't know much about the html or css's terminologies so don't use any html or css terminologies.
                    7.  At the end of the report give a harsh rating out of 100.
                  """
                }
              ]
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": f"Analyze this report and give me the actionables pointwise.\n{report}"
                }
              ]
            }
          ]
        )
        
        if hasattr(completion2, 'choices') and completion2.choices:
            print("Successfully Generated Actionables")
            actionables = completion2.choices[0].message.content
        else:
            print("\nError generating actionables")
        
except Exception as e:
    print(f"Error occurred: {type(e).__name__}: {str(e)}")
    print("Please check your API key and request parameters.")




with open ('reports/actionable.txt', 'w') as f : 
    f.write(actionables)