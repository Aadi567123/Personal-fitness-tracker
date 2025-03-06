from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Function to calculate calories burned
def calculate_calories(age, bmi, duration, heart_rate, gender):
    if gender == "male":
        return round((0.6309 * heart_rate + 0.1988 * bmi + 0.2017 * age - 55.0969) * duration / 4.184, 2)
    else:
        return round((0.4472 * heart_rate - 0.1263 * bmi + 0.074 * age - 20.4022) * duration / 4.184, 2)

# Function to generate exercise recommendations
def get_recommendations(bmi, goal):
    if goal == "weight_loss":
        if bmi > 25:
            return "Focus on cardio exercises like running, cycling, and HIIT. Strength training 2-3 times a week."
        else:
            return "Maintain with a mix of strength training and moderate cardio."
    elif goal == "muscle_gain":
        return "Prioritize weightlifting with compound movements (squats, deadlifts, bench press). Increase protein intake."
    elif goal == "endurance":
        return "Perform long-duration, low-intensity workouts like running, swimming, and cycling. Add interval training."
    return "Select a valid goal to receive recommendations."

@app.route('/')
def index():
    return render_template('index.html', workout_data=[])

@app.route('/calculate', methods=['POST'])
def calculate():
    age = int(request.form['age'])
    bmi = float(request.form['bmi'])
    duration = int(request.form['duration'])
    heart_rate = int(request.form['heartRate'])
    gender = request.form['gender']
    goal = request.form['goal']

    calories_burned = calculate_calories(age, bmi, duration, heart_rate, gender)
    recommendations = get_recommendations(bmi, goal)
    
    workout_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "age": age,
        "bmi": bmi,
        "duration": duration,
        "heartRate": heart_rate,
        "gender": gender,
        "caloriesBurned": calories_burned,
        "recommendations": recommendations
    }

    return jsonify(workout_entry)

if __name__ == '__main__':
    app.run(debug=True)
