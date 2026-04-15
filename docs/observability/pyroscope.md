# Continuous CPU & Memory Profiling using Pyroscope

## Problem

- Hidden Performance Bottlenecks: Standard metrics and logs often fail to reveal why a CPU is spiking or why memory is leaking at the code level, leading to "guess-driven" optimization.

- High Overhead of Traditional Profiling: Running manual profilers in production frequently causes significant performance degradation, making it risky to capture data during actual incidents.

- "It Works on My Machine" Syndrome: Performance issues that appear only under production-scale loads are nearly impossible to replicate in local environments without continuous data.

- Lack of Historical Context: Transient performance regressions are often missed because traditional profiling is usually "point-in-time" rather than recorded over days or weeks.

## Solution

- Pyroscope Integration: Deployed Grafana Pyroscope as a centralized continuous profiling platform to capture, store, and analyze functional-level performance data across the entire stack.

- Low-Overhead Agent Deployment: Implemented eBPF-based profiling and language-specific SDKs (Go, Python, Java, Rust) to ensure data collection with minimal impact on application throughput.

- Flame Graph Analysis: Utilized interactive Flame Graphs to visualize "hot paths" in the code, allowing developers to pinpoint the exact line of code consuming the most resources.

- Differential Profiling (Diff View): Enabled comparison between different deployments or time ranges to instantly identify performance regressions introduced by new code commits.

- Integration with Grafana Stack: Unified profiling data with existing Prometheus metrics and Tempo traces, providing a "single pane of glass" for troubleshooting the entire request lifecycle.
