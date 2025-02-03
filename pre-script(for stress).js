// Get the current iteration and calculate the request count
const currentIteration = pm.info.iteration;
const totalIterations = pm.info.iterationCount; // Automatically retrieves the total iterations

let requestCount;
const midpoint = Math.floor(totalIterations / 2);

if (currentIteration < midpoint) {
    // Increasing in the first half
    requestCount = Math.pow(2, currentIteration);
} else {
    // Decreasing in the second half
    requestCount = Math.pow(2, totalIterations - currentIteration - 1);
}

console.log(`Iteration ${currentIteration + 1} of ${totalIterations}: Sending ${requestCount} concurrent requests.`);
