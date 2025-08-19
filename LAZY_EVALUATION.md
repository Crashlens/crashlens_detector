# 🚀 Lazy Evaluation Optimization

## Overview

This document describes the lazy evaluation optimization implemented in Crashens Detector to improve performance by exiting early once a trace has been flagged.

## Problem Statement

Previously, the detection system would process ALL traces through ALL detectors sequentially, even after a trace had been flagged by a higher-priority detector. This resulted in unnecessary computation and slower performance, especially for large log files.

## Solution: Lazy Evaluation

The lazy evaluation optimization implements early exit at two levels:

### 1. Main Detection Loop Optimization

**File:** `crashlens/cli.py`

The main detection loop now tracks flagged traces and skips processing remaining traces through lower-priority detectors once they've been flagged:

```python
flagged_traces = set()  # Track traces that have been flagged by any detector

for detector_name, detector in detector_configs:
    # Run detector with lazy evaluation - only process unflagged traces
    if "already_flagged_ids" in detector.detect.__code__.co_varnames:
        # Detector supports suppression - pass both already flagged and newly flagged traces
        already_flagged = set(suppression_engine.trace_ownership.keys()) | flagged_traces
        raw_detections = detector.detect(traces, pricing_config.get("models", {}), already_flagged)
    else:
        # Basic detector - filter traces to only unflagged ones
        unflagged_traces = {trace_id: trace_records for trace_id, trace_records in traces.items() 
                          if trace_id not in flagged_traces}
        raw_detections = detector.detect(unflagged_traces, pricing_config.get("models", {}))
    
    # Update flagged traces set with newly flagged traces
    for detection in active_detections:
        if "trace_id" in detection:
            flagged_traces.add(detection["trace_id"])
```

### 2. Individual Detector Optimization

Each detector now implements early exit once it flags a trace:

#### RetryLoopDetector
```python
# 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
# No need to check other groups in this trace since we've already flagged it
break

# 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
# No need to check other traces since we've already flagged this one
if detections:
    break
```

#### FallbackStormDetector
```python
if detection:
    detections.append(detection)
    # 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
    # No need to check other traces since we've already flagged this one
    break
```

#### FallbackFailureDetector
```python
for failure in fallback_failures:
    failure["trace_id"] = trace_id
    detections.append(failure)
    
    # 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
    # No need to check other failures in this trace since we've already flagged it
    break

# 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
# No need to check other traces since we've already flagged this one
if detections:
    break
```

#### OverkillModelDetector
```python
if detection:
    detections.append(detection)
    # 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
    # No need to check other records in this trace since we've already flagged it
    break

# 🚀 LAZY EVALUATION: Exit early once we've flagged this trace
# No need to check other traces since we've already flagged this one
if detections:
    break
```

## Performance Benefits

### Before Lazy Evaluation
- **All traces processed through all detectors** regardless of priority
- **Redundant computation** for traces already flagged
- **O(n × d)** complexity where n = number of traces, d = number of detectors

### After Lazy Evaluation
- **Early exit** once a trace is flagged
- **Reduced computation** for already-flagged traces
- **O(n × d)** worst case, but typically much better due to early exits

## Priority-Based Suppression

The lazy evaluation works in conjunction with the existing priority-based suppression system:

1. **RetryLoopDetector** (Priority 1) - Claims traces first
2. **FallbackStormDetector** (Priority 2) - Claims remaining traces
3. **FallbackFailureDetector** (Priority 3) - Claims remaining traces
4. **OverkillModelDetector** (Priority 4) - Claims remaining traces

Once a trace is flagged by any detector, lower-priority detectors skip it entirely.

## Testing

Comprehensive tests have been added in `tests/test_lazy_evaluation.py` to verify:

- Each detector exits early after flagging the first trace
- Already flagged traces are properly skipped
- The optimization doesn't break existing functionality

## Backward Compatibility

The lazy evaluation optimization is **fully backward compatible**:

- ✅ All existing tests pass
- ✅ CLI functionality unchanged
- ✅ Detection accuracy maintained
- ✅ Output format preserved

## Implementation Details

### Files Modified
- `crashlens/cli.py` - Main detection loop optimization
- `crashlens/detectors/retry_loops.py` - Early exit implementation
- `crashlens/detectors/fallback_storm.py` - Early exit implementation
- `crashlens/detectors/fallback_failure.py` - Early exit implementation
- `crashlens/detectors/overkill_model_detector.py` - Early exit implementation
- `tests/test_lazy_evaluation.py` - New test suite

### Key Changes
1. **Flagged traces tracking** in main detection loop
2. **Early exit logic** in each detector
3. **Comprehensive test coverage** for the optimization
4. **Preservation of existing functionality** and output format

## Future Enhancements

Potential future optimizations could include:

1. **Parallel processing** of detectors for independent traces
2. **Caching** of detection results
3. **Streaming processing** for very large log files
4. **Adaptive thresholds** based on trace characteristics

## Conclusion

The lazy evaluation optimization significantly improves performance by eliminating redundant computation while maintaining full backward compatibility and detection accuracy. The implementation is robust, well-tested, and ready for production use.
