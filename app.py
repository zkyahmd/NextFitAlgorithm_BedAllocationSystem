from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages to work

# Bed class
class Bed:
    def __init__(self, bed_type, size):
        self.bed_type = bed_type
        self.size = size
        self.is_free = True  # True means bed is free, False means it's allocated

    def __str__(self):
        status = "Free" if self.is_free else "Allocated"
        return f"Type: {self.bed_type}, Size: {self.size}, Status: {status}"


# Next Fit Allocator class
class NextFitAllocator:
    def __init__(self, beds):
        self.beds = beds
        self.last_allocated_index = 0  # This keeps track of the last allocated bed index

    def allocate(self, request_size, bed_type):
        n = len(self.beds)
        start_index = self.last_allocated_index
        for i in range(n):
            index = (start_index + i) % n  # Wrap around if we reach the end
            bed = self.beds[index]
            if bed.is_free and bed.size >= request_size and bed.bed_type == bed_type:
                bed.is_free = False  # Mark bed as allocated
                self.last_allocated_index = index  # Update last allocated index
                return f"Allocated {bed_type} bed of size {request_size} at index {index}."
        return f"Failed to allocate {bed_type} bed of size {request_size}. No suitable bed available."

    def free(self, bed_index):
        if 0 <= bed_index < len(self.beds):
            bed = self.beds[bed_index]
            if bed.is_free:
                return f"Bed at index {bed_index} is already free."
            bed.is_free = True  # Mark bed as free
            return f"Freed bed at index {bed_index}."
        return "Invalid bed index."

    def get_bed_states(self):
        return [str(bed) for bed in self.beds]


# Initialize beds and allocator
beds = [
    Bed("General", 2),
    Bed("ICU", 1),
    Bed("General", 3),
    Bed("Private", 1)
]
allocator = NextFitAllocator(beds)


@app.route('/')
def index():
    # Display the current states of beds
    return render_template('index.html', beds=allocator.get_bed_states())


@app.route('/allocate', methods=['POST'])
def allocate():
    bed_type = request.form['bed_type']
    size = int(request.form['size'])
    result = allocator.allocate(size, bed_type)
    flash(result)  # Flash the result message for the user
    return redirect(url_for('index'))


@app.route('/free', methods=['POST'])
def free():
    index = int(request.form['index'])
    result = allocator.free(index)
    flash(result)  # Flash the result message for the user
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
