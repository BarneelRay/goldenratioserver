from fastapi import FastAPI
app = FastAPI()

# Number of segments
total_segments = 5

# Task assignments
unassigned_segments = list(range(1, total_segments + 1))

# Results for each segment
segment_results = {i: None for i in range(1, total_segments + 1)}

# API endpoint for root testing purposes
@app.get("/")
def read_root():
    return {"Welcome": "to the golden ratio calculator"}

# API endpoint for assigning a segment of the simulation task
@app.get("/assign-task")
def get_simulation_task():
    if unassigned_segments:
        segment = unassigned_segments.pop(0)
        print(f"{segment} task assigned")
        return {"segment": segment}
    print("extra task call recieved")    
    return {"message": "All tasks are assigned"}

# We create another API endpoint for the Arduino to assign the result back to the master
@app.post("/upload_result/{segment}")
def upload_result(segment: int, result: float):
    # Segment result processing
    # Store aggregated result and update the aggregation
    segment_results[segment] = result
    print(f"{segment} result is recieved")
    return {"message": f"Result for segment {segment} received"}

# We also estimate the Golden Ratio from here.
@app.get("/estimate_phi")
def estimate_phi():
    if all(segment_results.values()):
        estimated_pi = sum(segment_results.values()) / total_segments
        golden_ratio_estimate = (1 + estimated_pi) / 2
        print(f"estimate currently is {golden_ratio_estimate}")
        return {"golden_ratio_estimate": golden_ratio_estimate}
    print("not enough segments returned.")
    return {"issue": "Not enough segments analyzed"}
