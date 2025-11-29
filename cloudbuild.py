steps:
  # Step 1: Build the Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args: [
      'build',
      '-t', 'gcr.io/$PROJECT_ID/machine-learning-repo',
      '.'
    ]

images:
  - 'gcr.io/$PROJECT_ID/machine-learning-repo'
