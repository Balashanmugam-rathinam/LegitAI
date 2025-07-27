import os
from datetime import datetime

def generate_output_report(resume_text, resume_filename, links, similarity_score):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"report_{os.path.splitext(resume_filename)[0]}_{timestamp}.txt"
    output_path = os.path.join("reports", output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Smart Resume Screener & Verifier Report\n")
        f.write("="*50 + "\n\n")
        f.write(f"Resume Filename: {resume_filename}\n")
        f.write(f"Similarity Score: {similarity_score}%\n\n")

        f.write("Validated Hyperlinks:\n")
        if links:
            for url, status in links:
                f.write(f"- {url} --> {'Valid' if status else 'Invalid'}\n")
        else:
            f.write("No hyperlinks found.\n")

        f.write("\nResume Content:\n")
        f.write("-"*50 + "\n")
        f.write(resume_text)

    return output_path
