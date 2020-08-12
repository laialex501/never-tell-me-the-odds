from flask import Flask, render_template, request, jsonify
from calculator import estimate_probability

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def estimate_prob():
    # Get number of each dice and create dice pool
    ability = int(request.form['ability'])
    proficiency = int(request.form['proficiency'])
    difficulty = int(request.form['difficulty'])
    challenge = int(request.form['challenge'])
    boost = int(request.form['boost'])
    setback = int(request.form['setback'])
    str_dice_pool = {'Ability': ability, 'Proficiency': proficiency, 
        'Difficulty': difficulty, 'Challenge': challenge, 
        'Boost': boost, 'Setback': setback}

    # Get estimation metric and convert to desired attributes
    query = request.form.get('query')
    attr_names = query.split('-')
    prob_of = query.replace('-', ' and ')

    estimate = estimate_probability(str_dice_pool, attr_names)
    str_estimate = str(round(estimate * 100, 1)) + "%"
    return render_template('index.html', show_output=True, prob_of=prob_of, estimate=str_estimate)

@app.route("/estimate", methods=['POST'])
def estimate():
    # Get number of each dice and create dice pool
    response = request.get_json()
    
    ability = int(response['ability'])
    proficiency = int(response['proficiency'])
    difficulty = int(response['difficulty'])
    challenge = int(response['challenge'])
    boost = int(response['boost'])
    setback = int(response['setback'])
    str_dice_pool = {'Ability': ability, 'Proficiency': proficiency, 
        'Difficulty': difficulty, 'Challenge': challenge, 
        'Boost': boost, 'Setback': setback}

    # Get estimation metric and convert to desired attributes
    query = response['query']
    attr_names = query.split('-')
    query_str = query.replace('-', ' and ')

    estimate = estimate_probability(str_dice_pool, attr_names, sample_size=1000, num_samples=1)
    str_estimate = str(round(estimate * 100, 1)) + "%"
    return jsonify(estimate=str_estimate, query_str=query_str)

if __name__ == "__main__":
    app.run(debug=True)