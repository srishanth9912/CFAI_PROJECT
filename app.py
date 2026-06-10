from flask import Flask, render_template, request
from time import perf_counter

app = Flask(__name__)

# Bubble Sort
def bubble_sort(arr):
    a = arr.copy()
    n = len(a)

    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                temp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = temp

    return a


# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            numbers = request.form["numbers"]

            arr = []

            for x in numbers.split(","):
                arr.append(int(x.strip()))

            # Bubble Sort Timing
            start = perf_counter()

            for _ in range(1000):
                bubble_result = bubble_sort(arr)

            bubble_time = perf_counter() - start

            # Merge Sort Timing
            start = perf_counter()

            for _ in range(1000):
                merge_result = merge_sort(arr)

            merge_time = perf_counter() - start

            # Winner
            if abs(bubble_time - merge_time) < 0.000001:
                winner = "Tie"
            elif bubble_time < merge_time:
                winner = "Bubble Sort"
            else:
                winner = "Merge Sort"

            return render_template(
                "index.html",
                original_array=arr,
                sorted_array=merge_result,
                bubble_time=round(bubble_time, 6),
                merge_time=round(merge_time, 6),
                winner=winner,
                total=len(arr)
            )

        except ValueError:
            return render_template(
                "index.html",
                error="Please enter valid integers separated by commas."
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)