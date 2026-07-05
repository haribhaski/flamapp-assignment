# flamapp-assignment

The optimization was formulated as a nested parameter estimation problem. The outer optimizer estimated the global curve parameters (θ, M, X), while an inner bounded scalar optimization recovered the closest curve parameter t for each observed point. This avoids introducing one optimization variable per sample point and significantly reduces the dimensionality of the global search space.
