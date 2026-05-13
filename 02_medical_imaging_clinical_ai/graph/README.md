# Graph-Enhanced Clinical Reasoning

## Purpose

The graph-enhanced component is included as a portfolio extension for **case-based clinical reasoning**.

The main project compares:

| Model | Input | Clinical meaning |
|---|---|---|
| CNN baseline | Image only | Imaging-only benchmark |
| Multimodal | Image + metadata | Closer to clinical workflow |
| Graph-enhanced | Similar cases | Adds case-based reasoning |

## What graph-enhanced means here

A graph-enhanced clinical AI system can connect patients or imaging cases based on similarity, such as:

- similar image embeddings
- similar age groups
- similar prior condition status
- same scanner site
- similar predicted risk profile

This can support a workflow like:

> “This patient looks similar to prior cases A, B, and C. What were their labels or outcomes?”

## Why it is not fully trained in this lightweight package

The core package is designed to run locally and quickly using MedMNIST.  
MedMNIST does not include rich longitudinal patient records, site information, or clinical outcomes, so the graph part is implemented as a conceptual extension rather than a full graph neural network.

## Suggested future upgrade

A stronger version could add:

1. Extract CNN embeddings for every image.
2. Create a nearest-neighbor graph between cases.
3. Add metadata similarity edges.
4. Train a graph neural network or use graph-based label propagation.
5. Compare graph-enhanced results against CNN and multimodal models.

## Portfolio value

Including this design shows awareness that clinical AI is not only image classification. Real clinical reasoning often benefits from similar-case retrieval, patient context, and explainability.
