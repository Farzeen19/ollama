from flask import Flask, render_template, request, jsonify
from backend.llm import generate
import PyPDF2

app = Flask(__name__)

# /-----------------API ROUTES-----------------/

@app.route('/health', methods=['GET'])
def check_health():
    return {"output": "healthy"}, 200

@app.route('/echo', methods=['POST'])
def echo_post():
    data = request.get_json(silent=True) or {}

    user_input = data.get('user')
    some_value = data.get('some_value')

    # processing it using some functions.
    output = generate(user_input)
    #  ... 
    return jsonify({
        "input": user_input,
        "output": output
    }), 200

@app.route('/summary', methods=['POST'])
def summary_post():
    data = request.get_json(silent=True) or {}
    # input 
    user_input = data.get('user')
    # processing it using some functions.
    prompt = "Summerize this entire text: " + user_input
    output = generate(prompt)
    # ouput
    return jsonify({
        "output": output
    }), 200

@app.route('/rewritetone',methods=['POST'])
def rewrite():
    data=request.get_json(silent=True) or {}
    user_input=data.get('user')
    tone=data.get('tone')
    prompt = f"Rewrite the {user_input} in {tone} tone without changing its meaning" 
    output = generate(prompt)
    #  ... 
    return jsonify({
        "input": user_input,
        "tone":tone,
        "output": output
    }), 200
# /-----------------PAGES-----------------/
@app.route('/keypoints',methods=['POST'])
def points():
    data=request.get_json(silent=True) or {}
    user_input=data.get('user')
    count=data.get('count')
    prompt = f"use {user_input} to provide concised {count} points line by line "
    output=generate(prompt)
    points=[p.strip() for p in output.split("\n") if p.strip()]

    return jsonify({
        "Total_points_requested":count,
        "key_points":points 
    }),200

@app.route('/learningcheck',methods=['POST'])
def learn():
    #data=request.get_json(silent=True) or {}
    level=request.form.get('level')
    ques=request.form.get('ques')
    file=request.files.get('file')

    pdf_text = ""
    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    # --- FIX END ---

    # Pass the EXTRACTED TEXT (pdf_text), not the file object
    prompt =  f"""
    Analyze the following text: {pdf_text} 
    Act as a rigorous teacher. 
    Ask exactly {ques} questions based on the {level} difficulty level. 
    The questions must strictly test reasoning and understanding of the text provided. 
    Do not summarize the content and do not provide any answers.
"""
    output = generate(prompt)
    points=[p.strip() for p in output.split("\n") if p.strip()]

    return jsonify({
        "Difficulty_Level":level,
        "Number_of_Questions":ques,
        "Questions":points 
    }),200

@app.route('/analyzeuseractivity',methods=['POST'])
def analyze():
    data=request.get_json(silent=True) or {}
    user_data=data.get('user_data')
    query=data.get('query')
    prompt=f"{user_data} is certain ,parse the {user_data} with natural language query,identify the {query} and retrieve only the field which is asked,without listing everything "
    output=generate(prompt)
    points=[p.strip() for p in output.split("\n") if p.strip()]
    return jsonify({
        "Query":query,
        "matched_role":points
    })
@app.route('/')
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)