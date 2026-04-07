# Graph README

This file explains the graph portion of the project in simple interview-ready language.

## Intuition

In healthcare, a model often benefits from knowing:
- what the current image looks like
- what the patient's structured features look like
- which **similar prior cases** exist in the dataset

The graph module models each case as a node.  
Edges connect similar cases using embedding similarity.

That lets the model answer:
> "What do similar patients or studies suggest?"

## Graph design

### Nodes
Each node represents one patient study or image sample.

### Node features
Each node can include:
- image embedding
- metadata embedding
- fused embedding

### Edges
Edges are built using nearest-neighbor similarity:
- cosine similarity or Euclidean distance
- connect to top-k nearest neighbors

### Aggregation
A case can refine its representation by aggregating information from neighboring cases:
- weighted average
- attention
- graph neural network layer
- simpler kNN evidence blending

## Practical design used in this package

To keep the project easy to run locally, this package uses a **lightweight graph refinement** method:

1. compute fused embeddings
2. retrieve top-k nearest training examples
3. aggregate their probabilities
4. combine with the base model prediction

This is lighter than a full GNN and much easier to explain in interviews.

## Why this matters

Compared with image-only modeling, graph reasoning can:
- stabilize predictions
- leverage related cases
- better approximate case-based reasoning
- provide a more realistic clinical AI architecture story

## Interview explanation

You can describe it like this:

> "The baseline model predicts from the image alone.  
> Then I extend it to multimodal learning by adding structured clinical features.  
> Finally, I add a graph-inspired refinement stage that retrieves similar prior cases and uses their evidence to improve prediction robustness."

## Architecture graph

See `docs/ARCHITECTURE_GRAPH.md` for the Mermaid diagram.
