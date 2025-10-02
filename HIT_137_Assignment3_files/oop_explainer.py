# This file provides explanation and model metadata for bottom of the Tkinter GUI

def get_oop_explanation():  # Returns formatted explanation of OOP concepts
    return (
        "• Multiple Inheritance: GUI inherits from Tkinter and ModelRunner\n"
        "• Encapsulation: GUI components wrapped in methods\n"
        "• Polymorphism: Handle to Model\n"
            "•Image to Text (Salesforce/Blip AI Model) &\n"
            "•Text to Audio (Suno/Bark AI Model)\n"
        "• Method Overriding: display_output could be overridden in subclasses\n"
        "• Multiple Decorators: Logging and Error Handling"
    )

def get_model_info(name, category, description):  # Formats model for display
    return f"Model Name: {name}\nCategory: {category}\nShort Description: {description}" 
#Explains which AI model is used and what type of AI model it is with a description and category
