# macOS same-path installation

The requested final path remains exactly:

`/Users/yuzhang/projects/Machine_learning/11_enterprise_data_platform_architecture`

The reported `PermissionError` occurs before pip reads the project. Python cannot call `os.getcwd()` for the current directory object. The installer recreates the directory at the same path, removes quarantine metadata, preserves the old copy as a timestamped backup, and verifies directory access.

From the folder containing this distribution, run:

```bash
bash INSTALL_AT_SAME_PATH.sh
```

Then follow the commands printed by the installer.
