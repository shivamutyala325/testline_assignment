import json
import matplotlib.pyplot as plt
from collections import defaultdict


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_topic_wise_performance(history_data):
    #store the history data
    topic_scores = defaultdict(list)
    topic_accuracies = defaultdict(list)
    topic_attempts = defaultdict(int)
    topic_trends = defaultdict(list)

    for quiz in history_data:
        topic = quiz["quiz"]["topic"]
        topic_scores[topic].append(quiz["score"])
        accuracy = float(quiz["accuracy"].replace(" %", ""))
        topic_accuracies[topic].append(accuracy)
        topic_attempts[topic] += 1
        topic_trends[topic].append((quiz["submitted_at"], quiz["score"]))

    avg_scores = {topic: sum(scores) / len(scores) for topic, scores in topic_scores.items()}
    avg_accuracies = {topic: sum(accs) / len(accs) for topic, accs in topic_accuracies.items()}

    return avg_scores, avg_accuracies, topic_scores, topic_attempts, topic_trends


def compare_performance(topic_scores, topic_attempts, topic_trends, latest_quiz):
    topic = latest_quiz["quiz"]["topic"]
    latest_score = latest_quiz["score"]
    previous_scores = topic_scores.get(topic, [])
    attempts = topic_attempts.get(topic, 0)

    comparison_message = f"The present quiz is based on '{topic}'. You have attempted this topic {attempts} times. "

    if previous_scores:
        avg_previous_score = sum(previous_scores) / len(previous_scores)
        comparison_message += f"The previous average score for this topic was {avg_previous_score:.2f}. "
        if latest_score > avg_previous_score:
            recommendation = f"Your performance in '{topic}' has improved! Keep it up."
        else:
            recommendation = f"Your performance in '{topic}' has decreased. Revise the topic to improve."
    else:
        recommendation = f"No previous data available for '{topic}'."

    incorrect_answers = latest_quiz["incorrect_answers"]
    if incorrect_answers > 5:  # Threshold for too many mistakes
        recommendation += " You made many incorrect attempts. Focus on accuracy."

    return comparison_message + recommendation


def plot_trend_analysis(topic_trends):
    plt.figure(figsize=(12, 6))

    for topic, trends in topic_trends.items():
        dates = [t[0] for t in trends]
        scores = [t[1] for t in trends]
        plt.plot(dates, scores, marker='o', label=topic)

    plt.xlabel("Attempt Date")
    plt.ylabel("Score")
    plt.title("Topic-wise Performance Trend Over Time")
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.grid()
    plt.show()


def plot_histograms(avg_scores, avg_accuracies):
    topics = list(avg_scores.keys())
    scores = list(avg_scores.values())
    accuracies = list(avg_accuracies.values())

    plt.figure(figsize=(12, 5))

    #visualising scores
    plt.subplot(1, 2, 1)
    plt.bar(topics, scores, color='blue')
    plt.xlabel("Topics")
    plt.ylabel("Average Score")
    plt.title("Topic-wise Score Comparison")
    plt.xticks(rotation=45, ha='right')

    #visualsing accuraies
    plt.subplot(1, 2, 2)
    plt.bar(topics, accuracies, color='green')
    plt.xlabel("Topics")
    plt.ylabel("Average Accuracy (%)")
    plt.title("Topic-wise Accuracy Comparison")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()



history_data = load_json("XgAgFJ.json")
latest_quiz = history_data[1]  #take one entry out of 14 as an example


avg_scores, avg_accuracies, topic_scores, topic_attempts, topic_trends = analyze_topic_wise_performance(history_data)


recommendation = compare_performance(topic_scores, topic_attempts, topic_trends, latest_quiz) #comparing the present performance with previous
print("Recommendation:", recommendation)


#visualize the insights
plot_histograms(avg_scores, avg_accuracies)
plot_trend_analysis(topic_trends)
